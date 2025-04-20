#!/usr/bin/env python3

# app/rag/reset_chroma.py

import os
import shutil
import sys
from datetime import datetime

def reset_chroma_database(path="chroma_store"):
    """
    Completely resets the ChromaDB database by backing up the current one and creating a fresh instance.
    """
    if not os.path.exists(path):
        print(f"No ChromaDB database found at {path}")
        return
    
    # Create backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}_backup_{timestamp}"
    
    print(f"⚠️ Creating backup of current database at: {backup_path}")
    try:
        shutil.copytree(path, backup_path)
        print(f"✅ Backup created successfully")
    except Exception as e:
        print(f"❌ Error creating backup: {str(e)}")
        print("Proceeding without backup...")
    
    # Remove the current database
    print(f"🗑️ Removing current ChromaDB database from: {path}")
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        print(f"✅ Successfully removed database")
    except Exception as e:
        print(f"❌ Error removing database: {str(e)}")
        sys.exit(1)
    
    # Create fresh directory 
    print(f"🆕 Creating fresh ChromaDB directory at: {path}")
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✅ Fresh ChromaDB directory created")
    except Exception as e:
        print(f"❌ Error creating directory: {str(e)}")
        sys.exit(1)
    
    print("\n✨ ChromaDB has been reset successfully!")
    print(f"Your previous database is backed up at: {backup_path}")
    print("\nYou can now run your ingestion scripts to populate the database.")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
        reset_chroma_database(db_path)
    else:
        # Default path
        reset_chroma_database() 