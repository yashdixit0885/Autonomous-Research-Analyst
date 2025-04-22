# app/routes/full_report.py

from fastapi import APIRouter, Query
from app.agents.fundamentals_agent import run_fundamentals_agent
from app.agents.technical_agent import run_technical_agent
from app.agents.risk_agent import run_risk_agent
from app.agents.llm_coordinator import generate_final_report


router = APIRouter()

@router.get("/generate-full-report")
def generate_full_report(ticker: str = Query(...)):
    try:
        fundamentals = run_fundamentals_agent(ticker)
        technicals = run_technical_agent(ticker)
        risks = run_risk_agent(ticker)

        # Final LLM report using all the above insights
        report = generate_final_report(ticker)

        return {
            "ticker": ticker.upper(),
            "fundamentals": fundamentals,
            "technicals": technicals,
            "risks": risks,
            "report": report,
        }

    except Exception as e:
        return {"error": str(e)}
