"""
Gramin-Nyaya: AI Legal Assistant (FastAPI Server)
=================================================
This server acts as the local API gateway for the rural digital judicial system.
Designed to run 100% offline via local LLM orchestration (Ollama) to ensure
absolute data privacy and confidentiality for rural users.

Author: DEI Engineering Team (Human-Centric Design)
Year: 2024
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rag_logic import ask_gramin_nyaya

# --- Setup Logging Infrastructure ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger("GraminNyayaAPI")

app = FastAPI(
    title="Gramin-Nyaya API",
    description="Offline-first privacy-preserving legal assistant gateway for Indian rural populations.",
    version="2.0.4"
)

# --- Enable Cross-Origin Resource Sharing (CORS) ---
# Allows the clean, single-page kiosk interface (index.html) to interact with
# the FastAPI backend seamlessly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Data Models ---
class QueryRequest(BaseModel):
    """
    Structured model to handle secure user input text queries.
    """
    question: str = Field(
        ..., 
        description="The legal query typed or spoken by the user in Hindi/English.",
        min_length=3
    )

# --- Endpoints ---
@app.get("/")
async def health_check():
    """
    System diagnostic endpoint to confirm the API gateway is fully operational.
    """
    logger.info("Health check endpoint accessed.")
    return {
        "status": "online",
        "service": "Gramin-Nyaya Backend Gateway",
        "version": "2.0.4"
    }

@app.post("/ask")
async def handle_query(request: QueryRequest):
    """
    Main reasoning entry point. Accepts the user's query, fetches relevant
    offline contextual knowledge from the vector store, feeds it to the local
    LLM pipeline, and returns the simplified legal guidance.
    """
    user_query = request.question.strip()
    logger.info(f"Processing new user query: '{user_query}'")

    try:
        # Pass query to the local RAG orchestrator (offline)
        simplified_advice = ask_gramin_nyaya(user_query)
        
        logger.info("Successfully generated grounded legal advice.")
        return {
            "query": user_query,
            "answer": simplified_advice,
            "success": True
        }
    except Exception as error_context:
        logger.error(f"Error encountered during RAG query reasoning: {error_context}", exc_info=True)
        
        # Humanised fallback error response in Hindi for a smooth user experience
        raise HTTPException(
            status_code=500,
            detail="विधिक परामर्श सेवा में तकनीकी समस्या आ रही है। कृपया सुनिश्चित करें कि Ollama स्थानीय रूप से चल रहा है।"
        )

# --- Bootloader ---
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Gramin-Nyaya offline FastAPI gateway on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)