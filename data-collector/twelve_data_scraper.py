# twelve_data_scraper.py
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TWELVE_API_KEY = os.getenv("TWELVE_API_KEY", "885fae425bc643a881f012bb94d1768f")
BASE_URL = "https://api.twelvedata.com/time_series"

def fetch_twelve_data(symbol, interval="1day", outputsize=5000):
    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": TWELVE_API_KEY,
        "outputsize": outputsize,
        "order": "DESC",
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"❌ API 요청 실패: {response.status_code}")
        return None

    data = response.json()
    if "values" not in data:
        print(f"⚠️ {symbol} 데이터 없음 또는 오류: {data}")
        return None

    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)
    df.sort_index(inplace=True)

    df = df.rename(columns={"close": "price"})
    df["price"] = df["price"].astype(float)

    return df[["price"]]
