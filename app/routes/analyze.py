# 1. analyze.py
from fastapi import APIRouter, Query
from app.agents.fundamentals_agent import run_fundamentals_agent
from app.agents.technical_agent import run_technical_agent
from app.agents.risk_agent import run_risk_agent
from app.agents.llm_coordinator import generate_final_report

router = APIRouter()

@router.get("/analyze")
def analyze(ticker: str = Query(...), generateReport: bool = Query(False)):
    fundamentals = run_fundamentals_agent(ticker)
    technicals = run_technical_agent(ticker)
    risks = run_risk_agent(ticker)

    final_report = generate_final_report(fundamentals['ai_summary'], technicals['ai_summary'], risks['risk_summary']) if generateReport else ""

    return {
        "ticker": ticker,
        "fundamentals": fundamentals,
        "technicals": technicals,
        "risks": risks,
        "report": final_report
    }