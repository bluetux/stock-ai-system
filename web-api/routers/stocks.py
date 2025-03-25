# 📁 web-api/routers/stocks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/stocks", tags=["Stocks"])

@router.get("/{ticker}")
def get_stock(ticker: str, db=Depends(get_db)):
    query = text("""
    SELECT
        w.ticker, w.alias, w.region, w.is_open, w.icon,
        d.close_price AS price,
        d.open_price AS open,
        d.high_price AS high,
        d.low_price AS low,
        d.volume,
        d.exchange_rate 
    FROM watchlist w
    LEFT JOIN stock_daily_data d ON w.ticker = d.ticker
    WHERE w.ticker = :ticker
    ORDER BY d.price_date DESC
    LIMIT 1
    """)
    result = db.execute(query, {"ticker": ticker}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Stock not found")
    return result
