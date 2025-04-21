import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_store"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Memory optimization settings
MEMORY_OPTIMIZATION = {
    "embedding_batch_size": 32,
    "max_documents_per_query": 3,
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "max_response_length": 500,
    "use_cpu": True,
    "normalize_embeddings": True
}

# ChromaDB settings
CHROMA_SETTINGS = {
    "anonymized_telemetry": False,
    "allow_reset": True,
    "is_persistent": True
}

# Model settings
MODEL_SETTINGS = {
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "device": "cpu" if MEMORY_OPTIMIZATION["use_cpu"] else "auto"
} 