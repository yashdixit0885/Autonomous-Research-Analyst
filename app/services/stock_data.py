import yfinance as yf

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
        return summary
    except Exception as e:
        return {"error": str(e)}
