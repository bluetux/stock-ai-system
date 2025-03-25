<!-- /stock-aisystem/web-api/README.md -->
# 📊 Stock Dashboard API & UI 설계

## 📌 개요

주식 데이터를 수집하고, AI 예측 및 퀀트 분석을 활용한 대시보드를 구축하는 프로젝트입니다.  
설정 페이지에서는 관심종목 및 그룹을 관리하고, 각 종목/그룹의 Lucide 아이콘을 설정할 수 있습니다.

---

## 📌 주요 기능

### 1. 수집된 주가 보기
- `/api/stocks/` : 전체 주가 데이터 조회
- `/api/stocks/{ticker}` : 특정 종목 주가 조회

### 2. 관심종목(Watchlist) 관리
- `/api/watchlist/` : 전체 Watchlist 조회
- `/api/watchlist/{user_id}/{ticker}` : 관심 종목 추가 / 삭제
- 각 종목에는 `icon` 필드가 포함됨 (`activity`, `cpu`, `rocket`, 등 Lucide 아이콘명)

### 3. 그룹 관리
- `/api/stocks/groups` : 그룹별 종목 리스트 조회
- `/api/stocks/groups/{group_id}` : 그룹 정보 수정, 삭제
- `/api/stocks/groups/new` : 새로운 그룹 추가

### 4. 설정 페이지
- `/dashboard/settings` : 설정 메인
- `/dashboard/settings/watchlist` : 종목 추가 / 수정 / 삭제 (아이콘 포함)
- `/dashboard/settings/groups` : 그룹 추가 / 수정 / 삭제 (아이콘 포함)

### 5. AI 예측 및 퀀트 분석
- `/api/ai/predictions/{ticker}` : AI 기반 주가 예측 조회
- `/api/quant/analysis/{ticker}` : 퀀트 분석 결과 조회

---

## 📌 데이터베이스 스키마 업데이트

### 🔸 watchlist 테이블

```sql
ALTER TABLE watchlist ADD COLUMN icon VARCHAR(50) DEFAULT 'activity';

프론트엔드 UI 설계 (React + Tailwind)

🧭 전체 레이아웃
	•	상단 메뉴: 우리코난 AI 시스템, 주식 분석, 설정, 계정
	•	좌측 사이드바 1열: 지역/그룹 목록 (Lucide 아이콘 포함)
	•	좌측 사이드바 2열: 해당 그룹 종목 리스트 (Lucide 아이콘 포함)
	•	메인 컨텐츠: 대시보드 / 종목 상세 / 설정 페이지 등


                  # ✅ 이 문서

---

## 🎨 프론트엔드 UI 상세 설계 (React + Tailwind)

### 🌈 테마 및 컬러

- 기본 배경색: `#F9F8F6` (고급스러운 크림화이트)
- 설정 페이지 Sidebar: `#2C3E50` (시스템 설정에 적합한 다크네이비)
- 주요 텍스트: `#000000` (기본 검정)
- 강조 텍스트/링크: `#2563eb` (Tailwind blue-600)



---

## ⚙️ 시스템 설정 페이지 설계 (`/dashboard/settings`)

설정 페이지는 주식 분석 시스템에서 관리할 항목들을 제어할 수 있는 인터페이스입니다.

### 📁 페이지 구성

- `/dashboard/settings`
  - 설정 메인 페이지 (왼쪽 사이드바 포함)
- `/dashboard/settings/watchlist`
  - 관심 종목 추가, 수정, 삭제
  - 종목 아이콘 선택 가능 (Lucide 아이콘)
- `/dashboard/settings/groups`
  - 그룹 목록 관리, 아이콘 설정

---

### 🎛️ SettingsSidebar 구성

- 배경 색상: `#2C3E50` (다크 네이비 계열)
- 텍스트 색상: `white`
- 구성 항목:
  - 📋 관심종목 관리 (`/dashboard/settings/watchlist`)
  - 🗂️ 그룹 관리 (`/dashboard/settings/groups`)
- 접기 / 펼치기 기능 제공 (`<<`, `>>` 버튼)
- Lucide 아이콘 사용

---
---

### 📝 설정 항목 기능 요약

#### 1. 관심종목 관리 (WatchlistSettings)

- 기존 종목 수정
- 새로운 종목 추가
- 종목 삭제
- 종목 아이콘 변경 (`LucideIcons` 목록 중 선택)

#### 2. 그룹 관리 (GroupSettings)

- 기존 그룹명 및 아이콘 수정
- 새로운 그룹 추가
- 그룹 삭제
- 그룹에 포함된 종목 확인 및 수정

> 이 설정은 데이터베이스의 `watchlist` 및 `stock_groups` 테이블을 직접 반영합니다.

---

### 🛠️ 향후 확장 예정 항목

- AI 분석 설정
  - AI 알고리즘 선택
  - 알림 조건 설정
- 사용자 인터페이스 세부 설정 (다크 모드 등)
- 백테스트 / 시뮬레이션 파라미터 조정

---