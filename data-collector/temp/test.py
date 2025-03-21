symbols = ["META", "AAPL", "QQQ", "NVDL", ".INX", ".IXIC"]

for symbol in symbols:
    url = get_naver_worldstock_url(symbol)
    if url:
        print(f"🔗 {symbol} → {url}")
    else:
        print(f"🚫 {symbol} → 유효한 URL을 찾지 못했습니다.")
