# save_to_db.py
import psycopg2

def save_to_db(ticker, df, source="TWELVE"):
    """데이터를 DB에 저장"""
    if df is None or df.empty:
        print(f"⚠️ {ticker} 데이터 없음, 저장 스킵")
        return

    conn = psycopg2.connect(
        dbname="stock_data",
        user="admin",
        password="securepassword",
        host="db"
    )
    cur = conn.cursor()

    for date, row in df.iterrows():
        cur.execute("""
            INSERT INTO stock_data (ticker, country, price, created_at, data_source)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (ticker, created_at)
            DO UPDATE SET price = EXCLUDED.price;
        """, (ticker, "US" if source in ["TWELVE", "ALPHA"] else "KR", row["close"], date, source))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ {ticker} 데이터 저장 완료")
