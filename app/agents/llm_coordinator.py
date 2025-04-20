from app.services.gemini_engine import gemini_chat

def generate_final_report(fundamentals_analysis: str, technical_analysis: str, risk_analysis: str):
    prompt = f"""
You are a Wall Street analyst. Write a full research report for {ticker} using the following:

--- Fundamentals ---
{fundamentals_analysis}

--- Technical Analysis ---
{technical_analysis}

--- Risk Disclosures ---
{risk_analysis}

Structure it like a professional report with clear insights, concise explanations, and a Buy/Hold/Sell recommendation at the end.
"""
    return gemini_chat(prompt)

