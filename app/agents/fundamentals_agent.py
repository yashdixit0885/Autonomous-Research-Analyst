from app.services.stock_data import fetch_stock_summary
from app.services.gemini_engine import gemini_chat

def run_fundamentals_agent(ticker: str):
    metrics = fetch_stock_summary(ticker)

    prompt = f"""
You are a finance analyst. Summarize the following company's key fundamental metrics:

Symbol: {metrics['symbol']}
Market Cap: {metrics['marketCap']}
PE Ratio: {metrics['trailingPE']}
Forward PE: {metrics['forwardPE']}
ROE: {metrics['returnOnEquity']}
Debt/Equity: {metrics['debtToEquity']}

Provide a professional summary of the company's fundamentals.
"""
    summary = gemini_chat(prompt)
    return {
        "metrics": metrics,
        "ai_summary": summary
    }

