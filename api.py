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
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rag_logic import ask_gramin_nyaya
import os
import json
from datetime import datetime
import stt_service

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

class ConsultationRequest(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=10)
    desc: str = Field(..., min_length=3)

@app.post("/consultation")
async def handle_consultation(request: ConsultationRequest):
    logger.info(f"New consultation callback request received for name: {request.name}")
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "name": request.name,
            "phone": request.phone,
            "description": request.desc
        }
        
        file_path = "consultations.json"
        
        consultations = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    consultations = json.load(f)
            except Exception as read_err:
                logger.error(f"Error reading consultations.json, resetting: {read_err}")
                consultations = []
                
        consultations.append(data)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(consultations, f, ensure_ascii=False, indent=4)
            
        logger.info("Successfully persisted consultation request.")
        return {
            "success": True,
            "message": "Consultation request submitted successfully."
        }
    except Exception as e:
        logger.error(f"Failed to record consultation request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save request. Please try again.")

@app.post("/transcribe")
async def handle_transcription(file: UploadFile = File(...)):
    logger.info("New audio file received for transcription.")
    temp_filename = "uploaded_voice.wav"
    try:
        content = await file.read()
        with open(temp_filename, "wb") as f:
            f.write(content)
            
        logger.info(f"Successfully saved temp audio file. Proceeding with Whisper inference.")
        
        transcribed_text = stt_service.record_and_transcribe(file_path=temp_filename)
        
        logger.info(f"Transcription completed: '{transcribed_text}'")
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        return {
            "text": transcribed_text,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error during audio transcription: {e}", exc_info=True)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))


# --- Bootloader ---
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Gramin-Nyaya offline FastAPI gateway on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)