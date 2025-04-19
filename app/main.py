import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze
from app.routes import sec_rag
from app.routes import full_report 

app = FastAPI(
    title="Autonomous Investment Research Analyst",
    description="AI-powered research assistant for stock analysis",
    version="0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-research-analyst.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(analyze.router, prefix="/analyze")
app.include_router(sec_rag.router, prefix="/sec-rag")
app.include_router(full_report.router, prefix="/full-report") 