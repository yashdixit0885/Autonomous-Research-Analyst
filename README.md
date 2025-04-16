# 🧠 Autonomous Investment Research Analyst

An AI-powered stock research assistant that mimics a Wall Street analyst — built with FastAPI, Gemini LLM, and a stylish React + Tailwind frontend.

---

## ✨ Features

- 🔍 **Search any stock ticker** (e.g., AAPL, TSLA, NVDA)
- 📊 **Company fundamentals + technical analysis**
- 📰 **Recent news headlines**
- 🤖 **AI-generated investment research report** (Buy / Hold / Sell)
- 🧾 **Downloadable AI report**
- 🌗 **Dark/Light mode toggle**
- 🌀 **Animated loading states**
- 🎨 Fully styled with Tailwind CSS v3

---

## 🧪 Technologies Used

| Layer      | Tech                     |
|------------|--------------------------|
| Frontend   | React + Tailwind + Vite  |
| Backend    | FastAPI (Python)         |
| LLM        | Gemini `gemini-1.5-pro`  |
| Data APIs  | yFinance, Finnhub        |

---

## 🖥️ How to Run Locally

### 🧩 Backend (FastAPI)

cd backend-folder
pip install -r requirements.txt
uvicorn app.main:app --reload

Make sure .env contains:
GEMINI_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here

### 💻 Frontend (React + Tailwind):
cd investment-analyst-frontend
npm install
npm run dev
Visit: http://localhost:5173

## 📬 Feedback Welcome!
This is an early MVP — open to feedback, suggestions, and contributors.

## 📄 License
MIT