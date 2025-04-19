from app.rag.loaders.edgar_loader import fetch_filing_text
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRALAI_API_KEY")

def ingest_filing(ticker: str, form_type: str, persist_path="chroma_store"):
    text = fetch_filing_text(ticker, form_type=form_type)
    print("✅ Filing text loaded (first 500 chars):\n", text[:500])
    if not text:
        print(f"No {form_type} found for {ticker}")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])

    # Add metadata for filtering
    for d in docs:
        d.metadata["form_type"] = form_type
        d.metadata["ticker"] = ticker.upper()

    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_path
    )

    vectordb.persist()
    print(f"✅ Ingested {form_type} for {ticker} — {len(docs)} chunks")

if __name__ == "__main__":
    for form in ["10-K", "10-Q", "8-K", "DEF 14A"]:
        ingest_filing("AMD", form)
