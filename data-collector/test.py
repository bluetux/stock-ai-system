import requests
from bs4 import BeautifulSoup
import re

print("✅ test.py 실행됨!")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def validate_stock_page(url: str) -> bool:
    """
    주어진 URL에서 종목 정보(현재가 등)가 실제로 존재하는지 확인하는 함수
    """
    print(f"🔍 {url} 확인 중...")
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        print(f"🔄 응답 코드: {res.status_code}")  # 응답 상태 출력

        soup = BeautifulSoup(res.text, "html.parser")

        # 가격 정보 (현재가) 태그 확인
        price_tag = soup.find("span", class_=re.compile(r"current_price"))
        if price_tag and price_tag.text.strip():
            print(f"✅ [유효한 데이터] {url} → 현재가 존재")
            return True  # 정상적인 종목 페이지
        else:
            print(f"⚠️ [데이터 없음] {url} → 네이버 페이지에 종목 정보 없음")
            return False
    except Exception as e:
        print(f"⚠️ [확인 오류] {url}: {e}")
        return False

# 테스트용 URL 리스트 추가
test_urls = [
    "https://m.stock.naver.com/worldstock/stock/META.O/total",
    "https://m.stock.naver.com/worldstock/stock/AAPL.O/total",
    "https://m.stock.naver.com/worldstock/etf/QQQ.O/total",
    "https://m.stock.naver.com/worldstock/etf/NVDL.O/total",
    "https://m.stock.naver.com/worldstock/index/.INX/total",
    "https://m.stock.naver.com/worldstock/index/.IXIC/total",
    "https://m.stock.naver.com/worldstock/stock/INVALID.O/total"
]

print("\n📦 Naver World Stock URL 테스트 시작\n")

for url in test_urls:
    print(f"🔍 테스트 중: {url}")
    result = validate_stock_page(url)
    print(f"✅ 테스트 결과: {result}")

print("\n✅ 테스트 완료!")
