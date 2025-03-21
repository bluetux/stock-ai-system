import os
import psycopg2
import requests
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
from stock_naver_scraper import fetch_stock_data
from save_to_db_bulk import save_single_record
# from save_to_db_bulk import execute_query


# ✅ 환경 변수 로드
load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def get_watchlist_symbols():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST")
    )
    cur = conn.cursor()
    cur.execute("SELECT ticker FROM watchlist WHERE is_active = TRUE;")
    symbols = [row[0] for row in cur.fetchall()]
    conn.close()

    # ✅ 예: ^IXIC → .IXIC
    converted_symbols = [s.replace("^", ".") for s in symbols]
    return converted_symbols

def safe_float(value, default=0.0):
    try:
        return float(value.replace(",", ""))
    except (ValueError, AttributeError):
        return default

def save_stock_data_to_db(data):
    if data:
        ticker = data.get("symbol") or data.get("ticker")

        save_single_record(
            ticker=ticker,
            price=safe_float(data["current_price"])
        )

        save_daily_stock_data(
            ticker=ticker,
            open_price=safe_float(data.get("open_price")),
            high_price=safe_float(data.get("high_price")),
            low_price=safe_float(data.get("low_price")),
            close_price=safe_float(data["current_price"]),
            volume=None
        )
        print(f"✅ {ticker} 저장 완료")




def run_naver_scraper():
    """✅ 네이버 크롤링 실행 + DB 저장"""
    watchlist_symbols = get_watchlist_symbols()
    for symbol in watchlist_symbols:
        data = fetch_stock_data(symbol)
        if data:
            save_stock_data_to_db(data)  # ✅ 수정된 DB 저장 함수 호출
def execute_query(query, params):
    import psycopg2
    import os

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST")
    )
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

def save_daily_stock_data(ticker, open_price, high_price, low_price, close_price, volume):
    """✅ 실시간으로 stock_daily_data 업데이트 (크롤링될 때마다 최신화)"""
    query = """
    INSERT INTO stock_daily_data (ticker, open_price, high_price, low_price, close_price, volume, price_date)
    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
    ON CONFLICT (ticker, price_date) 
    DO UPDATE SET 
        high_price = GREATEST(stock_daily_data.high_price, EXCLUDED.high_price),  -- ✅ 최고가 최신화
        low_price = LEAST(stock_daily_data.low_price, EXCLUDED.low_price),        -- ✅ 최저가 최신화
        close_price = EXCLUDED.close_price,  -- ✅ 현재 크롤링된 가격을 종가로 업데이트
        volume = EXCLUDED.volume;  -- ✅ 거래량 업데이트 (있다면)
    """
    execute_query(query, (ticker, open_price, high_price, low_price, close_price, volume))

def is_market_open():
    """✅ 네이버 증권 페이지에서 장 상태 확인"""
    url = "https://m.stock.naver.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ 장 상태를 나타내는 텍스트 찾기
        market_status = soup.find("span", class_="market_status")
        if market_status and "장마감" in market_status.text:
            print("✅ 장이 마감됨! 실시간 크롤링 중지.")
            return False
        else:
            print("✅ 장이 열려 있음! 실시간 크롤링 실행 가능.")
            return True
    except Exception as e:
        print(f"⚠️ 장 상태 확인 실패: {e}")
        return True  # 만약 에러가 나면 기본적으로 크롤링 실행

def check_market_status():
    from datetime import datetime
    import pytz

    # 한국 시간
    kr_now = datetime.now(pytz.timezone("Asia/Seoul"))
    kr_open = kr_now.replace(hour=9, minute=0, second=0)
    kr_close = kr_now.replace(hour=15, minute=30, second=0)
    is_kr_open = kr_open <= kr_now <= kr_close

    # 미국 동부 시간 (NYSE/NASDAQ 기준)
    us_now = datetime.now(pytz.timezone("US/Eastern"))
    us_open = us_now.replace(hour=9, minute=30, second=0)
    us_close = us_now.replace(hour=16, minute=0, second=0)
    is_us_open = us_open <= us_now <= us_close

    print(f"🇰🇷 한국장: {'🟢 열림' if is_kr_open else '🔴 마감'} ({kr_now.strftime('%H:%M')})")
    print(f"🇺🇸 미국장: {'🟢 열림' if is_us_open else '🔴 마감'} ({us_now.strftime('%H:%M')})")

    return is_kr_open, is_us_open

if __name__ == "__main__":
    check_market_status()

    if is_market_open():  # 기본 장 상태 크롤링 체크
        run_naver_scraper()
    else:
        print("🚨 장 종료 상태 → 실시간 크롤링 중지")