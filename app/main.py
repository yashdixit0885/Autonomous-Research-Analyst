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

app = FastAPI(
    title="Autonomous Investment Research Analyst",
    description="AI-powered research assistant for stock analysis",
    version="0.1"
)

# ✅ Add this block to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-research-analyst.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(analyze.router, prefix="/analyze")
app.include_router(sec_rag.router, prefix="/sec-rag")