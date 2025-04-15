import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def build_prompt(summary, technicals, news):
    news_block = "\n".join(
        [f"{i+1}. \"{n['headline']}\" - {n['source']} - {n['datetime']}" for i, n in enumerate(news)]
    )

    prompt = f"""
You're an investment research analyst. Based on the following data, write a professional 3-paragraph report including a Buy/Hold/Sell recommendation.

--- COMPANY FUNDAMENTALS ---
Symbol: {summary['symbol']}
Sector: {summary.get('sector')}
Industry: {summary.get('industry')}
Current Price: {summary.get('currentPrice')}
Market Cap: {summary.get('marketCap')}
Trailing P/E: {summary.get('trailingPE')}
Forward P/E: {summary.get('forwardPE')}
Return on Equity: {summary.get('returnOnEquity')}
Debt to Equity: {summary.get('debtToEquity')}

--- TECHNICAL ANALYSIS ---
RSI: {technicals.get('RSI')}
MACD: {technicals.get('MACD')}
MACD Signal: {technicals.get('MACD_Signal')}
50-day MA: {technicals.get('50_MA')}
200-day MA: {technicals.get('200_MA')}
Volume: {technicals.get('Volume')}
Avg Volume (50d): {technicals.get('AvgVolume50')}

--- NEWS HEADLINES ---
{news_block}

Now write a research note in natural language including your rating.
"""
    return prompt

def generate_gemini_report(summary, technicals, news):
    prompt = build_prompt(summary, technicals, news)
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
