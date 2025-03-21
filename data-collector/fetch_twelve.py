import os
from dotenv import load_dotenv
import psycopg2
import requests
from datetime import datetime

# ✅ 환경 변수 로드
load_dotenv()
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")

BASE_URL = "https://api.twelvedata.com/time_series"

# ✅ DB 연결 함수
def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )

# ✅ watchlist에서 TWELVE 종목 가져오기
def get_watchlist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ticker FROM watchlist WHERE is_active = TRUE AND data_source = 'TWELVE'")
    tickers = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return tickers

# ✅ TWELVE API에서 실시간 주가 데이터 가져오기
def fetch_twelve_data(symbol):
    params = {
        "symbol": symbol,
        "interval": "1min",
        "outputsize": 1,
        "apikey": TWELVE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "values" in data:
            latest = data["values"][0]
            return {
                "ticker": symbol,
                "price": float(latest["close"]),
                "created_at": datetime.strptime(latest["datetime"], "%Y-%m-%d %H:%M:%S")
            }
        else:
            print(f"⚠️ {symbol} 데이터 없음 또는 오류: {data}")
    else:
        print(f"❌ {symbol} 요청 실패: {response.status_code}")
    return None

# ✅ DB에 저장
def save_to_db(record):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO stock_data (ticker, country, price, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ticker, created_at)
            DO UPDATE SET price = EXCLUDED.price;
        """, (record["ticker"], "US", record["price"], record["created_at"]))
        conn.commit()
        print(f"✅ {record['ticker']} 저장 완료")
    except Exception as e:
        print(f"❌ {record['ticker']} 저장 실패: {e}")
    finally:
        cur.close()
        conn.close()

# ✅ 전체 실행
def fetch_all():
    tickers = get_watchlist()
    for ticker in tickers:
        print(f"\n📊 {ticker} 실시간 데이터 가져오는 중...")
        record = fetch_twelve_data(ticker)
        if record:
            save_to_db(record)

# ✅ 스크립트 실행
if __name__ == "__main__":
    fetch_all()
