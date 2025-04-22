# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analyze, full_report, sec_rag

app = FastAPI(
    title="Autonomous Investment Research Analyst",
    description="AI-powered financial research tool for analyzing company fundamentals, technicals, filings, and risks.",
    version="1.0.0"
)

# Allow frontend (local + deployed)
origins = [
    "http://localhost:5173",
    "https://ai-research-analyst.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routes
app.include_router(analyze.router)
app.include_router(full_report.router, prefix="/full-report")
app.include_router(sec_rag.router, prefix="/sec-rag")

@app.get("/")
def root():
    return {"message": "Autonomous Investment Research Analyst API is running!"}
