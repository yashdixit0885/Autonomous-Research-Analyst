# app/agents/risk_agent.py

from app.rag.retrievers.qa_rag_runner import query_vectorstore
from app.services.gemini_engine import gemini_chat

# Define the central question for risk analysis
RISK_QUESTION = "What are the key risk disclosures and red flags mentioned in the company's filings?"

def run_risk_agent(ticker: str) -> dict:
    """
    Agent to retrieve and summarize risks from SEC filings using vectorstore + Gemini LLM.
    """
    try:
        context = query_vectorstore(ticker, RISK_QUESTION, k=10)

        if not context or not context.strip():
            return {
                "risk_summary": "No risk-related information was found in the SEC filings."
            }

        prompt = f"""
You are a professional financial analyst. Based on the following excerpts from SEC filings, identify and summarize the key risk disclosures and red flags mentioned by the company ({ticker}).

--- SEC Filing Excerpts ---
{context}

Structure the response clearly with headings or bullet points. Be concise, specific, and highlight any sections explicitly labeled as "Risk Factors".
        """

        response = gemini_chat(prompt)
        return {
            "risk_summary": response.strip()
        }

    except Exception as e:
        return {
            "risk_summary": f"❌ Failed to extract risks due to error: {str(e)}"
        }
