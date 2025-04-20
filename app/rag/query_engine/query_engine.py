from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.services.gemini_engine import gemini_chat
import os

def query_filings(ticker: str, query: str, filing_type: str = "10-K"):
    """Query SEC filings for a given ticker and question."""
    try:
        # Use the same naming pattern as your ingestion code
        collection_name = f"sec-{ticker.lower()}-{filing_type.lower().replace(' ', '-')}"
        
        # Use the same embedding model as your ingestion code
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Load vector DB with the correct collection name
        vectordb = Chroma(
            collection_name=collection_name,
            persist_directory="data/chroma_store",
            embedding_function=embedding
        )
        
        # Search filings for relevant content
        docs = vectordb.similarity_search(query, k=6)
        context = "\n\n".join(doc.page_content for doc in docs)

        if not context.strip():
            return "No relevant information found in the filings."

        # Build Gemini prompt
        prompt = f"""
You are a professional financial analyst. Use the following context extracted from the company's SEC filings to answer the user's question.

--- SEC Filing Context ---
{context}

--- User Question ---
{query}

Be concise, evidence-based, and clear.
"""

        response = gemini_chat(prompt)
        return response

    except Exception as e:
        print("❌ Error querying filings:", e)
        return str(e) 