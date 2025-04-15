# 🧠 Autonomous Investment Research Analyst

An AI-powered backend API that mimics a Wall Street research analyst.  
It retrieves live stock data, performs basic analysis, and will soon generate professional research reports using LLMs.

---

## 🚀 Features (MVP)
- 📊 Pulls stock fundamentals via Yahoo Finance
- 🧪 Technical indicators (coming next)
- 🗞️ Company news summaries (coming soon)
- 🧠 Gemini LLM-powered research generation (coming soon)

---

## 📦 Project Structure

autonomous-research-analyst/
│
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── routes/
│   │   └── analyze.py       # Route for /analyze endpoint
│   ├── services/
│   │   └── stock_data.py    # Logic for pulling stock data (fundamentals, technicals)
│   └── utils/
│       └── helpers.py       # Reusable helper functions
│
├── .env                     # For API keys and secrets
├── requirements.txt         # Python dependencies
├── README.md
├── .gitignore

---

## 🧪 How to Run

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
Visit: http://localhost:8000/analyze?ticker=AAPL

🌐 Deployment
Coming soon — this backend will connect to a React frontend and eventually host Gemini-powered reports.

📘 License
MIT - Use freely, improve openly.
