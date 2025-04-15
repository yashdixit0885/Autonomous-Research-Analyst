import os
from dotenv import load_dotenv
import httpx
from datetime import datetime, timedelta

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

async def fetch_news(ticker: str):
    try:
        # Set date range (last 7 days)
        to_date = datetime.now().date()
        from_date = to_date - timedelta(days=7)

        url = f"https://finnhub.io/api/v1/company-news"
        params = {
            "symbol": ticker.upper(),
            "from": from_date.isoformat(),
            "to": to_date.isoformat(),
            "token": FINNHUB_API_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            # Return top 5 recent news items
            news = []
            for item in data[:5]:
                news.append({
                    "headline": item["headline"],
                    "source": item["source"],
                    "datetime": datetime.fromtimestamp(item["datetime"]).strftime("%Y-%m-%d %H:%M"),
                    "url": item["url"]
                })

            return news

    except Exception as e:
        return [{"error": str(e)}]
