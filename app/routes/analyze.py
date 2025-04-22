# app/routes/analyze.py

from fastapi import APIRouter, Query
from app.agents.fundamentals_agent import run_fundamentals_agent
from app.agents.technical_agent import run_technical_agent
from app.agents.risk_agent import run_risk_agent
from app.agents.llm_coordinator import generate_final_report
from app.services.stock_data import fetch_stock_summary, fetch_latest_news

router = APIRouter()

@router.get("/analyze")
def analyze_stock(ticker: str = Query(...), generateReport: bool = Query(False)):
    try:
        # Step 1: Basic data
        summary = fetch_stock_summary(ticker)
        news = fetch_latest_news(ticker)

        # Step 2: Agents fetch insights
        fundamentals = run_fundamentals_agent(ticker)
        technicals = run_technical_agent(ticker)
        risks = run_risk_agent(ticker)

        # Step 3: Optional: Generate final analyst report
        final_report = None
        if generateReport:
            final_report = generate_final_report(summary, fundamentals, technicals, risks, news)

        return {
            "ticker": ticker,
            "summary": summary,
            "news": news,
            "fundamentals": fundamentals,
            "technicals": technicals,
            "risks": risks,
            "report": final_report
        }

    except Exception as e:
        return {"error": str(e)}
