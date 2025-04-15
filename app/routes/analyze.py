from fastapi import APIRouter, Query
from app.services.stock_data import fetch_stock_summary
from app.services.news_fetcher import fetch_news
from app.services.gemini_engine import generate_gemini_report

router = APIRouter()

@router.get("/")
async def analyze_stock(
    ticker: str = Query(..., description="Stock ticker symbol"),
    generateReport: bool = Query(False, description="Generate Gemini AI Report")
):
    summary_result = await fetch_stock_summary(ticker)
    news_result = await fetch_news(ticker)

    result = {
        **summary_result,
        "news": news_result
    }

    if generateReport and "summary" in summary_result and "technicals" in summary_result:
        try:
            report = generate_gemini_report(
                summary_result["summary"],
                summary_result["technicals"],
                news_result
            )
            result["gemini_report"] = report
        except Exception as e:
            result["gemini_report"] = f"Error generating report: {e}"

    return result
