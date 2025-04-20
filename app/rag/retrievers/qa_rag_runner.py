from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Set up retriever
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"batch_size": 32, "normalize_embeddings": True}
)

vectordb = Chroma(
    persist_directory="chroma_store",
    embedding_function=embedding_model
)

retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# Option 1: Use Gemini (commented)
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

# Option 2: Use Mistral LLM


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Prompt Template
template = """
You are a financial research analyst. Use the following SEC filing context to answer the question truthfully and professionally.

Context:
{context}

Question:
{question}

Answer as if writing to an investor:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# Setup RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# Test query
if __name__ == "__main__":
    question = "What are the major risk factors AMD listed in their 10-K?"
    result = qa_chain.run(question)
    print("\n📘 RAG Answer:")
    print(result)
