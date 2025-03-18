import os
import yfinance as yf
import psycopg2
import pandas as pd 
from datetime import datetime, timedelta
from dotenv import load_dotenv

import pytz

# PostgreSQL 접속 정보
# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경 변수에서 DB 정보 가져오기
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


def get_db_connection():
    """환경 변수에서 불러온 DB 정보로 PostgreSQL 연결"""
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )

# 한국 시간대 설정
KST = pytz.timezone("Asia/Seoul")

def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )

def get_watchlist():
    """PostgreSQL에서 활성화된 관심 종목 가져오기"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ticker FROM watchlist WHERE is_active = TRUE;")
        tickers = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return tickers
    except Exception as e:
        print(f"❌ 관심 종목 조회 실패: {e}")
        return []

def fetch_stock_data():
    """활성화된 종목의 최근 5일치 주가 데이터 수집 및 저장 (한국 시간 변환 포함)"""
    conn = get_db_connection()
    cur = conn.cursor()

    active_tickers = get_watchlist()

    for ticker in active_tickers:
        print(f"✅ {ticker} 기존 주식 → 최근 5일치 데이터 수집")
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")

        if hist.empty:
            print(f"⚠️ {ticker} 데이터 없음")
            continue

        last_valid_price = None  # ✅ 마지막으로 저장된 유효한 가격

        for date, row in hist.iterrows():
            close_price = float(row['Close']) if not pd.isna(row['Close']) else None

            # ✅ 주가가 없으면 마지막 유효한 가격 사용
            if close_price is None or close_price == 0.0:
                if last_valid_price is not None:
                    close_price = last_valid_price
                else:
                    print(f"⚠️ {ticker} {date} 주가 없음, 스킵")
                    continue
            else:
                last_valid_price = close_price

            # ✅ 한국 시간(KST)으로 변환
            kst_date = date.astimezone(KST)

            cur.execute("""
                INSERT INTO stock_data (ticker, country, price, created_at) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (ticker, created_at) 
                DO UPDATE SET price = EXCLUDED.price;
            """, (ticker, "US" if ticker.startswith("^") else "KR", close_price, kst_date))

    conn.commit()
    cur.close()
    conn.close()
    print("📊 데이터 수집 완료")

fetch_stock_data()
