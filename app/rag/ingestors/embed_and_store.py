from app.rag.loaders.edgar_loader import fetch_10k_text
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv("MISTRALAI_API_KEY")

def ingest_ticker(ticker: str, persist_path="chroma_store"):
    start_time = time.time()
    print(f"\n📥 Starting ingestion for {ticker}...")
    
    # Pull 10-K document from EDGAR
    print("📄 Fetching 10-K document...")
    fetch_start = time.time()
    raw_text = fetch_10k_text(ticker)
    if not raw_text:
        print(f"❌ Failed to fetch 10-K for {ticker}")
        return False
    print(f"✅ Fetched {len(raw_text)} characters in {time.time() - fetch_start:.2f}s")
    
    # Chunk the document
    print("✂️ Splitting document into chunks...")
    split_start = time.time()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = splitter.create_documents([raw_text])
    print(f"✅ Split into {len(docs)} chunks in {time.time() - split_start:.2f}s")
    
    # Embed using Mistral
    print("🔢 Generating embeddings...")
    embed_start = time.time()
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=api_key
    )
    
    # Store in Chroma
    print("💾 Storing in vector database...")
    store_start = time.time()
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_path,
        collection_name=ticker.lower()  # Ensure consistent case
    )
    vectordb.persist()
    print(f"✅ Stored in {time.time() - store_start:.2f}s")
    
    total_time = time.time() - start_time
    print(f"✨ Completed ingestion in {total_time:.2f}s")
    return True

if __name__ == "__main__":
    ticker = "AMD"
    ingest_ticker(ticker)
