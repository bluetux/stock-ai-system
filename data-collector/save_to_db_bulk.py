# ✅ save_to_db_bulk.py
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

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


def save_single_record(ticker, price, created_at=None, table="stock_prices"):
    conn = get_db_connection()
    cur = conn.cursor()

    if not created_at:
        created_at = datetime.now()

    query = f"""
        INSERT INTO {table} (ticker, price, created_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (ticker, created_at) DO UPDATE SET
            price = EXCLUDED.price;
    """
    try:
        cur.execute(query, (ticker, price, created_at))
        conn.commit()
        print(f"✅ {ticker} 저장 완료")
    except Exception as e:
        print(f"❌ {ticker} 저장 실패: {e}")
    finally:
        cur.close()
        conn.close()


def save_daily_stock_data(ticker, open_price, high_price, low_price, close_price, volume=None):
    conn = get_db_connection()
    cur = conn.cursor()

    today = datetime.today().date()

    query = """
        INSERT INTO stock_daily_data (ticker, price_date, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, price_date) DO UPDATE SET
            open_price = EXCLUDED.open_price,
            high_price = EXCLUDED.high_price,
            low_price = EXCLUDED.low_price,
            close_price = EXCLUDED.close_price;
    """
    try:
        cur.execute(query, (ticker, today, open_price, high_price, low_price, close_price, volume))
        conn.commit()
        print(f"✅ {ticker} 일별 데이터 저장 완료")
    except Exception as e:
        print(f"❌ {ticker} 일별 데이터 저장 실패: {e}")
    finally:
        cur.close()
        conn.close()