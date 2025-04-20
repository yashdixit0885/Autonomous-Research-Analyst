from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import analyze, full_report, sec_rag

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/analyze")
app.include_router(full_report.router, prefix="/full-report")
app.include_router(sec_rag.router, prefix="/sec-rag")

@app.get("/")
def root():
    return {"status": "✅ API is running"}
