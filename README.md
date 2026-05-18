# ⚖️ Gramin-Nyaya: AI Legal Assistant

**Gramin-Nyaya** is an offline, privacy-focused AI assistant designed to provide legal guidance to rural populations in India. By utilizing Retrieval-Augmented Generation (RAG), the system provides accurate answers from the **Registration Act, 1908** in simple Hindi.

---

## 🚀 Features
- **Offline Intelligence:** Runs locally using Ollama and Qwen 2.5 (1.5B), ensuring data privacy and zero internet cost during inference.
- **Hindi-First Interface:** A minimalist, "Village-Friendly" UI designed for high readability and ease of use.
- **Voice-Enabled:** Integrated with Faster-Whisper for Hindi speech-to-text, allowing users to speak their queries.
- **Verified Legal Data:** Uses RAG to ground AI responses directly in official legal documents, reducing hallucinations.

---

## 🛠️ Tech Stack
- **LLM:** Qwen 2.5 (1.5B) via Ollama
- **Backend:** FastAPI (Python)
- **Vector Database:** ChromaDB
- **STT:** Faster-Whisper (Base model)
- **Frontend:** Simple HTML/CSS/JS (Optimized for low-resource devices)
- **Embeddings:** HuggingFace Multilingual-MiniLM

---

## 📂 Project Structure
- `api.py`: FastAPI server connecting the UI to the AI logic.
- `rag_logic.py`: Core RAG implementation and document processing.
- `stt_service.py`: Speech-to-Text conversion logic.
- `index.html`: The user-friendly web interface.
- `legal_docs/`: Contains the source PDF (Registration Act).
- `requirements.txt`: List of necessary Python libraries.

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Install **Ollama** and pull the model:
  ```bash
  ollama pull qwen2.5:1.5b
