# app/services/stock_data.py

import yfinance as yf
import requests

def fetch_stock_summary(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "symbol": ticker.upper(),
        "shortName": info.get("shortName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "marketCap": info.get("marketCap", "N/A"),
        "summary": info.get("longBusinessSummary", "N/A")
    }


def fetch_latest_news(ticker: str) -> list:
    # Yahoo Finance News RSS feed
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

    try:
        import feedparser
    except ImportError:
        raise ImportError("Please install feedparser to fetch latest news: pip install feedparser")

    feed = feedparser.parse(url)
    news_items = []

    for entry in feed.entries[:5]:
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "")
        })

    return news_items
