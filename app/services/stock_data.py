import yfinance as yf

def fetch_stock_summary(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "symbol": info.get("symbol"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "returnOnEquity": info.get("returnOnEquity"),
        "debtToEquity": info.get("debtToEquity")
    }
