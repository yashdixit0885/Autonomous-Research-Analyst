from fastapi import APIRouter, Query
from app.services.stock_data import fetch_stock_summary

router = APIRouter()

@router.get("/")
async def analyze_stock(ticker: str = Query(..., description="Stock ticker symbol")):
    result = await fetch_stock_summary(ticker)
    return result
