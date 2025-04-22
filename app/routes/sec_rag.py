# app/routes/sec_rag.py

from fastapi import APIRouter, Query, Body
from app.rag.ingestors.embed_and_store import ingest_filing
from app.rag.retrievers.qa_rag_runner import query_vectorstore

router = APIRouter()

@router.get("/ask-sec")
def ask_sec_filing(
    ticker: str = Query(..., description="Stock ticker symbol"),
    question: str = Query(..., description="Natural language question to ask")
):
    try:
        result = query_vectorstore(ticker, question)

        return {
            "ticker": ticker,
            "question": question,
            "answer": {
                "query": question,
                "result": result
            }
        }
    except Exception as e:
        print("❌ Error in ask-sec route:", str(e))
        return {
            "ticker": ticker,
            "question": question,
            "answer": {
                "query": question,
                "result": "An error occurred while processing the question."
            },
            "error": str(e)
        }

@router.post("/ingest")
def ingest_on_demand(
    ticker: str = Body(...),
    form: str = Body(default="10-K")
):
    try:
        ingest_filing(ticker.upper(), form_type=form)
        return {"status": "success", "message": f"{ticker} - {form} ingested"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
