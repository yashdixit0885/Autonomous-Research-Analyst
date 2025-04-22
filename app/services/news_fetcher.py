# app/services/news_fetcher.py

import yfinance as yf

def fetch_news(ticker: str, limit: int = 5):
    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news[:limit]
        cleaned_news = []

        for item in news_items:
            cleaned_news.append({
                "headline": item.get("title", "No title"),
                "source": item.get("publisher", "Unknown"),
                "datetime": item.get("providerPublishTime", ""),
                "link": item.get("link", "#")
            })

        return cleaned_news

    except Exception as e:
        print(f"❌ Error fetching news for {ticker}:", e)
        return []
