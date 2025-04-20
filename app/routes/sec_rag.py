# app/routes/sec_rag.py

from fastapi import APIRouter, Query, Body
from rag.ingestors.embed_and_store import ingest_filing
from services.gemini_engine import gemini_chat
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

router = APIRouter()

@router.get("/ask-sec")
def ask_sec_filing(ticker: str = Query(...), question: str = Query(...), filing_type: str = Query("10-K")):
    try:
        # Use the same naming pattern as your ingestion code
        collection_name = f"sec-{ticker.lower()}-{filing_type.lower().replace(' ', '-')}"
        
        # Use the same embedding model as your ingestion code
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Load vector DB with the correct collection name
        vectordb = Chroma(
            collection_name=collection_name,
            persist_directory="chroma_store",
            embedding_function=embedding
        )
        
        # Rest of your code remains the same
        print("Total documents stored:", vectordb._collection.count())

        # Search filings for relevant content
        docs = vectordb.similarity_search(question, k=6)
        context = "\n\n".join(doc.page_content for doc in docs)

        if not context.strip():
            return {
                "ticker": ticker,
                "question": question,
                "answer": {
                    "query": question,
                    "result": "No context retrieved from filings."
                }
            }

        # Build Gemini prompt
        prompt = f"""
You are a professional financial analyst. Use the following context extracted from the company's SEC filings (10-K, 10-Q, 8-K, and Proxy statements) to answer the user's question.

--- SEC Filing Context ---
{context}

--- User Question ---
{question}

Be concise, evidence-based, and clear.
"""

        response = gemini_chat(prompt)

        return {
            "ticker": ticker,
            "question": question,
            "answer": {
                "query": question,
                "result": response
            }
        }

    except Exception as e:
        print("❌ Backend error:", e)
        return {"error": str(e)}


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
