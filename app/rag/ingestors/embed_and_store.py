#!/usr/bin/env python3

# app/rag/ingestors/simple_embed.py

import os
import shutil
from tqdm import tqdm
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
from app.rag.loaders.edgar_loader import fetch_filing_text
import re
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict

# Load environment variables
load_dotenv()

# Set up storage path in the project directory
CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "chroma_store")

# Ensure the directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

# Set up the embedding function with memory optimization
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    device="cpu",  # Force CPU usage to save memory
    normalize_embeddings=True
)

def clean_filing_text(filing_text):
    """Clean the raw filing text to prepare it for embedding."""
    # Remove HTML/XML tags and clean the text
    filing_text = re.sub(r'<[^>]+>', '', filing_text)  # Remove HTML/XML tags
    filing_text = re.sub(r'&[^;]+;', ' ', filing_text)  # Remove HTML entities
    filing_text = re.sub(r'style="[^"]*"', '', filing_text)  # Remove style attributes
    filing_text = re.sub(r'class="[^"]*"', '', filing_text)  # Remove class attributes
    
    # Remove repeated patterns and special characters
    filing_text = re.sub(r'\([\s\(]+M\([\s\(]+\)', ' ', filing_text)  # Remove repeated patterns
    filing_text = re.sub(r'[^\w\s.,;:!?()-]', ' ', filing_text)  # Keep only alphanumeric and basic punctuation
    filing_text = re.sub(r'\s+', ' ', filing_text)  # Normalize whitespace
    filing_text = filing_text.strip()
    
    # Additional cleaning for SEC-specific content
    filing_text = re.sub(r'xbrl\.sec\.gov.*?(?=\s|$)', '', filing_text)  # Remove XBRL references
    filing_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', filing_text)  # Remove URLs
    filing_text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', '', filing_text)  # Remove email addresses
    
    # Remove garbled content (sequences of special characters and numbers)
    filing_text = re.sub(r'[A-Z0-9]{5,}', ' ', filing_text)  # Remove long sequences of caps and numbers
    filing_text = re.sub(r'[^A-Za-z0-9\s.,;:!?()-]{3,}', ' ', filing_text)  # Remove sequences of special chars
    
    # Final cleanup
    filing_text = re.sub(r'\s+', ' ', filing_text)  # Normalize whitespace again
    filing_text = filing_text.strip()
    
    return filing_text

def ingest_filing(ticker: str, filing_type: str, start_date: datetime, end_date: datetime, reset_collection: bool = False):
    """Ingest an SEC filing for a given ticker and form type."""
    print(f"\n📡 Fetching {filing_type} for {ticker.upper()}")
    
    # Format collection name to meet ChromaDB requirements
    collection_name = f"sec-{ticker.lower()}-{filing_type.lower().replace(' ', '-')}"
    
    # Step 1: Create ChromaDB client with memory optimization
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=chromadb.Settings(
            anonymized_telemetry=False,
            allow_reset=True,
            is_persistent=True
        )
    )
    
    # Step 2: Delete collection if reset is requested
    if reset_collection:
        try:
            client.delete_collection(collection_name)
            print(f"Collection {collection_name} deleted.")
        except Exception as e:
            print(f"Error deleting collection (may not exist): {e}")
            
    # Step 3: Create or get collection
    try:
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={"source": f"{ticker}-{filing_type}"}
        )
        print(f"Collection ready: {collection_name}")
    except Exception as e:
        print(f"❌ Error with collection: {str(e)}")
        try:
            # Try to delete and recreate
            client.delete_collection(collection_name)
            collection = client.create_collection(
                name=collection_name,
                embedding_function=embedding_function,
                metadata={"source": f"{ticker}-{filing_type}"}
            )
            print(f"Collection recreated: {collection_name}")
        except Exception as e2:
            print(f"❌ Critical error: {str(e2)}")
            return False
    
    # Step 4: Fetch and clean filing text
    try:
        filing_text = fetch_filing_text(ticker.upper(), form_type=filing_type)
        if not filing_text or not filing_text.strip():
            print(f"❌ No text retrieved for {filing_type} of {ticker}")
            return False
            
        # Clean the text
        filing_text = clean_filing_text(filing_text)
        
        # Skip if the text is too short or contains mostly special characters
        if len(filing_text) < 100 or len(re.sub(r'[^A-Za-z]', '', filing_text)) < 50:
            print(f"❌ Text too short or contains too many special characters after cleaning")
            return False
    except Exception as e:
        print(f"❌ Error fetching or cleaning text: {str(e)}")
        return False
    
    # Step 5: Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([filing_text])
    
    # Step 6: Add documents to collection in batches
    batch_size = 20
    success_count = 0
    
    # Create batches for processing
    for i in tqdm(range(0, len(docs), batch_size), desc=f"Ingesting {filing_type}"):
        batch = docs[i:i + batch_size]
        
        ids = []
        texts = []
        metadatas = []
        
        # Process each document in the batch
        for j, doc in enumerate(batch):
            doc_id = f"{ticker}-{filing_type}-{i+j}"
            text = doc.page_content.strip()
            
            # Skip invalid content
            if not text or len(text) < 20:
                continue
                
            # Truncate long text
            text = text[:3000]  # Keep tokens within limits
            
            # Add to batch lists
            ids.append(doc_id)
            texts.append(text)
            metadatas.append({
                "source": f"{ticker}-{filing_type}",
                "chunk_index": i+j,
                "length": len(text)
            })
        
        # Skip empty batches
        if not ids:
            print(f"⚠️ Skipped batch {i}: all chunks were empty or invalid")
            continue
            
        # Debug info
        print(f"\n Debug - Batch {i}:")
        print(f"Documents: {len(ids)}")
        print(f"First document length: {len(texts[0])}")
        print(f"First document start: {texts[0][:100]}")
        
        # Add to collection
        try:
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            success_count += len(ids)
        except Exception as e:
            print(f"❌ Failed adding batch {i}: {str(e)}")
            
    print(f"✅ Ingested {success_count} chunks from {ticker} {filing_type}")
    return True

def main():
    """Process filings for specified tickers and forms."""
    # Reset Chroma collections before beginning
    forms = ["10-K", "10-Q", "8-K", "DEF 14A"]
    tickers = ["AMD"]
    
    # Set date range for filings
    start_date = datetime(2020, 1, 1)  # Start from January 1, 2020
    end_date = datetime.now()  # End at current date
    
    for ticker in tickers:
        for form in forms:
            try:
                success = ingest_filing(ticker, filing_type=form, start_date=start_date, end_date=end_date, reset_collection=True)
                if success:
                    print(f"✅ Successfully ingested {form} for {ticker}")
                else:
                    print(f"❌ Failed to ingest {form} for {ticker}")
            except Exception as e:
                print(f"❌ Error processing {form} for {ticker}: {str(e)}")
    
    print("\n🎉 Processing complete!")

if __name__ == "__main__":
    main() 