import yfinance as yf
from app.services.gemini_engine import gemini_chat


def get_llm_summary(metrics: dict) -> str:
    prompt = f"""
You are a professional equity research analyst.

Given the following financial metrics for a company:

{metrics}

Write a concise 100–150 word summary evaluating the company's:
- Valuation (e.g., PE, PB, EPS)
- Profitability (e.g., ROE, ROA, margins)
- Financial health (e.g., debt levels, interest coverage)
- Growth trends (e.g., revenue growth)

Interpret the data like you're writing a professional investment research note. Do not repeat the raw numbers — provide meaning and insight.
"""
    return gemini_chat(prompt)


def fetch_fundamentals_ai(ticker: str) -> dict:
    stock = yf.Ticker(ticker)

    try:
        info = stock.info
        financials = stock.financials
    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}

    metrics = {
        "EPS": info.get("trailingEps"),
        "PE_Ratio": info.get("trailingPE"),
        "PB_Ratio": info.get("priceToBook"),
        "ROE": info.get("returnOnEquity"),
        "ROA": info.get("returnOnAssets"),
        "Debt_to_Equity": info.get("debtToEquity"),
        "Operating_Margin": info.get("operatingMargins"),
    }

    # Revenue growth (YoY)
    try:
        revenue_now = info.get("totalRevenue")
        revenue_1y_ago = financials.loc["Total Revenue"].values[1]
        metrics["Revenue_Growth_YoY"] = (revenue_now - revenue_1y_ago) / revenue_1y_ago
    except:
        metrics["Revenue_Growth_YoY"] = None

    # Interest Coverage = EBIT / Interest Expense
    try:
        ebit = financials.loc["Ebit"].values[0]
        interest_expense = financials.loc["Interest Expense"].values[0]
        metrics["Interest_Coverage"] = ebit / abs(interest_expense)
    except:
        metrics["Interest_Coverage"] = None

    # Round cleanly
    rounded_metrics = {k: round(v, 4) if isinstance(v, (int, float)) else v for k, v in metrics.items()}

    # LLM interpretation (Gemini summary)
    ai_summary = get_llm_summary(rounded_metrics)

    return {
        "ticker": ticker.upper(),
        "metrics": rounded_metrics,
        "ai_summary": ai_summary
    }
