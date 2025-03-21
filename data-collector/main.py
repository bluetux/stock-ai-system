import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from korea_stock_naver_scraper import fetch_korea_stock_naver  # ✅ 네이버 주식 스크래퍼 가져오기

# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경 변수에서 DB 정보 가져오기
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def get_db_connection():
    """PostgreSQL 연결"""
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )

def get_watchlist():
    """PostgreSQL에서 활성화된 관심 종목 가져오기 (데이터 소스 포함)"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ticker, data_source FROM watchlist WHERE is_active = TRUE;")
    tickers = cur.fetchall()
    cur.close()
    conn.close()
    return tickers  # ✅ ticker와 data_source 함께 리턴

# ✅ 데이터 소스 매핑
DATA_SOURCE = {
    "NAVER": fetch_korea_stock_naver
}

def save_to_db(ticker, data):
    """데이터를 DB에 저장"""
    if not data or not data["current_price"].isdigit():
        print(f"⚠️ {ticker} 데이터 없음 또는 유효하지 않음, 저장 스킵")
        return

    price = int(data["current_price"].replace(",", ""))  # ✅ 콤마 제거 후 정수 변환

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO stock_data (ticker, country, price, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ticker, created_at)
            DO UPDATE SET price = EXCLUDED.price;
        """, (ticker, "KR", price, datetime.now()))

        conn.commit()
        print(f"✅ {ticker} 데이터 저장 완료")
    except Exception as e:
        print(f"❌ {ticker} 데이터 저장 실패: {e}")
    finally:
        cur.close()
        conn.close()


def run_scraper():
    """등록된 관심 종목을 기반으로 스크래핑 실행"""
    tickers = get_watchlist()
    for ticker, source in tickers:
        if source in DATA_SOURCE:
            print(f"🚀 {ticker} → {source} 방식으로 데이터 가져오기")
            stock_data = DATA_SOURCE[source](ticker)
            save_to_db(ticker, stock_data)  # ✅ 가져온 데이터 DB에 저장
        else:
            print(f"⚠️ {ticker}: 지원하지 않는 데이터 소스 {source}")

if __name__ == "__main__":
    run_scraper()
