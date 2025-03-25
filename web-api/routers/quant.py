# 📌 파일: routers/quant.py

from fastapi import APIRouter

router = APIRouter(prefix="/api/quant", tags=["Quant"])

@router.get("/analysis/{ticker}")
async def get_quant_analysis(ticker: str):
    return {"ticker": ticker, "quant_score": 92}
