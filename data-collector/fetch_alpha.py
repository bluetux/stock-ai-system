# fetch_alpha.py
import requests
import pandas as pd
from datetime import datetime

ALPHA_API_KEY = "X22TDQ6CN5ASQDHK"
BASE_URL = "https://www.alphavantage.co/query"

def fetch_alpha_vantage(ticker):
    """Alpha Vantage API에서 1년치 데이터 가져오기"""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": ALPHA_API_KEY,
        "outputsize": "full"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df = df.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume"
            })
            df.index = pd.to_datetime(df.index)  # 날짜 변환
            df = df.sort_index(ascending=True)
            return df
        else:
            print(f"❌ {ticker} 데이터 없음 (Alpha Vantage)")
            return None
    else:
        print(f"❌ API 요청 실패: {response.status_code}")
        return None

# ✅ 테스트 실행
if __name__ == "__main__":
    df = fetch_alpha_vantage("TSLA")  # 테슬라(TSLA) 데이터 가져오기
    if df is not None:
        print(df.head())
