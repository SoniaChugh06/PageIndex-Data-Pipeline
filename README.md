📚 PageIndex-Inspired Hierarchical Chunking for LLM Fine-Tuning

A structure-aware data preprocessing pipeline that transforms markdown documents into hierarchical trees and generates high-quality training data for LLMs.

🔍 What it does
- 📄 Parses markdown into a tree structure (sections & subsections)
- 🧠 Preserves hierarchical context (A > B > C)
- 🔀 Supports both paragraph-level and sentence-level chunking
- 📏 Uses token-aware splitting for optimal chunk sizes
- 🔗 Merges small sections to maintain coherence

🚀 Why this matters
Traditional chunking:
- ❌ Breaks context
- ❌ Ignores document structure

This approach:
- ✅ Preserves hierarchy
- ✅ Improves coherence
- ✅ Enhances context-aware learning during fine-tuning

💡 Key Insight
Chunking is not just preprocessing — it directly impacts how LLMs learn.

🎯 Use Cases
- LLM fine-tuning datasets
- RAG data preprocessing
- Document understanding pipelines
- Structured knowledge extraction

🧠 Inspired by
PageIndex-style document structuring (commonly used in RAG), adapted here for training data generation

🏁 Output Example
{
  "context": "Networking > TCP > Congestion Control",
  "text": "TCP uses congestion control mechanisms to regulate data flow..."
}
