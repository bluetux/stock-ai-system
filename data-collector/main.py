import os
import psycopg2
from dotenv import load_dotenv
from twelve_data_scraper import fetch_twelve_data
from korea_stock_naver_scraper import fetch_korea_stock_naver
from fetch_fdr import fetch_fdr_data
from save_to_db_bulk import save_single_record

# ✅ 환경 변수 로드
load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )


def get_watchlist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ticker, data_source FROM watchlist WHERE is_active = TRUE;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def run_scraper():
    watchlist = get_watchlist()
    for ticker, source in watchlist:
        print(f"\n📊 {ticker} 실시간 데이터 가져오는 중...")

        try:
            if source == "NAVER":
                data = fetch_korea_stock_naver(ticker)
                if data and "current_price" in data:
                    save_single_record(ticker, data["current_price"], country="KR")
                else:
                    print(f"⚠️ {ticker} NAVER 데이터 없음 또는 구조 오류")

            elif source == "TWELVE":
                data = fetch_twelve_data(ticker)
                if data is not None and isinstance(data, dict) and "price" in data:
                    save_single_record(ticker, data["price"], country="US")
                else:
                    print(f"⚠️ {ticker} TWELVE 데이터 없음 또는 구조 오류: {data}")

            elif source == "FDR":
                data = fetch_fdr_data(ticker)
                if data is not None and "price" in data:
                    save_single_record(ticker, data["price"], country="KR")
                else:
                    print(f"⚠️ {ticker} FDR 데이터 없음 또는 구조 오류: {data}")

            else:
                print(f"⚠️ {ticker}: 지원하지 않는 데이터 소스 '{source}'")

        except Exception as e:
            print(f"❌ {ticker} 실행 오류: {e}")


if __name__ == "__main__":
    run_scraper()
