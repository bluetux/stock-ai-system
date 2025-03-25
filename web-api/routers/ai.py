# 📌 파일 위치: stock-dashboard-api/routers/ai.py

from fastapi import APIRouter

router = APIRouter(prefix="/api/ai", tags=["AI Predictions"])

@router.get("/predictions/{ticker}")
async def get_ai_prediction(ticker: str):
    return {"ticker": ticker, "predicted_price": 160.0}
