from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from app.services.gemini_engine import gemini_chat
import os

def run_risk_analysis(ticker: str, persist_path="chroma_store") -> dict:
    embedding = MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=os.getenv("MISTRALAI_API_KEY")
    )

    vectordb = Chroma(
        persist_directory=persist_path,
        embedding_function=embedding
    )

    query = (
        "Extract key business risks, uncertainties, or red flags mentioned in the SEC filings. "
        "Focus on risk disclosures such as geopolitical risks, supply chain, regulatory pressure, or litigation."
    )

    docs = vectordb.similarity_search(query, k=15)  # You can filter by form_type if needed

    combined_context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an investment research analyst specializing in risk disclosures.

Given the following excerpts from SEC filings for {ticker}, identify and summarize the most material risks facing the company.

Include risks such as:
- Geopolitical instability
- Supply chain disruption
- Regulatory investigations
- Market concentration or key customer loss
- Ongoing or potential litigation

Use professional tone and return a 150-word risk analysis.

--- FILINGS CONTEXT ---
{combined_context}
"""

    ai_summary = gemini_chat(prompt)

    return {
        "ticker": ticker.upper(),
        "risk_summary": ai_summary,
        "source_chunks": len(docs)
    }
