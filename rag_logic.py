"""
Gramin-Nyaya: AI Legal Assistant (Core RAG Engine)
==================================================
Orchestrates the offline Retrieval-Augmented Generation (RAG) pipeline.
It persistent loads the vector database and utilizes a dual-agent collaborative reasoning process:
1. DeepSeek-R1 (Researcher): Reads context and extracts precise legal facts at temp 0.0.
2. Qwen 2.5 (Communicator): Explains and localizes facts into conversational, village-friendly language.

Optimizations:
- Persistent vector store check to skip re-embeddings.
- keep_alive: 0 config to unload models instantly and preserve local hardware RAM.

Author: DEI Engineering Team (Human-Centric Design)
Year: 2024
"""

import os
import logging
import ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- Setup Internal Logging ---
logger = logging.getLogger("GraminNyayaRAG")
logger.setLevel(logging.INFO)

DB_DIRECTORY = "./chroma_db"
PDF_DOCUMENT_PATH = "./legal_docs/registrationActHindi.pdf"

# Initialize Multilingual Embedding Engine (Sentence-Transformers)
logger.info("Initializing HuggingFace Multilingual-MiniLM embedding engine...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# --- Persistent Vector Database Loading ---
if os.path.exists(DB_DIRECTORY) and len(os.listdir(DB_DIRECTORY)) > 0:
    logger.info(f"Loading existing persistent Chroma database from '{DB_DIRECTORY}'")
    vector_db = Chroma(
        persist_directory=DB_DIRECTORY,
        embedding_function=embeddings
    )
else:
    logger.info("Chroma database not found or empty. Beginning document indexing pipeline...")
    
    if not os.path.exists(PDF_DOCUMENT_PATH):
        logger.error(f"Critical Error: Statutory PDF not found at '{PDF_DOCUMENT_PATH}'")
        raise FileNotFoundError(f"Missing essential document: {PDF_DOCUMENT_PATH}")
    
    # 1. Parse and extract PDF document content
    logger.info(f"Reading and loading: {PDF_DOCUMENT_PATH}")
    loader = PyPDFLoader(PDF_DOCUMENT_PATH)
    raw_documents = loader.load()
    
    # 2. Text splitting to keep chunks concise and readable
    logger.info("Splitting document into manageable legal context chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    document_chunks = text_splitter.split_documents(raw_documents)
    
    # 3. Create and persist the vector store
    logger.info(f"Generating vectors and storing in '{DB_DIRECTORY}'...")
    vector_db = Chroma.from_documents(
        documents=document_chunks,
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )
    logger.info("Vector database compilation successful.")

def ask_gramin_nyaya(user_query: str) -> str:
    """
    Two-step Retrieval-Augmented Generation reasoning pipeline:
    1. Researcher Agent (DeepSeek-R1): Extracts exact statutory facts and codes from the context.
    2. Communicator Agent (Qwen 2.5): Translates and humanizes the facts into simple, conversational rural Hindi.
    """
    logger.info(f"Querying RAG system with query: '{user_query}'")
    
    # 1. Retrieve the top 2 matching document chunks
    matching_chunks = vector_db.similarity_search(user_query, k=2)
    
    if not matching_chunks:
        logger.warning("No matching document chunks found in vector database.")
        return "क्षमा करें, यह जानकारी इस दस्तावेज़ में उपलब्ध नहीं है।"
        
    context_text = "\n\n".join([chunk.page_content for chunk in matching_chunks])
    logger.info(f"Retrieved {len(matching_chunks)} chunks from ChromaDB.")

    # 2. Step One: The Researcher (DeepSeek R1)
    # Analyzes context and extracts strict legal facts.
    logger.info("--- Phase 1: Running DeepSeek-R1 (Researcher) ---")
    deepseek_prompt = (
        "You are a precise legal researcher.\n"
        "Read the context below and extract the exact legal facts, requirements, and section numbers related to the user's query.\n"
        "Do NOT use outside knowledge. Do NOT simplify language yet. Just extract the facts.\n"
        "If the answer is not in the context, output: 'NOT_FOUND'.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Query: {user_query}"
    )
    
    try:
        research_response = ollama.chat(
            model='deepseek-r1:1.5b',
            messages=[{'role': 'user', 'content': deepseek_prompt}],
            options={
                "temperature": 0.0,
                "keep_alive": 0  # Unload immediately to preserve device memory (Jetson Nano/local CPU)
            }
        )
        extracted_facts = research_response['message']['content'].strip()
    except Exception as deepseek_error:
        logger.error(f"DeepSeek-R1 failed, falling back to direct context extraction: {deepseek_error}")
        extracted_facts = context_text  # Fallback to direct context if DeepSeek is missing

    if "NOT_FOUND" in extracted_facts:
        return "क्षमा करें, यह जानकारी इस दस्तावेज़ में उपलब्ध नहीं है।"

    # 3. Step Two: The Communicator (Qwen 2.5)
    # Translates and simplifies the extracted facts into easy Hindi.
    logger.info("--- Phase 2: Running Qwen 2.5 (Communicator) ---")
    qwen_prompt = (
        "आप एक कानूनी सहायक हैं जो ग्रामीण लोगों को आसान भाषा में समझाते हैं।\n"
        "नीचे दिए गए 'Legal Facts' को बहुत ही सरल, स्पष्ट और संवादात्मक हिंदी (Devanagari) में समझाएं।\n"
        "यदि कोई धारा (Section) है, तो उसका उल्लेख करें लेकिन आसान शब्दों में।\n"
        "अपनी तरफ से कोई नई कानूनी जानकारी न जोड़ें।\n\n"
        f"Legal Facts:\n{extracted_facts}"
    )

    try:
        final_response = ollama.chat(
            model='qwen2.5:1.5b',
            messages=[
                {'role': 'system', 'content': 'आप एक मददगार और सरल भाषा में बोलने वाले कानूनी सहायक हैं।'},
                {'role': 'user', 'content': qwen_prompt}
            ],
            options={
                "temperature": 0.1,
                "repeat_penalty": 1.2,
                "top_k": 10,
                "top_p": 0.1,
                "keep_alive": 0
            }
        )
        return final_response['message']['content'].strip()
    except Exception as qwen_error:
        logger.error(f"Failed to communicate with Qwen 2.5 Communicator: {qwen_error}")
        return (
            "क्षमा करें, वर्तमान में हमारे ऑफलाइन भाषा मॉडल (LLM) सर्वर से कनेक्शन नहीं हो पा रहा है। "
            "कृपया सुनिश्चित करें कि Ollama पृष्ठभूमि में चल रहा है और 'qwen2.5:1.5b' तथा 'deepseek-r1:1.5b' मॉडल इंस्टॉल हैं।"
        )