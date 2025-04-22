# app/agents/technical_agent.py

import yfinance as yf
import numpy as np

def fetch_technical_indicators(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    if hist.empty:
        raise ValueError(f"No historical data found for {ticker}")

    close = hist["Close"]
    ma50 = close.rolling(window=50).mean().iloc[-1]
    ma200 = close.rolling(window=200).mean().iloc[-1]
    rsi = compute_rsi(close)

    return {
        "MA50": safe_float(ma50),
        "MA200": safe_float(ma200),
        "RSI": safe_float(rsi),
        "latest_close": safe_float(close.iloc[-1]),
    }

def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def summarize_technicals(metrics: dict) -> str:
    return (
        f"Latest Close: ${metrics['latest_close']:.2f}\n"
        f"50-day MA: ${metrics['MA50']:.2f}, 200-day MA: ${metrics['MA200']:.2f}\n"
        f"RSI: {metrics['RSI']:.2f} ({interpret_rsi(metrics['RSI'])})"
    )

def interpret_rsi(rsi):
    if rsi >= 70:
        return "Overbought"
    elif rsi <= 30:
        return "Oversold"
    return "Neutral"

def safe_float(value):
    try:
        f = float(value)
        if np.isnan(f) or np.isinf(f):
            return 0.0
        return f
    except:
        return 0.0

def run_technical_agent(ticker: str):
    metrics = fetch_technical_indicators(ticker)
    ai_summary = summarize_technicals(metrics)
    return {"metrics": metrics, "ai_summary": ai_summary}

