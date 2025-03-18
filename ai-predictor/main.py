import os
import psycopg2 # noqa
import numpy as np
import tensorflow as tf
from tensorflow import keras
from dotenv import load_dotenv

# ✅ TensorFlow 최적화 설정
os.environ["TF_XLA_FLAGS"] = "--tf_xla_auto_jit=2"

# ✅ PostgreSQL 접속 정보 (환경변수 사용)
# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경 변수에서 DB 정보 가져오기
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def get_db_connection():
    """환경 변수에서 불러온 DB 정보로 PostgreSQL 연결"""
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )


# ✅ PostgreSQL 연결 및 테이블 자동 생성
try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST
    )
    cursor = conn.cursor()

    # ✅ AI 예측 테이블 생성 (없으면 자동 생성)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_predictions (
        id SERIAL PRIMARY KEY,
        ticker VARCHAR(20) UNIQUE,
        predicted_price FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ PostgreSQL 테이블 확인 완료")
except Exception as e:
    print(f"❌ PostgreSQL 연결 실패: {e}")

# ✅ 모델 로드 코드 추가
model_path = "/app/model.h5"  # 모델 파일 경로
try:
    model = keras.models.load_model(model_path)
    print("✅ 모델 로드 성공:", model_path)
except Exception as e:
    print("❌ 모델 로드 실패:", str(e))
    model = None

def fetch_stock_data():
    """DB에서 관심 종목의 최신 가격 데이터를 가져옴"""
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST
        )
        cur = conn.cursor()
        cur.execute("SELECT ticker, price FROM stock_data")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data if data else []
    except Exception as e:
        print(f"❌ DB 데이터 가져오기 실패: {e}")
        return []

def predict_stock_price(data):
    """주어진 데이터를 사용하여 주가 예측"""
    if model is None:
        print("❌ 모델이 로드되지 않았습니다. 예측을 실행할 수 없습니다.")
        return []

    if not data:
        print("❌ 예측할 데이터가 없습니다.")
        return []

    results = []
    for row in data:
        ticker = row[0]
        price = float(row[1]) if row[1] is not None else 0  
        input_data = np.array([[price]], dtype=np.float32)  
        predicted_price = float(model.predict(input_data)[0][0])  
        results.append((ticker, predicted_price))
        print(f"📊 AI 예측 결과: {ticker} - {predicted_price}")

    return results

def save_prediction_results(results):
    """AI 예측 결과를 DB에 저장 (이력 남기도록 변경)"""
    conn = psycopg2.connect( ... )
    cur = conn.cursor()
    for result in results:
        cur.execute(
            "INSERT INTO ai_predictions (ticker, predicted_price, created_at) VALUES (%s, %s, NOW())",
            (result["ticker"], result["predicted_price"])
        )
    conn.commit()
    cur.close()
    conn.close()
    print("✅ AI 예측 결과 저장 완료")


# 실행
if model:
    data = fetch_stock_data()
    if data:
        results = predict_stock_price(data)
        save_predictions(results)
        print("📊 AI 예측 완료 및 저장 완료")
    else:
        print("⚠️ 예측할 데이터가 없습니다.")
