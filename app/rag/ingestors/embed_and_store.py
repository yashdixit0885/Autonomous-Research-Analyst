# app/rag/ingestors/embed_and_store.py

import os
from tqdm import tqdm
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.rag.loaders.edgar_loader import fetch_filing_text
from app.rag.store.chroma_utils import persist_documents

# Load environment variables
load_dotenv()


def ingest_filing(ticker: str, form_type: str = "10-K"):
    ticker = ticker.upper()
    print(f"📡 Fetching {form_type} for {ticker}")

    try:
        filing_text = fetch_filing_text(ticker, form_type)
    except Exception as e:
        print(f"❌ Skipped {form_type} for {ticker} due to error: {e}")
        return

    if not filing_text or len(filing_text.strip()) == 0:
        print(f"⚠️ No content found in {form_type} filing for {ticker}")
        return

    # Optimized chunking parameters for better performance
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Increased chunk size
        chunk_overlap=200,  # Increased overlap for better context
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", " "],  # Better sentence splitting
        is_separator_regex=False
    )
    
    docs = splitter.create_documents([filing_text])
    print(f"✂️ Split into {len(docs)} chunks")

    # Filter out very short chunks
    docs = [doc for doc in docs if len(doc.page_content.strip()) > 100]
    print(f"📊 Filtered to {len(docs)} meaningful chunks")

    persist_documents(docs, ticker, form_type)


if __name__ == "__main__":
    for form in ["10-K", "10-Q", "8-K", "DEF 14A"]:
        ingest_filing("AMD", form_type=form)
