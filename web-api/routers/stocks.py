# 📁 web-api/routers/stocks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd
import numpy as np

from db import get_db

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """기술적 지표 계산"""
    try:
        # Ensure price column is numeric
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Calculate indicators only if we have enough data
        if len(df) >= 20:
            # Moving averages
            df['MA5'] = df['price'].rolling(window=5).mean().round(2)
            df['MA20'] = df['price'].rolling(window=20).mean().round(2)
            
            # Bollinger Bands
            df['MA20'] = df['price'].rolling(window=20).mean()
            rolling_std = df['price'].rolling(window=20).std()
            df['Upper_Band'] = (df['MA20'] + (rolling_std * 2)).round(2)
            df['Lower_Band'] = (df['MA20'] - (rolling_std * 2)).round(2)
            
            # Handle any infinite values
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.ffill().bfill()
        
        return df
    except Exception as e:
        print(f"Error in calculate_technical_indicators: {str(e)}")
        return df

@router.get("/{ticker}")
def get_stock(ticker: str, db: Session = Depends(get_db)):
    """종목 기본 정보 조회"""
    query = text("""
    SELECT 
        w.ticker, w.alias, w.region, w.is_active, w.icon,
        d.close_price as price,
        d.open_price as open,
        d.high_price as high,
        d.low_price as low,
        d.volume,
        d.exchange_rate,
        CASE 
            WHEN w.region = '한국' THEN 
                CASE 
                    WHEN EXTRACT(DOW FROM CURRENT_TIMESTAMP) IN (0, 6) THEN false
                    WHEN CURRENT_TIME BETWEEN '09:00' AND '15:30' THEN true
                    ELSE false
                END
            WHEN w.region = '미국' THEN 
                CASE 
                    WHEN EXTRACT(DOW FROM CURRENT_TIMESTAMP) IN (0, 6) THEN false
                    WHEN CURRENT_TIME BETWEEN '22:30' AND '05:00' THEN true
                    ELSE false
                END
            ELSE false
        END as is_open
    FROM watchlist w
    LEFT JOIN stock_daily_data d ON w.ticker = d.ticker
    WHERE w.ticker = :ticker
    ORDER BY d.price_date DESC
    LIMIT 1
    """)
    
    result = db.execute(query, {"ticker": ticker}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
    return result

@router.get("/{ticker}/history")
def get_stock_history(
    ticker: str,
    period: str = "1D",
    db: Session = Depends(get_db)
):
    """기간별 주가 데이터 조회"""
    try:
        if period == "1D":
            query = text("""
                SELECT
                    created_at as timestamp,
                    price
                FROM stock_prices
                WHERE ticker = :ticker
                AND created_at >= :start_time
                ORDER BY created_at
            """)
            
            start_time = datetime.now() - timedelta(days=1)
            result = db.execute(query, {"ticker": ticker, "start_time": start_time})
            rows = result.fetchall()
            
            # Convert to list of dicts and add volume=0 for 1D data
            data = [{"timestamp": row[0], "price": float(row[1]), "volume": 0} for row in rows]
        else:
            if period == "7D":
                start_time = datetime.now() - timedelta(days=7)
            elif period == "1M":
                start_time = datetime.now() - timedelta(days=30)
            elif period == "1Y":
                start_time = datetime.now() - timedelta(days=365)
            else:  # All
                start_time = datetime(2000, 1, 1)
            
            query = text("""
                SELECT 
                    price_date as timestamp,
                    open_price as open,
                    high_price as high,
                    low_price as low,
                    close_price as close,
                    close_price as price,
                    COALESCE(volume, 0) as volume
                FROM stock_daily_data
                WHERE ticker = :ticker
                AND price_date >= :start_time
                ORDER BY price_date
            """)

            # 주가 데이터 조회
            result = db.execute(query, {
                "ticker": ticker,
                "start_time": start_time
            }).mappings().all()
            
            # DataFrame 생성 및 기술적 지표 계산
            if result:
                data = [{
                    "timestamp": row['timestamp'],
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close']),
                    "price": float(row['price']),
                    "volume": float(row['volume'])
                } for row in result]
            else:
                data = []
        
        if not data:
            return {"error": "No data found"}

        # Calculate technical indicators
        df = pd.DataFrame(data)
        df = calculate_technical_indicators(df)
        
        # Handle infinite values and ensure JSON compatibility
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.ffill().bfill()
        
        # Round numeric columns to prevent floating point precision issues
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].round(2)
        
        # AI 예측 데이터 조회 (있는 경우)
        pred_query = text("""
            SELECT 
                created_at as timestamp,
                predicted_price
            FROM ai_predictions
            WHERE ticker = :ticker
            AND created_at >= :start_time
            ORDER BY created_at
        """)
        
        predictions = db.execute(pred_query, {
            "ticker": ticker,
            "start_time": start_time
        }).mappings().all()
        
        if predictions:
            pred_df = pd.DataFrame(predictions)
            df = pd.merge(df, pred_df, on='timestamp', how='left')
            df['predicted_price'] = df['predicted_price'].round(2)
        
        return df.to_dict('records')
    except Exception as e:
        print(f"Error in get_stock_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
def search_stocks(
    query: str,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """종목 검색"""
    search = f"%{query}%"
    sql_query = """
        SELECT ticker, alias, region, icon
        FROM watchlist
        WHERE (ticker ILIKE :search OR alias ILIKE :search)
    """
    
    if region:
        sql_query += " AND region = :region"
    
    result = db.execute(
        text(sql_query),
        {"search": search, "region": region}
    ).mappings().all()
    
    return list(result)
