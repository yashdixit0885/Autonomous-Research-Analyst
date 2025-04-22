# app/rag/retrievers/qa_rag_runner.py
import time
from functools import lru_cache
import asyncio
from typing import Optional
import concurrent.futures

from app.services.gemini_engine import gemini_chat
from app.rag.store.chroma_utils import load_vectorstore

DEFAULT_QUESTION = "Summarize the key findings from this company's SEC filings."
CACHE_SIZE = 100  # Number of vectorstores to cache
TIMEOUT_SECONDS = 15  # Reduced timeout
MAX_CONTEXT_LENGTH = 4000  # Maximum context length for Gemini
SIMILARITY_THRESHOLD = 0.9  # Increased from 0.8 to 0.9

@lru_cache(maxsize=CACHE_SIZE)
def get_cached_vectorstore(ticker: str):
    """Cache the vectorstore to avoid repeated disk reads"""
    return load_vectorstore(ticker)

def query_vectorstore(
    ticker: str, 
    question: str = DEFAULT_QUESTION, 
    k: int = 3,  # Reduced from 4 to 3
    timeout: int = TIMEOUT_SECONDS
) -> str:
    """
    Query the Chroma vectorstore for the given ticker and question,
    and use Gemini to generate a contextual answer.
    """
    try:
        # Load the vectorstore from cache
        start_time = time.time()
        vectordb = get_cached_vectorstore(ticker)
        print(f"[{ticker}] Loaded vectorstore in {time.time() - start_time:.2f}s")

        # Search for relevant context with score threshold
        start_time = time.time()
        docs = vectordb.similarity_search_with_score(question, k=k)
        print(f"[{ticker}] Retrieved top {len(docs)} docs in {time.time() - start_time:.2f}s")

        if not docs:
            return "No relevant context found in the filings."

        # Print similarity scores for debugging
        print(f"[{ticker}] Similarity scores:")
        for i, (doc, score) in enumerate(docs):
            print(f"  Doc {i+1}: {score:.4f}")

        # Filter documents by score and build context
        context_chunks = []
        total_length = 0
        
        for doc, score in docs:
            if score < SIMILARITY_THRESHOLD:  # Only include highly relevant chunks
                content = doc.page_content.strip()
                if len(content) > 100:  # Basic relevance threshold
                    if total_length + len(content) <= MAX_CONTEXT_LENGTH:
                        context_chunks.append(content)
                        total_length += len(content)
                    else:
                        break

        if not context_chunks:
            return "No sufficiently relevant context found in the filings."

        context = "\n\n".join(context_chunks)

        # Compose Gemini prompt
        prompt = f"""
You are a professional financial analyst. Use the following context extracted from the company's SEC filings to answer the user's question.

--- Context from SEC Filings ---
{context}

--- Question ---
{question}

Provide a clear, concise answer grounded in the context. If the context doesn't contain enough information to answer the question, say so.
        """

        # Make Gemini API call with timeout
        start_time = time.time()
        try:
            # Run Gemini in a separate thread to handle timeout
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(gemini_chat, prompt)
                result = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            return "The request timed out. Please try again with a more specific question."
            
        print(f"[{ticker}] Gemini responded in {time.time() - start_time:.2f}s")
        return result

    except Exception as e:
        print(f"❌ Error in query_vectorstore: {str(e)}")
        return f"An error occurred while processing your question: {str(e)}"
