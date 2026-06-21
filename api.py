import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_logic import ask_gramin_nyaya

app = FastAPI(title="Gramin Nyaya API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict this to the frontend origin in production.
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
async def handle_query(request: QueryRequest):
    logger.info("User asked: %s", request.question)

    try:
        answer = ask_gramin_nyaya(request.question)
        return {"answer": answer}
    except Exception as exc:
        logger.error("Error processing query: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Sorry, we encountered an error while processing your legal query.",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
