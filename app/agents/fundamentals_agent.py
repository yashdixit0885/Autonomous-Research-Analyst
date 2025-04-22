# app/agents/fundamentals_agent.py

import yfinance as yf
import math

def sanitize(value):
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return "N/A"
    return value

KEY_METRICS = [
    "currentPrice", "marketCap", "trailingPE", "forwardPE", "priceToBook",
    "returnOnEquity", "debtToEquity", "grossMargins", "profitMargins",
    "revenueGrowth", "earningsGrowth", "operatingMargins"
]

def fetch_fundamentals(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    metrics = {key: sanitize(info.get(key, "N/A")) for key in KEY_METRICS}

    summary = f"Fundamentals for {ticker}:\n"
    if isinstance(metrics.get("marketCap"), int):
        summary += f"- Market Cap: ${metrics['marketCap']:,}\n"
    if isinstance(metrics.get("trailingPE"), float):
        summary += f"- Trailing P/E: {metrics['trailingPE']}\n"
    if isinstance(metrics.get("forwardPE"), float):
        summary += f"- Forward P/E: {metrics['forwardPE']}\n"
    if isinstance(metrics.get("returnOnEquity"), float):
        summary += f"- ROE: {metrics['returnOnEquity'] * 100:.2f}%\n"
    if isinstance(metrics.get("debtToEquity"), float):
        summary += f"- Debt/Equity: {metrics['debtToEquity']:.2f}\n"

    return {
        "metrics": metrics,
        "ai_summary": summary.strip()
    }

def run_fundamentals_agent(ticker: str):
    return fetch_fundamentals(ticker)
