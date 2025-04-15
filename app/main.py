from fastapi import FastAPI
from app.routes import analyze

app = FastAPI(
    title="Autonomous Investment Research Analyst",
    description="AI-powered research assistant for stock analysis",
    version="0.1"
)

app.include_router(analyze.router, prefix="/analyze")
