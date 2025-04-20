from services.gemini_engine import gemini_chat

def generate_final_report(ticker, fundamentals, technicals, risks):
    prompt = f"""
You are a Wall Street analyst. Write a full research report for {ticker} using the following:

--- Fundamentals ---
{fundamentals['ai_summary']}

--- Technical Analysis ---
{technicals['ai_summary']}

--- Risk Disclosures ---
{risks['risk_summary']}

Structure it like a professional report with clear insights, concise explanations, and a Buy/Hold/Sell recommendation at the end.
"""
    return gemini_chat(prompt)

