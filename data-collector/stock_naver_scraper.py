# stock_naver_scraper.py
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import pytz
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ✅ 심볼 변환 함수 (예: ^GSPC → .INX, ^KQ11 → .KQ11 등)
def convert_symbol_for_naver(symbol: str) -> str:
    conversion_map = {
        "^GSPC": ".INX",
        "^IXIC": ".IXIC",
        "^KQ11": ".KQ11",
        "^KS11": ".KS11",
    }
    return conversion_map.get(symbol, symbol)

# ✅ 한국 주식 데이터 크롤링
def fetch_korea_stock_naver(ticker):
    clean_ticker = ticker.split(".")[0]
    url = f"https://finance.naver.com/item/sise.naver?code={clean_ticker}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        prices = soup.select("div.new_totalinfo dl.blind dd")

        def extract_price(text):
            match = re.search(r"[\d,]+", text)
            return match.group().replace(",", "") if match else None

        if len(prices) >= 9:
            stock_data = {
                "ticker": ticker,
                "current_price": extract_price(prices[3].text),
                "previous_close": extract_price(prices[4].text),
                "open_price": extract_price(prices[5].text),
                "high_price": extract_price(prices[6].text),
                "low_price": extract_price(prices[8].text),
            }
            print(f"✅ {ticker} 한국 주식 데이터 가져오기 성공: {stock_data}")
            return stock_data
        else:
            print(f"⚠️ {ticker} 한국 주식 데이터 없음")
    else:
        print(f"❌ 네이버 요청 실패: {response.status_code}")
    return None

# ✅ 국내 지수 크롤링
def fetch_korea_index_naver(symbol: str):
    index_map = {
        ".KQ11": "KOSDAQ",
        ".KS11": "KOSPI"
    }

    if symbol not in index_map:
        print(f"⚠️ 국내 지수 {symbol} 은 지원되지 않음.")
        return None

    index_code = index_map[symbol]
    url = f"https://m.stock.naver.com/domestic/index/{index_code}/total"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"🔍 {symbol} 국내 지수 페이지 로딩 중: {url}")
        driver.get(url)
        time.sleep(3)
        price_element = driver.find_element(By.CSS_SELECTOR, "strong[class^='GraphMain_price__']")
        if price_element:
            print(f"✅ {symbol} 국내 지수 현재가: {price_element.text.strip()}")
            return {
                "symbol": symbol,
                "current_price": price_element.text.strip()
            }
        else:
            print(f"⚠️ {symbol} 국내 지수 가격 요소 없음")
    except Exception as e:
        print(f"⚠️ [오류] {symbol}: {e}")
    finally:
        driver.quit()
    return None

# ✅ 해외 주식 데이터 크롤링
def fetch_foreign_stock_naver(symbol: str):
    url = guess_naver_worldstock_url(symbol)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"🔍 {symbol} 해외 주식 페이지 로딩 중: {url}")
        driver.get(url)
        time.sleep(3)

        price = driver.find_element(By.CSS_SELECTOR, "strong[class^='GraphMain_price__']").text.strip()
        open_price = driver.find_element(By.XPATH, "//*[contains(text(),'시가')]/following-sibling::*").text.strip()
        high_price = driver.find_element(By.XPATH, "//*[contains(text(),'고가')]/following-sibling::*").text.strip()
        low_price = driver.find_element(By.XPATH, "//*[contains(text(),'저가')]/following-sibling::*").text.strip()

        data = {
            "symbol": symbol,
            "current_price": price.replace("\nUSD", "").replace("USD", ""),
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price
        }
        print(f"✅ {symbol} 해외 주식 데이터 가져오기 성공: {data}")
        return data
    except Exception as e:
        print(f"⚠️ [오류] {symbol}: {e}")
    finally:
        driver.quit()
    return None

# ✅ 종목 타입에 따라 크롤링 분기
def fetch_stock_data(symbol: str, region: str = None):
    """✅ 한국 주식 / 국내 지수 / 해외 주식 구분하여 크롤링 (with retry)"""
    symbol = convert_symbol_for_naver(symbol)
    korea_index_symbols = [".KQ11", ".KS11"]
    foreign_index_symbols = [".INX", ".IXIC", ".GSPC"]

    if symbol in korea_index_symbols:
        return fetch_korea_index_naver(symbol)
    elif region and region.lower() in ["kr", "한국"]:
        return fetch_korea_stock_naver(symbol)
    else:
        return retry_fetch_foreign_stock(symbol)  # ✅ 해외 주식은 retry 포함

def retry_fetch_foreign_stock(symbol: str, max_retries: int = 1, delay: int = 5):
    """✅ 실패 시 재시도 로직 포함"""
    for attempt in range(max_retries + 1):
        try:
            return fetch_foreign_stock_naver(symbol)
        except Exception as e:
            print(f"⚠️ {symbol} 시도 {attempt + 1} 실패: {e}")
            if attempt < max_retries:
                time.sleep(delay)
            else:
                print(f"❌ {symbol} 최종 실패")
                return None

                
# ✅ 네이버 월드 주식 URL 추정 함수
def guess_naver_worldstock_url(symbol: str) -> str:
    index_symbols = [".INX", ".IXIC", ".GSPC"]
    etf_symbols = ["QQQ", "NVDL"]

    if symbol in index_symbols:
        return f"https://m.stock.naver.com/worldstock/index/{symbol}/total"
    elif symbol in etf_symbols:
        return f"https://m.stock.naver.com/worldstock/etf/{symbol}.O/total"
    else:
        return f"https://m.stock.naver.com/worldstock/stock/{symbol}.O/total"


# ✅ 현재 시장 개장 여부 확인 (한국/미국)
def get_market_status():
    now_kr = datetime.now(pytz.timezone("Asia/Seoul"))
    now_us = datetime.now(pytz.timezone("America/New_York"))

    def is_open(now, open_time, close_time):
        return open_time <= now.time() <= close_time

    kr_open = is_open(now_kr, datetime.strptime("09:00", "%H:%M").time(), datetime.strptime("15:30", "%H:%M").time())
    us_open = is_open(now_us, datetime.strptime("09:30", "%H:%M").time(), datetime.strptime("16:00", "%H:%M").time())

    return {"KR": kr_open, "US": us_open}
