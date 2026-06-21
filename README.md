# Gramin-Nyaya: AI Legal Assistant

## Project Overview

**Project:** Gramin-Nyaya  
**Purpose:** Offline, privacy-first legal information assistance for rural users in India.  
**Primary law covered:** Registration Act, 1908.  
**Primary language:** Hindi, with legal retrieval grounded in English source text.  
**Deployment target:** Low-memory edge hardware such as NVIDIA Jetson.  
**Privacy model:** Local-only processing; user questions and responses do not need to leave the device.  
**Status:** Prototype legal information system, not a substitute for a licensed lawyer.

Gramin-Nyaya, meaning Rural Justice, is an offline AI assistant designed to reduce the legal information gap for rural communities. It provides simplified Hindi answers grounded in official legal documents, with a retrieval workflow tuned for constrained edge devices.

## Author And Review

**Author:** Kkushak16, project creator and repository maintainer.  
**Technical credentials:** AI/RAG application developer responsible for the FastAPI backend, React frontend, ChromaDB retrieval workflow, and Ollama LLM integration.  
**Legal source credentials:** Answers are grounded in the included Registration Act, 1908 source documents.  
**Review note:** This project provides legal information only. Important matters should be reviewed by a qualified legal professional.

## Key Features

**Edge-optimized pipeline:** Powered by Llama 3.2 1B through Ollama and tuned for low-memory devices.  
**Offline operation:** Runs locally without requiring cloud-hosted inference.  
**Privacy-first design:** Keeps legal questions and generated answers on the user's device or local network.  
**Cross-lingual RAG:** Retrieves from clean English legal text, then produces simplified Devanagari Hindi answers.  
**Voice-ready architecture:** Designed to integrate with Faster-Whisper for Hindi speech-to-text.  
**Grounded responses:** Uses LangChain and ChromaDB so answers are based on retrieved legal document chunks.

## Architecture

**Ingestion:** The legal document `registrationActEnglish.txt` is chunked and embedded into a local ChromaDB vector store.  
**Retrieval:** Hindi user questions are mapped to relevant English legal chunks.  
**Generation:** Llama 3.2 1B reads the retrieved facts, preserves legal values such as dates, sections, amounts, and limits, then formats the final response in simple Hindi.  
**Fallback behavior:** If the answer is not present in the retrieved legal context, the assistant should refuse to invent an answer.

## Tech Stack And Libraries

**Core language:** Python 3.10+  
**LLM engine:** `ollama` with `llama3.2:1b`  
**RAG framework:** `langchain`, `langchain-community`  
**Vector database:** `chromadb`  
**Embeddings:** `langchain-huggingface`, `sentence-transformers` using `paraphrase-multilingual-MiniLM-L12-v2`  
**Voice and STT:** `faster-whisper`, `pyaudio`  
**Web server and API:** `fastapi`, `uvicorn`  
**Frontend:** React, Vite, `react-markdown`  
**Document utilities:** `pypdf`

## Project Structure

```text
Gramin-Nyaya/
├── legal_docs/             # Source legal documents
├── chroma_db/              # Local vector database for semantic search
├── api.py                  # FastAPI server connecting backend to frontend
├── rag_logic.py            # LangChain RAG pipeline and LLM prompting logic
├── ingest_docs.py          # Script to chunk and embed documents into ChromaDB
├── frontend/               # React and Vite web interface
└── README.md               # Project overview, author details, and setup notes
```

## Usage Notes

**Backend command:** `uvicorn api:app --host 0.0.0.0 --port 8000`  
**Frontend command:** `npm run dev` from the `frontend` directory.  
**API endpoint:** `POST /ask` with a JSON body containing `question`.  
**Expected answer format:** Simple Hindi legal information grounded in retrieved document text.
