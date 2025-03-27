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
        # 5분봉 데이터 (stock_prices 테이블)
        if period == "5min":
            try:
                # 먼저 데이터가 있는지 확인
                check_query = text("""
                    SELECT COUNT(*) as cnt
                    FROM stock_prices
                    WHERE ticker = :ticker
                    AND created_at >= :start_time
                """)
                
                start_time = datetime.now() - timedelta(hours=8)
                print(f"Checking data for ticker={ticker}, start_time={start_time}")
                
                count = db.execute(check_query, {
                    "ticker": ticker,
                    "start_time": start_time
                }).scalar()
                
                print(f"Found {count} rows for the period")
                
                if count == 0:
                    return {"error": "데이터가 없습니다.", "details": f"Ticker: {ticker}, Period: {period}, Start Time: {start_time}"}
                
                # 데이터가 있으면 N개씩 그룹화하여 OHLC 계산
                query = text("""
                    WITH groups AS (
                        SELECT
                            created_at as timestamp,
                            price,
                            -- 캔들스틱 그룹화 크기 설정
                            -- 아래 숫자를 조정하여 한 캔들에 포함될 데이터 수를 변경할 수 있습니다.
                            -- 예: 10개 데이터 = 50분 단위 캔들
                            -- 현재: 5개 데이터 = 25분 단위 캔들
                            FLOOR((ROW_NUMBER() OVER (ORDER BY created_at) - 1) / 5) as group_id
                        FROM stock_prices
                        WHERE ticker = :ticker
                        AND created_at >= :start_time
                    ),
                    group_stats AS (
                        SELECT DISTINCT
                            group_id,
                            FIRST_VALUE(timestamp) OVER (PARTITION BY group_id ORDER BY timestamp) as timestamp,
                            FIRST_VALUE(price) OVER (PARTITION BY group_id ORDER BY timestamp) as open,
                            LAST_VALUE(price) OVER (PARTITION BY group_id ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as close,
                            MAX(price) OVER (PARTITION BY group_id) as high,
                            MIN(price) OVER (PARTITION BY group_id) as low
                        FROM groups
                    )
                    SELECT
                        timestamp,
                        open,
                        high,
                        low,
                        close
                    FROM group_stats
                    ORDER BY timestamp
                """)
                
                print("Executing OHLC query...")
                result = db.execute(query, {
                    "ticker": ticker,
                    "start_time": start_time
                })
                
                try:
                    rows = result.mappings().all()
                    print(f"Query executed successfully. Found {len(rows)} grouped records")
                    
                    data = [{
                        "timestamp": row['timestamp'],
                        "open": float(row['open']),
                        "high": float(row['high']),
                        "low": float(row['low']),
                        "close": float(row['close']),
                        "volume": 0
                    } for row in rows]
                    
                    print(f"Data processed successfully. First record: {data[0] if data else 'No data'}")
                    return data
                    
                except Exception as e:
                    print(f"Error processing query results: {str(e)}")
                    print(f"Result object: {result}")
                    raise HTTPException(
                        status_code=500,
                        detail={
                            "error": f"데이터 처리 중 오류 발생: {str(e)}",
                            "location": "result processing"
                        }
                    )
                
            except Exception as e:
                print(f"Error in 5min data processing: {str(e)}")
                print(f"Full error details: {e.__class__.__name__}: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": f"5분봉 데이터 처리 중 오류 발생: {str(e)}",
                        "error_type": e.__class__.__name__,
                        "query_params": {
                            "ticker": ticker,
                            "period": period,
                            "start_time": str(start_time)
                        }
                    }
                )

        # 일봉 데이터 (stock_daily_data 테이블, 그대로 사용)
        elif period == "1day":
            query = text("""
                SELECT 
                    price_date as timestamp,
                    open_price as open,
                    high_price as high,
                    low_price as low,
                    close_price as close,
                    COALESCE(volume, 0) as volume
                FROM stock_daily_data
                WHERE ticker = :ticker
                AND price_date >= :start_time
                ORDER BY price_date
            """)
            
            start_time = datetime.now() - timedelta(days=60)  # 60일치 데이터
            result = db.execute(query, {"ticker": ticker, "start_time": start_time}).mappings().all()
            data = [{
                "timestamp": row['timestamp'],
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close']),
                "volume": float(row['volume'])
            } for row in result]

        # 주봉 데이터
        elif period == "1week":
            query = text("""
                WITH weekly AS (
                    SELECT 
                        date_trunc('week', price_date) as week_start,
                        MIN(price_date) as first_date,
                        MAX(price_date) as last_date,
                        FIRST_VALUE(open_price) OVER (PARTITION BY date_trunc('week', price_date) ORDER BY price_date) as open_price,
                        MAX(high_price) as high_price,
                        MIN(low_price) as low_price,
                        LAST_VALUE(close_price) OVER (PARTITION BY date_trunc('week', price_date) ORDER BY price_date) as close_price,
                        SUM(volume) as volume
                    FROM stock_daily_data
                    WHERE ticker = :ticker
                    AND price_date >= :start_time
                    GROUP BY date_trunc('week', price_date), price_date, open_price, close_price
                )
                SELECT DISTINCT
                    last_date as timestamp,
                    open_price as open,
                    high_price as high,
                    low_price as low,
                    close_price as close,
                    volume
                FROM weekly
                ORDER BY last_date
            """)
            
            start_time = datetime.now() - timedelta(days=365)  # 1년치 데이터
            result = db.execute(query, {"ticker": ticker, "start_time": start_time}).mappings().all()
            data = [{
                "timestamp": row['timestamp'],
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close']),
                "volume": float(row['volume'])
            } for row in result]

        # 월봉 데이터
        elif period == "1month":
            query = text("""
                WITH monthly AS (
                    SELECT 
                        date_trunc('month', price_date) as month_start,
                        MIN(price_date) as first_date,
                        MAX(price_date) as last_date,
                        FIRST_VALUE(open_price) OVER (PARTITION BY date_trunc('month', price_date) ORDER BY price_date) as open_price,
                        MAX(high_price) as high_price,
                        MIN(low_price) as low_price,
                        LAST_VALUE(close_price) OVER (PARTITION BY date_trunc('month', price_date) ORDER BY price_date) as close_price,
                        SUM(volume) as volume
                    FROM stock_daily_data
                    WHERE ticker = :ticker
                    AND price_date >= :start_time
                    GROUP BY date_trunc('month', price_date), price_date, open_price, close_price
                )
                SELECT DISTINCT
                    last_date as timestamp,
                    open_price as open,
                    high_price as high,
                    low_price as low,
                    close_price as close,
                    volume
                FROM monthly
                ORDER BY last_date
            """)
            
            start_time = datetime.now() - timedelta(days=365*5)  # 5년치 데이터
            result = db.execute(query, {"ticker": ticker, "start_time": start_time}).mappings().all()
            data = [{
                "timestamp": row['timestamp'],
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close']),
                "volume": float(row['volume'])
            } for row in result]

        # 라인 차트용 데이터 (stock_daily_data)
        else:
            if period == "3M":
                start_time = datetime.now() - timedelta(days=90)
            elif period == "1Y":
                start_time = datetime.now() - timedelta(days=365)
            else:  # ALL
                start_time = datetime(2000, 1, 1)
            
            query = text("""
                SELECT 
                    price_date as timestamp,
                    close_price as price,
                    COALESCE(volume, 0) as volume
                FROM stock_daily_data
                WHERE ticker = :ticker
                AND price_date >= :start_time
                ORDER BY price_date
            """)

            result = db.execute(query, {"ticker": ticker, "start_time": start_time}).mappings().all()
            data = [{
                "timestamp": row['timestamp'],
                "price": float(row['price']),
                "volume": float(row['volume'])
            } for row in result]
        
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
        if period not in ["5min"]:  # 5분봉 데이터에는 예측 데이터 제외
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
