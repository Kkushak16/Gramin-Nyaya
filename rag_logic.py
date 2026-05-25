"""
Gramin-Nyaya: AI Legal Assistant (Core RAG Engine)
==================================================
Orchestrates the offline Retrieval-Augmented Generation (RAG) pipeline.
It handles indexing the Hindi Registration Act PDF into ChromaDB via HuggingFace
multilingual sentence embeddings, and retrieves precise context to feed into the local LLM.

Optimizations:
- Persistent vector store checks to prevent costly CPU re-embeddings on restart.
- Structured, transparent execution logs.

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
# Designed to map Hindi/Devanagari queries to appropriate statutory sections
logger.info("Initializing HuggingFace Multilingual-MiniLM embedding engine...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# --- Persistent Vector Database Loading ---
# If the vector store already exists on disk, we load it directly. 
# This avoids re-embedding the entire PDF on every script restart.
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
    Given a user's question, searches the database for relevant sections
    of the Registration Act and queries the offline Qwen model to synthesize
    a highly precise, hallucination-free response in Hindi.
    """
    logger.info(f"Querying RAG system: '{user_query}'")
    
    # 1. Retrieve the top 2 matching document chunks
    matching_chunks = vector_db.similarity_search(user_query, k=2)
    
    if not matching_chunks:
        logger.warning("No matching document chunks found in vector database.")
        return "क्षमा करें, यह जानकारी इस दस्तावेज़ में उपलब्ध नहीं है।"
        
    context_text = "\n\n".join([chunk.page_content for chunk in matching_chunks])
    logger.info(f"Retrieved {len(matching_chunks)} contextual chunks from ChromaDB.")

    # 2. Strict system prompt forcing grounding and preventing hallucination
    system_instruction = (
        "आप एक विधिक सहायक (Legal Assistant) हैं। केवल दिए गए Context का उपयोग करके "
        "जवाब दें। यदि उत्तर Context में नहीं है, तो सटीक शब्दों में कहें "
        "'क्षमा करें, यह जानकारी इस दस्तावेज़ में उपलब्ध नहीं है।'\n\n"
        f"Context:\n{context_text}"
    )

    try:
        # 3. Request reasoning response from Qwen 2.5 local model via Ollama
        logger.info("Sending query to local Qwen 2.5 LLM...")
        llm_response = ollama.chat(
            model='qwen2.5:1.5b',
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': user_query}
            ],
            options={
                "temperature": 0.0,      # Strict outputs
                "repeat_penalty": 1.3,   # Prevent infinite repetition loops
                "top_k": 10,             # Keep focus on high probability terms
                "top_p": 0.1,            # High threshold confidence selection
                "num_predict": 150       # Concise guidance
            }
        )
        
        reply_content = llm_response['message']['content'].strip()
        logger.info("Model response synthesized successfully.")
        return reply_content

    except Exception as ollama_error:
        logger.error(f"Failed to communicate with local Ollama engine: {ollama_error}")
        
        # Friendly offline legal fallback response
        return (
            "क्षमा करें, वर्तमान में हमारे ऑफलाइन भाषा मॉडल (LLM) सर्वर से कनेक्शन नहीं हो पा रहा है। "
            "कृपया सुनिश्चित करें कि Ollama पृष्ठभूमि में चल रहा है और 'qwen2.5:1.5b' मॉडल इंस्टॉल है।"
        )