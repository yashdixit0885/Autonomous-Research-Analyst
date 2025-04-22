# app/agents/llm_coordinator.py

from app.agents.fundamentals_agent import run_fundamentals_agent
from app.agents.technical_agent import run_technical_agent
from app.agents.risk_agent import run_risk_agent
from app.services.gemini_engine import gemini_chat


def generate_final_report(ticker: str, fundamentals: dict, technicals: dict, risks: dict, news: list) -> dict:
    prompt = f"""
You are a Wall Street analyst. Given the following data for {ticker}, write a professional-quality investment report.

📊 Fundamentals:
{fundamentals['ai_summary']}

📈 Technicals:
{technicals['ai_summary']}

⚠️ Risks:
{risks['risk_summary']}

📰 Latest News:
{news[0] if news else "No recent news available."}

Format this report professionally with clear sections and use an analyst-style tone.
    """

    final_report = gemini_chat(prompt)

    return {
        "ticker": ticker,
        "fundamentals": fundamentals,
        "technicals": technicals,
        "risks": risks,
        "news": news,
        "report": final_report
    }
