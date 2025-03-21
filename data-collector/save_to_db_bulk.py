import os
import psycopg2
from dotenv import load_dotenv
import datetime

# .env 값 로드
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

def save_single_record(ticker, price, created_at=None, country="US", table="stock_data"):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        if not created_at:
            created_at = datetime.datetime.now()

        cur.execute(f"""
            INSERT INTO {table} (ticker, country, price, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ticker, created_at)
            DO UPDATE SET price = EXCLUDED.price;
        """, (ticker, country, float(price), created_at))

        conn.commit()
        print(f"✅ {ticker} 저장 완료")
    except Exception as e:
        print(f"❌ {ticker} 저장 실패: {e}")
    finally:
        cur.close()
        conn.close()
