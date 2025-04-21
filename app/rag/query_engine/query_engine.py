from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.services.gemini_engine import gemini_chat
import os
from functools import lru_cache

# Cache embeddings to avoid reloading
@lru_cache(maxsize=1)
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"batch_size": 32, "normalize_embeddings": True}
    )

def query_filings(ticker: str, query: str, filing_type: str = "10-K"):
    """Query SEC filings for a given ticker and question."""
    try:
        # Use the same naming pattern as your ingestion code
        collection_name = f"sec-{ticker.lower()}-{filing_type.lower().replace(' ', '-')}"
        
        # Get cached embedding model
        embedding = get_embedding_model()
        
        # Load vector DB with the correct collection name
        vectordb = Chroma(
            collection_name=collection_name,
            persist_directory="data/chroma_store",
            embedding_function=embedding
        )
        
        # Search filings for relevant content with reduced k value
        docs = vectordb.similarity_search(query, k=3)  # Reduced from 6 to 3
        context = "\n\n".join(doc.page_content for doc in docs)

        if not context.strip():
            return "No relevant information found in the filings."

        # Build Gemini prompt with memory optimization
        prompt = f"""
You are a professional financial analyst. Use the following context extracted from the company's SEC filings to answer the user's question.

--- SEC Filing Context ---
{context}

--- User Question ---
{query}

Be concise, evidence-based, and clear. Limit your response to 500 words.
"""

        response = gemini_chat(prompt)
        return response

    except Exception as e:
        print("❌ Error querying filings:", e)
        return str(e) 