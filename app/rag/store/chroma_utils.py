# app/rag/store/chroma_utils.py

import os
from typing import List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Initialize embedding model with optimized settings
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",  # More suitable for financial text
    model_kwargs={"device": "cpu"},
    encode_kwargs={
        "normalize_embeddings": True,
        "batch_size": 32  # Optimize batch size for better performance
    }
)

def persist_documents(docs: List[Document], ticker: str, form_type: str):
    """Persist documents to Chroma vectorstore"""
    collection_name = f"sec-{ticker.lower()}-{form_type.lower()}"
    persist_directory = "chroma_store"
    
    # Create directory if it doesn't exist
    os.makedirs(persist_directory, exist_ok=True)
    
    # Initialize Chroma with the documents
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )
    
    # Add documents in batches for better performance
    batch_size = 500
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        vectordb.add_documents(batch)
    
    print(f"✅ Ingested and saved {len(docs)} chunks to {persist_directory}/{collection_name}")

def load_vectorstore(ticker: str, form_type: str = "10-K"):
    """Load Chroma vectorstore for a given ticker and form type"""
    collection_name = f"sec-{ticker.lower()}-{form_type.lower()}"
    persist_directory = "chroma_store"
    
    # Initialize Chroma with the existing collection
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )
    
    return vectordb
