import os
import psycopg2
from dotenv import load_dotenv
from stock_naver_scraper import fetch_stock_data

# ✅ 환경 변수 로드
load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


def get_watchlist_symbols():
    """✅ DB에서 watchlist에 있는 종목을 불러오면서 네이버용 심볼로 변환"""
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )
    cur = conn.cursor()
    cur.execute("SELECT ticker FROM watchlist WHERE is_active = TRUE;")
    symbols = [row[0] for row in cur.fetchall()]
    conn.close()  # ✅ DB 연결 닫기

    # ✅ 네이버에서 사용할 수 있도록 변환 (예: ^IXIC → .IXIC)
    converted_symbols = [symbol.replace("^", ".") for symbol in symbols]
    return converted_symbols  # ✅ 이제 'connection'이 아니라 리스트를 반환!


def run_naver_scraper():
    """✅ watchlist에서 가져온 종목으로 네이버 크롤링 실행"""
    watchlist_symbols = get_watchlist_symbols()  # ✅ 이제 리스트를 반환함
    for symbol in watchlist_symbols:
        fetch_stock_data(symbol)  # ✅ 각각의 종목에 대해 크롤링 실행

if __name__ == "__main__":
    run_naver_scraper()
