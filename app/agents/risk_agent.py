from app.services.gemini_engine import gemini_chat
from app.services.stock_data import fetch_stock_summary

def run_risk_agent(ticker: str):
    try:
        with open(f"chroma_store/{ticker}-10-K.txt", "r") as f:
            filing_text = f.read()
    except FileNotFoundError:
        return {"risk_summary": "No 10-K available for risk analysis."}

    prompt = f"""
You're an expert in financial risk. Summarize major risk factors from the following SEC 10-K text:

{filing_text[:5000]}  # Avoid token overflow

Be specific, concise, and bullet out the top risks.
"""
    return {"risk_summary": gemini_chat(prompt)}
