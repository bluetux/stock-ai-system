from flask import Flask, render_template, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL 접속 정보
POSTGRES_HOST = "db"
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "securepassword")
POSTGRES_DB = os.getenv("POSTGRES_DB", "stock_data")

def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB, user=POSTGRES_USER,
        password=POSTGRES_PASSWORD, host=POSTGRES_HOST
    )

# ✅ **홈페이지**
@app.route("/")
def home():
    return render_template("index.html")

# ✅ **대시보드**
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ✅ **수집된 주가 보기**
@app.route('/stocks')
def stock_list():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 주식 그룹 목록 조회
    cur.execute("SELECT id, name FROM stock_groups;")
    stock_groups = cur.fetchall()

    # 개별 종목 목록 조회 (최근 가격 포함)
    cur.execute("""
        SELECT s.ticker, COALESCE(w.alias, s.ticker) AS alias, s.price, s.created_at
        FROM stock_data s
        JOIN watchlist w ON s.ticker = w.ticker
        WHERE s.created_at = (SELECT MAX(created_at) FROM stock_data WHERE ticker = s.ticker);
    """)
    stocks = cur.fetchall()

    cur.close()
    conn.close()
    
    return render_template("stocks.html", stock_groups=stock_groups, stocks=stocks)

# ✅ **API: 주가 데이터 JSON 반환**
@app.route("/api/stocks/", methods=["GET"])
def api_stock_prices():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.ticker, COALESCE(w.alias, s.ticker) AS alias, s.price, s.created_at
        FROM stock_data s
        JOIN watchlist w ON s.ticker = w.ticker
        WHERE s.created_at = (SELECT MAX(created_at) FROM stock_data WHERE ticker = s.ticker);
    """)
    
    stocks = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"ticker": row[0], "name": row[1], "price": row[2], "date": row[3]} for row in stocks])

# ✅ **AI 예측 결과**
@app.route("/ai-prediction")
def ai_prediction():
    return render_template("ai_prediction.html")

# ✅ **Quant 분석**
@app.route("/quant-analysis")
def quant_analysis():
    return render_template("quant_analysis.html")

# ✅ **설정 페이지**
@app.route("/settings")
def settings():
    return render_template("settings.html")

# ✅ **관심 종목 추가 API**
@app.route("/api/watchlist", methods=["POST"])
def add_to_watchlist():
    data = request.json
    ticker = data.get("ticker")
    alias = data.get("alias", "")

    if not ticker:
        return jsonify({"error": "ticker is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO watchlist (ticker, alias) VALUES (%s, %s) ON CONFLICT (ticker) DO UPDATE SET alias = EXCLUDED.alias;",
        (ticker, alias)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": f"{ticker} added to watchlist"}), 201

# ✅ **API: 특정 주식의 주가 변동 데이터**
@app.route("/api/stock/<ticker>", methods=["GET"])
def api_stock_data(ticker):
    conn = get_db_connection()
    cur = conn.cursor()

    # 티커별 5일치 데이터 가져오기
    cur.execute("""
        SELECT ticker, price, created_at FROM stock_data
        WHERE ticker = %s ORDER BY created_at DESC LIMIT 5;
    """, (ticker,))
    
    stock_history = cur.fetchall()
    cur.execute("SELECT alias FROM watchlist WHERE ticker = %s;", (ticker,))
    alias = cur.fetchone()
    
    cur.close()
    conn.close()

    return jsonify({
        "ticker": ticker,
        "name": alias[0] if alias else ticker,
        "history": [{"date": row[2], "price": row[1]} for row in stock_history]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
