import yfinance as yf
import pandas as pd
from app.services.gemini_engine import gemini_chat

def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(close: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()

    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()

    return macd, signal_line


def get_llm_technical_summary(ticker: str, metrics: dict) -> str:
    prompt = f"""
You are a technical analysis expert.

Given the following technical indicators for {ticker}, write a 100–150 word summary of the stock’s momentum, trend, and trader sentiment.

{metrics}

Focus on interpretation — e.g. is the stock overbought, trending bullish, at a support level, etc. Avoid restating raw values.
"""
    return gemini_chat(prompt)


def fetch_technical_analysis(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    if hist.empty:
        return {"error": "No historical data available."}

    close = hist["Close"]
    volume = hist["Volume"]

    rsi_series = calculate_rsi(close)
    macd_series, signal_series = calculate_macd(close)

    hist["RSI"] = rsi_series
    hist["MACD"] = macd_series
    hist["MACD_Signal"] = signal_series
    hist["MA_50"] = close.rolling(window=50).mean()
    hist["MA_200"] = close.rolling(window=200).mean()
    hist["AvgVolume_50"] = volume.rolling(window=50).mean()

    latest = hist.iloc[-1]

    metrics = {
        "RSI": round(latest["RSI"], 2) if pd.notna(latest["RSI"]) else None,
        "MACD": round(latest["MACD"], 2) if pd.notna(latest["MACD"]) else None,
        "MACD_Signal": round(latest["MACD_Signal"], 2) if pd.notna(latest["MACD_Signal"]) else None,
        "MA_50": round(latest["MA_50"], 2),
        "MA_200": round(latest["MA_200"], 2),
        "Volume": int(latest["Volume"]),
        "AvgVolume_50": int(latest["AvgVolume_50"]),
        "Price": round(latest["Close"], 2)
    }

    summary = get_llm_technical_summary(ticker, metrics)

    return {
        "ticker": ticker.upper(),
        "metrics": metrics,
        "ai_summary": summary
    }
