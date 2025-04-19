from app.services.fundamentals_agent import fetch_fundamentals_ai
from app.services.technical_agent import fetch_technical_analysis
from app.services.risk_agent import run_risk_analysis
from app.services.gemini_engine import gemini_chat

def generate_analyst_report(ticker: str) -> dict:
    # Fetch all agent outputs
    fundamentals = fetch_fundamentals_ai(ticker)
    technicals = fetch_technical_analysis(ticker)
    risk = run_risk_analysis(ticker)

    # Analyst report excerpt for stylistic reference
    analyst_report_excerpt = """
Company Overview
Founded in 1969, AMD is one of the largest suppliers of microprocessors and graphics processors worldwide to computing OEMs. AMD designs and sells CPUs and GPUs for desktops, notebooks and gaming consoles, as well as for datacenter and professional environments. AMD's key product families include Ryzen processors for personal computers, Radeon processors for graphics and EPYC processors for servers.

Investment Overview
Gaining share in a growing market. AMD sees a USD 400bn data centre accelerator TAM on the back of increasing adoption of artificial intelligence (AI) and the pervasiveness of AI across industries which necessitates significant investment in new infrastructure. AMD’s updated roadmap includes the MI325X accelerator in 4Q24, MI350 series in 2025, and MI400 series in 2026. In addition, AMD has a strong track record of innovation, design agility and proven execution and has been gaining market share from Intel in the server and client segment given the growing demand of its 4th Gen EPYC processors and Ryzen 8000 series.
"""

    # Combine into one prompt
    prompt = f"""
You are a Wall Street investment research analyst.

Use the following analyst report excerpt as a stylistic reference:
--- ANALYST REPORT EXCERPT ---
{analyst_report_excerpt}

Now, write a professional 4-part research report for {ticker} based on the following agent outputs:

--- FUNDAMENTALS ---
Metrics:
{fundamentals['metrics']}

Summary:
{fundamentals['ai_summary']}

--- TECHNICAL ANALYSIS ---
Metrics:
{technicals['metrics']}

Summary:
{technicals['ai_summary']}

--- RISK FACTORS ---
{risk['risk_summary']}

--- FINAL OUTPUT ---
Write a full-length report (400-500 words) structured like a professional equity analyst note:
1. Company Summary
2. Valuation and Financial Performance
3. Technical Momentum and Market Sentiment
4. Risks and Uncertainties
5. Final Rating: Buy / Hold / Sell — with rationale
Use a confident, institutional tone (think Morgan Stanley, JPMorgan, Goldman Sachs).
"""

    report = gemini_chat(prompt)

    return {
        "ticker": ticker.upper(),
        "report": report
    }