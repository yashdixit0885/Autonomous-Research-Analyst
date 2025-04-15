import yfinance as yf
import talib as ta
import numpy as np

async def fetch_stock_summary(ticker: str):
    try:
        stock = yf.Ticker(ticker)

        # Fetch general info
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

        # Pull last 6 months of price data
        hist = stock.history(period="6mo")
        close_prices = hist["Close"].values
        
        # Add technical indicators
        hist["RSI"] = ta.RSI(close_prices, timeperiod=14)
        macd, signal, _ = ta.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
        hist["MACD"] = macd
        hist["Signal"] = signal
        hist["MA50"] = ta.SMA(close_prices, timeperiod=50)
        hist["MA200"] = ta.SMA(close_prices, timeperiod=200)

        latest = hist.iloc[-1]

        technicals = {
            "RSI": round(float(latest["RSI"]), 2) if not np.isnan(latest["RSI"]) else None,
            "MACD": round(float(latest["MACD"]), 2) if not np.isnan(latest["MACD"]) else None,
            "MACD_Signal": round(float(latest["Signal"]), 2) if not np.isnan(latest["Signal"]) else None,
            "50_MA": round(float(latest["MA50"]), 2) if not np.isnan(latest["MA50"]) else None,
            "200_MA": round(float(latest["MA200"]), 2) if not np.isnan(latest["MA200"]) else None,
            "Volume": int(latest["Volume"]),
            "AvgVolume50": int(hist["Volume"].rolling(50).mean().iloc[-1])
        }
        
        trend = "Bullish" if latest["MA50"] > latest["MA200"] else "Bearish"
        technicals["Trend"] = trend
        
        if technicals["RSI"]:
            if technicals["RSI"] > 70:
                technicals["RSI_Signal"] = "Overbought"
            elif technicals["RSI"] < 30:
                technicals["RSI_Signal"] = "Oversold"
            else:
                technicals["RSI_Signal"] = "Neutral"



        return {
            "summary": summary,
            "technicals": technicals
        }

    except Exception as e:
        return {"error": str(e)}
