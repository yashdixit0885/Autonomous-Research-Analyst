import yfinance as yf
import numpy as np
import pandas as pd

async def fetch_stock_summary(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        summary = {
            "symbol": ticker.upper(),
            "longName": info.get("longName"),
            "currentPrice": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "returnOnEquity": info.get("returnOnEquity"),
            "debtToEquity": info.get("debtToEquity"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
        }

        hist = stock.history(period="6mo")

        # Calculate MA50, MA200
        hist["MA50"] = hist["Close"].rolling(50).mean()
        hist["MA200"] = hist["Close"].rolling(200).mean()

        # Calculate RSI
        delta = hist["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        hist["RSI"] = 100 - (100 / (1 + rs))

        # Calculate MACD
        ema12 = hist["Close"].ewm(span=12, adjust=False).mean()
        ema26 = hist["Close"].ewm(span=26, adjust=False).mean()
        hist["MACD"] = ema12 - ema26
        hist["Signal"] = hist["MACD"].ewm(span=9, adjust=False).mean()

        latest = hist.iloc[-1]

        technicals = {
            "RSI": round(latest["RSI"], 2) if not np.isnan(latest["RSI"]) else None,
            "MACD": round(latest["MACD"], 2) if not np.isnan(latest["MACD"]) else None,
            "MACD_Signal": round(latest["Signal"], 2) if not np.isnan(latest["Signal"]) else None,
            "50_MA": round(latest["MA50"], 2) if not np.isnan(latest["MA50"]) else None,
            "200_MA": round(latest["MA200"], 2) if not np.isnan(latest["MA200"]) else None,
            "Volume": int(latest["Volume"]),
            "AvgVolume50": int(hist["Volume"].rolling(50).mean().iloc[-1])
        }

        return {
            "summary": summary,
            "technicals": technicals
        }

    except Exception as e:
        return {"error": str(e)}
