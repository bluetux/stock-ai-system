# scraper_utils.py
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def guess_naver_worldstock_url(symbol: str) -> str:
    index_symbols = [".INX", ".IXIC"]
    etf_symbols = ["QQQ", "NVDL"]

    if symbol in index_symbols:
        return f"https://m.stock.naver.com/worldstock/index/{symbol}/total"
    elif symbol in etf_symbols:
        return f"https://m.stock.naver.com/worldstock/etf/{symbol}.O/total"
    else:
        return f"https://m.stock.naver.com/worldstock/stock/{symbol}.O/total"

def search_naver_worldstock(symbol: str) -> str | None:
    search_url = f"https://m.stock.naver.com/search?query={symbol}"
    try:
        res = requests.get(search_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        link_tag = soup.find("a", href=re.compile(r"/worldstock/(stock|etf|index)/.+/total"))
        if link_tag:
            return f"https://m.stock.naver.com{link_tag['href']}"
        else:
            print(f"❌ [검색실패] {symbol} 에 대한 링크를 찾지 못함.")
    except Exception as e:
        print(f"⚠️ [검색오류] {symbol}: {e}")
    return None

def get_naver_worldstock_url(symbol: str) -> str | None:
    url = guess_naver_worldstock_url(symbol)
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200 and "네이버" in res.text:
            return url
        else:
            print(f"⚠️ [추정 URL 실패] {symbol} → 검색으로 대체")
            return search_naver_worldstock(symbol)
    except Exception as e:
        print(f"⚠️ [URL 확인 오류] {symbol}: {e}")
        return search_naver_worldstock(symbol)
