# 📚 PageIndex-Inspired Hierarchical Chunking for LLM Fine-Tuning

**A structure-aware data preprocessing pipeline that transforms markdown documents into hierarchical trees and generates high-quality training data for LLMs.**

---

## 🔍 What it does

* 📄 **Parses markdown into a tree structure** (sections & subsections)
* 🧠 **Preserves hierarchical context** (`A > B > C`)
* 🔀 **Supports both paragraph-level and sentence-level chunking**
* 📏 **Uses token-aware splitting** for optimal chunk sizes
* 🔗 **Merges small sections** to maintain coherence

---

## 🚀 Why this matters

### **Traditional chunking:**

* ❌ Breaks context
* ❌ Ignores document structure

### **This approach:**

* ✅ Preserves hierarchy
* ✅ Improves coherence
* ✅ Enhances context-aware learning during fine-tuning

---

## 💡 Key Insight

> **Chunking is not just preprocessing — it directly impacts how LLMs learn.**

---

## 🎯 Use Cases

* LLM fine-tuning datasets
* RAG data preprocessing
* Document understanding pipelines
* Structured knowledge extraction

---

## 🧠 Inspired by

**PageIndex-style document structuring** (commonly used in RAG), adapted here for training data generation.

---

## 🏁 Output Example

```json
{
  "context": "Networking > TCP > Congestion Control",
  "text": "TCP uses congestion control mechanisms to regulate data flow..."
}
```

---

## ⚙️ Setup

Follow these steps to run the project locally:

### **1. Clone the repository**

```bash
git clone https://github.com/SoniaChugh06/PageIndex-Data-Pipeline
cd PageIndex-Data-Pipeline
```

---

### **2. Create and activate a virtual environment**

#### **Windows (VS Code / PowerShell)**

```bash
python -m venv venv
venv\Scripts\activate
```

#### **macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

### **4. Download spaCy model (required for sentence chunking)**

```bash
python -m spacy download en_core_web_sm
```

---

### **5. Run the scripts**

#### **Paragraph Chunking**

```bash
python paragraph_chunking.py
```

#### **Sentence Chunking**

```bash
python sentence_chunking.py
```

---

## 📌 Notes

* Place your markdown files in the configured `INPUT_FOLDER`
* Output will be saved as `.jsonl` files
* You can tweak `MIN_TOKENS` and `MAX_TOKENS` in the scripts

---

## ⚙️ How It Works

1. **Markdown → Parsed into hierarchical tree**
2. **Tree → Flattened with context paths** (`A > B > C`)
3. **Sections → Merged if too small**
4. **Large sections → Split using token-aware logic**
5. **Output → Structured `.jsonl` training dataset**

---

## 🔍 Traditional vs This Approach

| Traditional Chunking | PageIndex-Based Chunking |
| -------------------- | ------------------------ |
| Breaks context       | Preserves hierarchy      |
| Random splits        | Structure-aware          |
| Poor coherence       | High coherence           |
| Flat text            | Context-rich chunks      |

---

## 📁 Project Structure

```
PageIndex-Data-Pipeline/
│── paragraph_chunking.py
│── sentence_chunking.py
│── requirements.txt
│── README.md
```

---

## ⭐ Support

If you found this useful, consider giving it a ⭐ on GitHub!
