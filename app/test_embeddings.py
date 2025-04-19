from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from app.rag.loaders.edgar_loader import fetch_filing_text
import os
from dotenv import load_dotenv

load_dotenv()

ticker = "AMD"
form = "10-K"
persist_path = f"chroma_store/{ticker.upper()}"

# Load raw text
text = fetch_filing_text(ticker, form_type=form)
print("✅ Loaded filing length:", len(text))

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.create_documents([text])
print("✅ Total chunks created:", len(docs))

# Init embeddings
embedding = MistralAIEmbeddings(
    model="mistral-embed",
    mistral_api_key=os.getenv("MISTRALAI_API_KEY")
)

# Create vector store
vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=persist_path)
vectordb.persist()
print(f"✅ Ingested and saved {len(docs)} chunks to {persist_path}")
