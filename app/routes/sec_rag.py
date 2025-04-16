from fastapi import APIRouter, Query, HTTPException
from app.rag.loaders.edgar_loader import fetch_10k_text
from app.rag.ingestors.embed_and_store import ingest_ticker
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_mistralai import MistralAIEmbeddings
import os
import time

router = APIRouter()

@router.get("/ask-sec")
def ask_sec_filing(
    ticker: str = Query(...),
    question: str = Query(...),
):
    try:
        start_time = time.time()
        print(f"\n🔄 Starting request for {ticker} - {question}")
        
        # Ensure the vector store exists
        persist_path = f"chroma_store/{ticker.lower()}"
        if not os.path.exists(persist_path):
            print(f"🔍 No existing vector store found for {ticker}, ingesting...")
            ingest_start = time.time()
            if not ingest_ticker(ticker, persist_path):
                raise HTTPException(status_code=404, detail=f"Failed to ingest documents for {ticker}")
            print(f"⏱️ Ingestion took {time.time() - ingest_start:.2f} seconds")

        print("🔍 Loading vector store...")
        # Load store
        embedding = MistralAIEmbeddings(
            model="mistral-embed",
            mistral_api_key=os.getenv("MISTRALAI_API_KEY")
        )

        vectordb = Chroma(
            persist_directory=persist_path,
            collection_name=ticker.lower(),
            embedding_function=embedding
        )

        print("🔍 Performing similarity search...")
        # First try direct similarity search
        docs = vectordb.similarity_search(question, k=3)
        print(f"\n🔎 Vector search returned {len(docs)} results.")
        if not docs:
            raise HTTPException(status_code=404, detail="No relevant documents found")

        print("🔍 Setting up retriever...")
        # Set up retriever with more context
        retriever = vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        print("🔍 Retrieving relevant documents...")
        # Get relevant documents
        docs = retriever.get_relevant_documents(question)
        print(f"\n🔎 Retrieved {len(docs)} documents:")
        for i, doc in enumerate(docs[:3]):
            print(f"\n--- Document {i+1} ---\n{doc.page_content[:500]}")

        print("🤖 Setting up Gemini model...")
        # Set up Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        prompt = PromptTemplate.from_template("""
You are a financial analyst reading a company's SEC 10-K filing. Based on the following context, answer the question:

{context}

Question: {question}

Answer professionally and cite specific numbers or facts from the context when possible:
""")

        print("🤖 Generating answer...")
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt}
        )

        answer = qa.invoke({"query": question})
        print(f"✅ Request completed in {time.time() - start_time:.2f} seconds")

        return {
            "ticker": ticker,
            "question": question,
            "answer": answer,
            "num_docs_retrieved": len(docs)
        }

    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
