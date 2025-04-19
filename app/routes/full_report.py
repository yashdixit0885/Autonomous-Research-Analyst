from fastapi import APIRouter
from app.services.fundamentals_agent import fetch_fundamentals_ai
from app.services.technical_agent import fetch_technical_analysis
from app.services.risk_agent import run_risk_analysis
from app.services.llm_coordinator import generate_analyst_report
from app.utils.helpers import sanitize_for_json  # (create this if needed)

router = APIRouter()

@router.get("/generate-full-report")
def generate_full_report(ticker: str):
    fundamentals = fetch_fundamentals_ai(ticker)
    technicals = fetch_technical_analysis(ticker)
    risks = run_risk_analysis(ticker)
    report = generate_analyst_report(ticker)

    # Sanitize all before sending as JSON
    response = {
        "ticker": ticker,
        "fundamentals": fundamentals,
        "technicals": technicals,
        "risks": risks,
        "report": report["report"]
    }

    return sanitize_for_json(response)
