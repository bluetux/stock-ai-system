import FinanceDataReader as fdr
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd

# ✅ .env 로드
load_dotenv()

# ✅ 환경 변수에서 DB 정보 가져오기
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "securepassword")
POSTGRES_DB = os.getenv("POSTGRES_DB", "stock_data")

# ✅ DB 연결 함수
def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )

# ✅ 관심 종목 가져오기 & Ticker 변환
def get_watchlist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ticker FROM watchlist WHERE is_active = TRUE;")
    tickers = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    # ✅ KQ, KS 제거 (FDR 호환)
    tickers = [ticker.replace('.KQ', '').replace('.KS', '') for ticker in tickers]
    return tickers

# def fetch_fdr_data(ticker: str) -> dict:
#     try:
#         df = fdr.DataReader(ticker)
#         if df is None or df.empty:
#             print(f"⚠️ {ticker} FDR 데이터 없음")
#             return None
#         latest = df.iloc[-1]
#         return {
#             "ticker": ticker,
#             "price": round(float(latest['Close']), 2),
#             "created_at": latest.name.to_pydatetime()  # datetime
#         }
#     except Exception as e:
#         print(f"❌ {ticker} FDR 데이터 가져오기 실패: {e}")
#         return None

# ✅ 과거 데이터 저장 함수
def save_stock_data(ticker, data):
    """✅ stock_daily_data 테이블에 저장"""
    conn = get_db_connection()
    cur = conn.cursor()

    for date, row in data.iterrows():
        try:
            cur.execute("""
                INSERT INTO stock_daily_data (
                    ticker, price_date, open_price, high_price, low_price, close_price, volume
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, price_date) DO UPDATE SET
                    open_price = EXCLUDED.open_price,
                    high_price = EXCLUDED.high_price,
                    low_price = EXCLUDED.low_price,
                    close_price = EXCLUDED.close_price,
                    volume = EXCLUDED.volume;
            """, (
                ticker,
                date.date(),
                float(row['Open']) if not pd.isna(row['Open']) else None,
                float(row['High']) if not pd.isna(row['High']) else None,
                float(row['Low']) if not pd.isna(row['Low']) else None,
                float(row['Close']) if not pd.isna(row['Close']) else None,
                int(row['Volume']) if not pd.isna(row['Volume']) else None,
            ))
        except Exception as e:
            print(f"⚠️ {ticker} {date} 저장 실패: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ {ticker} 일별 데이터 저장 완료")


# ✅ 메인 실행 함수
def fetch_past_data():
    tickers = get_watchlist()
    
    # ✅ 주식 데이터 가져오기
    for ticker in tickers:
        print(f"📊 {ticker} 과거 데이터 가져오는 중...")
        data = fdr.DataReader(ticker)
        save_stock_data(ticker, data)

    # ✅ 환율 정보 가져오기 (USD/KRW)
    print("📈 환율 정보 가져오는 중...")
    fx_data = fdr.DataReader('USD/KRW')
    save_stock_data('USD/KRW', fx_data)

    # ✅ 금값 정보 가져오기 (GOLD/USD → GC=F로 변경)
    print("🪙 금값 정보 가져오는 중...")
    gold_data = fdr.DataReader('GC=F')  # ✅ GOLD/USD 대신 GC=F 사용
    save_stock_data('GC=F', gold_data)

if __name__ == "__main__":
    fetch_past_data()
