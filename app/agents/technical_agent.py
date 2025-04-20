import yfinance as yf
from services.gemini_engine import gemini_chat

def run_technical_agent(ticker: str):
    data = yf.download(ticker, period="6mo")

    # Sample metrics
    rsi = data["Close"].pct_change().rolling(14).std().iloc[-1] * 100
    ma50 = data["Close"].rolling(50).mean().iloc[-1]
    ma200 = data["Close"].rolling(200).mean().iloc[-1]

    prompt = f"""
You are a technical analysis expert. Analyze the following:

RSI: {rsi:.2f}
50-day MA: {ma50:.2f}
200-day MA: {ma200:.2f}

Explain the stock's short and long-term trend based on these indicators.
"""
    analysis = gemini_chat(prompt)
    return {
        "metrics": {
            "RSI": round(rsi, 2),
            "50_MA": round(ma50, 2),
            "200_MA": round(ma200, 2)
        },
        "ai_summary": analysis
    }

