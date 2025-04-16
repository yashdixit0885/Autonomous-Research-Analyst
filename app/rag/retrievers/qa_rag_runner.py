from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_mistralai import MistralAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Set up retriever
embedding = MistralAIEmbeddings(
    model="mistral-embed",
    mistral_api_key=os.getenv("MISTRALAI_API_KEY")
)

vectordb = Chroma(
    persist_directory="chroma_store",
    embedding_function=embedding
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
