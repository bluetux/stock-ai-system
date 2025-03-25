# 📁 web-api/routers/exchange.py
from fastapi import APIRouter, Depends
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/exchange", tags=["Exchange"])

@router.get("/usd-krw")
def get_latest_usd_krw_rate(db=Depends(get_db)):
    query = text("""
        SELECT close_price
        FROM stock_daily_data
        WHERE ticker = 'USD/KRW'
              AND price_date <= CURRENT_DATE   
        ORDER BY price_date DESC
        LIMIT 1
    """)
    result = db.execute(query).scalar()
    return {"usd_krw": float(result) if result else None}
