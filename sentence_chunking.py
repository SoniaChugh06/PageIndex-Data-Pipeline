import re
import json
import tiktoken
import spacy

from dataclasses import dataclass
from typing import List
from pathlib import Path
from tqdm import tqdm


# =========================
# Load NLP model
# =========================

nlp = spacy.load("en_core_web_sm")


def split_into_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


# =========================
# Configuration
# =========================

INPUT_FOLDER = "input.data"
OUTPUT_FILE = "sentence_training_dataset.jsonl"

MIN_TOKENS = 200
MAX_TOKENS = 1200

ENCODING = "cl100k_base"


# =========================
# Tokenizer
# =========================

tokenizer = tiktoken.get_encoding(ENCODING)


def token_count(text):
    return len(tokenizer.encode(text))


# =========================
# Data structure
# =========================

@dataclass
class SectionNode:
    title: str
    level: int
    content: str
    children: List["SectionNode"]


# =========================
# Markdown → PageIndex Tree
# =========================

def parse_markdown_to_tree(md_text):

    lines = md_text.split("\n")

    root = []
    stack = []

    for line in lines:

        heading = re.match(r'^(#{1,6})\s+(.*)', line)

        if heading:

            level = len(heading.group(1))
            title = heading.group(2).strip()

            node = SectionNode(
                title=title,
                level=level,
                content="",
                children=[]
            )

            while stack and stack[-1].level >= level:
                stack.pop()

            if stack:
                stack[-1].children.append(node)
            else:
                root.append(node)

            stack.append(node)

        else:
            if stack:
                stack[-1].content += line + "\n"

    return root


# =========================
# PageIndex context builder
# =========================

def flatten_tree(nodes, parent_titles=None):

    if parent_titles is None:
        parent_titles = []

    sections = []

    for node in nodes:

        context = parent_titles + [node.title]
        context_string = " > ".join(context)

        text = node.content.strip()

        if text:
            sections.append({
                "context": context_string,
                "text": text
            })

        if node.children:
            sections.extend(
                flatten_tree(node.children, context)
            )

    return sections


# =========================
# Merge small sections
# =========================

def merge_small_sections(sections):

    merged = []
    buffer = None

    for sec in sections:

        if buffer is None:
            buffer = sec
            continue

        if token_count(buffer["text"]) < MIN_TOKENS:
            buffer["text"] += "\n\n" + sec["text"]

        else:
            merged.append(buffer)
            buffer = sec

    if buffer:
        merged.append(buffer)

    return merged


# =========================
# Sentence-based chunking
# =========================

def split_large_sections(text):

    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        candidate = current_chunk + " " + sentence if current_chunk else sentence

        if token_count(candidate) <= MAX_TOKENS:
            current_chunk = candidate

        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# =========================
# Main chunking pipeline
# =========================

def chunk_document(md_text):

    tree = parse_markdown_to_tree(md_text)

    sections = flatten_tree(tree)

    if not sections:
        sections = [{"context": "document", "text": md_text}]

    sections = merge_small_sections(sections)

    dataset_chunks = []

    for sec in sections:

        full_text = sec["context"] + "\n\n" + sec["text"]

        if token_count(full_text) <= MAX_TOKENS:

            dataset_chunks.append({
                "context": sec["context"],
                "text": full_text
            })

        else:

            subchunks = split_large_sections(full_text)

            for sub in subchunks:

                dataset_chunks.append({
                    "context": sec["context"],
                    "text": sub
                })

    return dataset_chunks


# =========================
# Save dataset
# =========================

def save_jsonl(chunks, output_file):

    with open(output_file, "w", encoding="utf-8") as f:

        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


# =========================
# Full pipeline
# =========================

def process_markdown_folder(folder, output_jsonl):

    print("Scanning markdown folder...")

    md_files = list(Path(folder).rglob("*.md"))

    print(f"Found {len(md_files)} markdown files")

    all_chunks = []

    for file in tqdm(md_files):

        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except:
            continue

        chunks = chunk_document(text)

        for c in chunks:
            c["source"] = file.name

        all_chunks.extend(chunks)

    print("Total chunks created:", len(all_chunks))

    save_jsonl(all_chunks, output_jsonl)

    print("Saved dataset to:", output_jsonl)

    print("\nSample chunks:\n")

    for i in range(min(5, len(all_chunks))):
        print(all_chunks[i])
        print("-" * 80)


# =========================
# Run
# =========================

if __name__ == "__main__":

    process_markdown_folder(INPUT_FOLDER, OUTPUT_FILE)
