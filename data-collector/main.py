# data-collector/main.py
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from stock_naver_scraper import fetch_stock_data, get_market_status
from save_to_db_bulk import save_single_record, save_daily_stock_data

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

def get_watchlist_symbols():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ticker, is_open, region FROM watchlist WHERE is_active = TRUE;")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result  # [(ticker, is_open, region), ...]

def update_open_flag(ticker, is_open):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE watchlist SET is_open = %s WHERE ticker = %s;", (is_open, ticker))
    conn.commit()
    cur.close()
    conn.close()

def safe_float(value):
    try:
        return float(str(value).replace(",", ""))
    except:
        return 0.0

def run_naver_scraper():
    market_status = get_market_status()
    print(f"🇰🇷 한국장: {'🟢 열림' if market_status['KR'] else '🔴 마감'} ({datetime.now().strftime('%H:%M')})")
    print(f"🇺🇸 미국장: {'🟢 열림' if market_status['US'] else '🔴 마감'} ({datetime.now().strftime('%H:%M')})")
    print("✅ 장이 열려 있음! 실시간 크롤링 실행 가능.")

    for ticker, is_open_flag, region in get_watchlist_symbols():
        data = fetch_stock_data(ticker, region)
        if not data:
            continue

        symbol = data.get("symbol") or data.get("ticker")
        if region.lower() in ["kr", "한국"]:
            market = "KR"
        elif region.lower() in ["us", "미국"]:
            market = "US"
        else:
            market = "KR" if ".KS" in symbol or ".KQ" in symbol or "^KQ" in symbol else "US"
        is_market_open = market_status[market]

        if is_open_flag and is_market_open:
            # 열림 상태 유지
            save_single_record(symbol, safe_float(data["current_price"]))
            save_daily_stock_data(
                ticker=symbol,
                open_price=safe_float(data.get("open_price")),
                high_price=safe_float(data.get("high_price")),
                low_price=safe_float(data.get("low_price")),
                close_price=safe_float(data["current_price"]),
                volume=None
            )
        elif is_open_flag and not is_market_open:
            # 장 종료: 마지막 업데이트 후 open flag false
            save_single_record(symbol, safe_float(data["current_price"]))
            save_daily_stock_data(
                ticker=symbol,
                open_price=safe_float(data.get("open_price")),
                high_price=safe_float(data.get("high_price")),
                low_price=safe_float(data.get("low_price")),
                close_price=safe_float(data["current_price"]),
                volume=None
            )
            update_open_flag(ticker=symbol, is_open=False)
        elif not is_open_flag and is_market_open:
            # 장 개장: open flag true 로 복구 + 새로운 일일 데이터 insert
            save_single_record(symbol, safe_float(data["current_price"]))
            save_daily_stock_data(
                ticker=symbol,
                open_price=safe_float(data.get("open_price")),
                high_price=safe_float(data.get("high_price")),
                low_price=safe_float(data.get("low_price")),
                close_price=safe_float(data["current_price"]),
                volume=None
            )
            update_open_flag(ticker=symbol, is_open=True)
        else:
            print(f"⏩ {symbol}: 장 마감 중 & open flag = False → skip")


if __name__ == "__main__":
    run_naver_scraper()
