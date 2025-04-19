from fastapi import APIRouter, Query
from langchain_community.vectorstores import Chroma
from app.services.gemini_engine import gemini_chat
from langchain_mistralai import MistralAIEmbeddings
from fastapi import Body
from app.rag.ingestors.embed_and_store import ingest_filing
import os
from chromadb.config import Settings as ClientSettings
router = APIRouter()

@router.get("/ask-sec")
def ask_sec_filing(ticker: str = Query(...), question: str = Query(...)):
    try:
        persist_path = f"chroma_store/{ticker.upper()}"

        # Load Mistral embedding function
        embedding = MistralAIEmbeddings(
            model="mistral-embed",
            mistral_api_key=os.getenv("MISTRALAI_API_KEY")
        )

        # Load vector DB with the embedding function
        vectordb = Chroma(
            persist_directory=persist_path,
            embedding_function=embedding,
                client_settings=ClientSettings(
                persist_directory=persist_path,
                chroma_db_impl="duckdb+parquet",
                anonymized_telemetry=False,
                num_threads=1
            )
        )
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
