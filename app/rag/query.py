#!/usr/bin/env python3

import os
import sys
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CHROMA_PATH = "chroma_store"

# Set up the embedding function - must match what was used for ingestion
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def get_collections():
    """Get list of available collections"""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.list_collections()

def query_collection(collection_name, query_text, n_results=5):
    """Query a specific collection by name"""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    try:
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
    except Exception as e:
        print(f"Error accessing collection {collection_name}: {e}")
        return None
    
    # Execute the query
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    return results

def list_all_collections():
    """Print all available collections"""
    collections = get_collections()
    print(f"\n📚 Available Collections ({len(collections)}):")
    for idx, collection in enumerate(collections, 1):
        try:
            client = chromadb.PersistentClient(path=CHROMA_PATH)
            coll = client.get_collection(
                name=collection,
                embedding_function=embedding_function
            )
            count = coll.count()
            print(f"{idx}. {collection} ({count} documents)")
        except Exception as e:
            print(f"{idx}. {collection} (Error: {e})")

def search_all_collections(query_text, n_results=3):
    """Search across all collections"""
    collections = get_collections()
    all_results = {}
    
    print(f"\n🔎 Searching all collections for: '{query_text}'")
    
    for collection_name in collections:
        try:
            results = query_collection(collection_name, query_text, n_results)
            if results and results["documents"] and results["documents"][0]:
                all_results[collection_name] = results
        except Exception as e:
            print(f"Error querying {collection_name}: {e}")
    
    return all_results

def print_results(results_dict, max_length=300):
    """Print the search results in a readable format"""
    if not results_dict:
        print("No results found.")
        return
    
    for collection_name, results in results_dict.items():
        print(f"\n📄 Results from {collection_name}:")
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
            # Truncate long documents for display
            if len(doc) > max_length:
                display_doc = doc[:max_length] + "..."
            else:
                display_doc = doc
                
            # Print result with metadata
            print(f"\n--- Result {i} (Score: {1-dist:.4f}) ---")
            print(f"Metadata: {meta}")
            print(f"Content: {display_doc}")
            print("-" * 40)

def main():
    """Main function to handle CLI arguments"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python query.py list                # List all collections")
        print("  python query.py search 'query text' # Search all collections")
        print("  python query.py search 'query text' --collection=collection_name # Search specific collection")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_all_collections()
    
    elif command == "search" and len(sys.argv) >= 3:
        query_text = sys.argv[2]
        
        # Check if a specific collection is specified
        collection_name = None
        n_results = 5
        
        for arg in sys.argv[3:]:
            if arg.startswith("--collection="):
                collection_name = arg.split("=")[1]
            elif arg.startswith("--results="):
                try:
                    n_results = int(arg.split("=")[1])
                except ValueError:
                    pass
        
        if collection_name:
            results = query_collection(collection_name, query_text, n_results)
            if results:
                print_results({collection_name: results})
            else:
                print(f"No results found in collection {collection_name}.")
        else:
            results_dict = search_all_collections(query_text, n_results)
            print_results(results_dict)
    
    else:
        print("Invalid command. Use 'list' or 'search'.")

if __name__ == "__main__":
    main() 