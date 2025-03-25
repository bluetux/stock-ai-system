# 📦 data-collector

`data-collector`는 주식 종목들의 실시간 및 일별 주가 데이터를 수집하여 PostgreSQL에 저장하는 역할을 수행하는 서브 시스템입니다.  
네이버 모바일 페이지와 FDR API 등을 통해 국내/해외 주식, 지수, ETF, 환율, 금값 정보를 크롤링합니다.

---

## 📁 주요 구성

| 파일명                  | 설명 |
|------------------------|------|
| `main.py`              | 실시간 및 일일 주가 수집 실행. 장 개장 여부 확인 및 DB 저장까지 통합 실행 |
| `stock_naver_scraper.py` | 네이버 모바일 페이지에서 실시간 데이터 크롤링. 국내/해외/지수 자동 분기 |
| `fetch_fdr.py`         | FinanceDataReader를 이용한 과거 데이터 (일별) 수집 |
| `save_to_db_bulk.py`   | 데이터베이스 저장 함수 집합. 실시간 데이터, 일별 데이터 분리 처리 |
| `init.sql`             | 전체 데이터베이스 및 테이블 초기화 스크립트 |
| `tmp/`                 | 사용하지 않거나 테스트 용도의 이전 스크립트 백업 디렉토리 |

---

## 🔍 크롤링 대상 분류

1. **국내 주식 (e.g. 005930.KS)**  
   - `finance.naver.com` HTML 크롤링
   - 가격 정보 (현재가, 시가, 고가, 저가)

2. **국내 지수 (e.g. .KQ11, .KS11)**  
   - `m.stock.naver.com/domestic/index/{KOSPI|KOSDAQ}/total`
   - Selenium으로 렌더링 후 가격 추출

3. **해외 주식/ETF/지수 (e.g. AAPL, NVDL, .IXIC)**  
   - `m.stock.naver.com/worldstock/*` 페이지 크롤링
   - 정규장에서만 반영되는 시세 정보

4. **환율 및 금값 (fetch_fdr.py)**  
   - FDR 사용: `USD/KRW`, `GC=F`

---

## 🗃️ 데이터베이스 테이블

- `watchlist`: 모니터링할 종목 목록. `is_open` 컬럼으로 장 개방 상태 추적
- `stock_data`: 실시간 가격 정보 저장
- `stock_daily_data`: 일봉용 고가/저가/종가/시가 등 저장
- `stock_history`: FDR 기반 과거 일봉 백필용
- 기타: `ai_predictions`, `quant_results`, `stock_groups`, `stock_group_mapping`

---

## 🧠 장 개장 판단 방식

- `get_market_status()` 함수가 **한국/미국장 본장 기준으로 개장 여부 판단**
- 종목은 현재 `KR`/`US` 단위로 분기하여 처리
- 향후에는 종목별 `exchange` 필드를 추가하여 거래소별 시간표 기반 분기로 확장 가능

---

## ⏱️ cron 자동화

- `main.py`, `fetch_fdr.py` 는 `cron` 을 통해 5분 단위, 하루 단위 등으로 자동 실행 가능
- 실시간 수집은 1~2초 딜레이 허용 기준으로 설계됨

---

## ✅ TODO 및 향후 계획

- [ ] 종목별 거래소 (`exchange`) 구분 및 거래소별 장 개장 판단
- [ ] Web UI를 통한 종목 관리, 그룹핑, 분석 그래프 시각화
- [ ] 투자 가치선 / 판매 타이밍 표시 기능
- [ ] 분석 단계: AI 예측 / Quant 전략 연동
- [ ] API 통합 (Twelve Data, Alpha Vantage 등)

---

## 🧼 기타 참고

- 실거래 목적이 아닌, **퀀트 전략 및 분석용 수집 시스템**
- 프리마켓/애프터마켓 정보는 무시
- 기본 원칙: "단순하지만 확장 가능한 구조"

---

_작성자: [terry@localhost]_  
_도움이 필요하면 언제든지 `ChatGPT` 호출!_ 😎
