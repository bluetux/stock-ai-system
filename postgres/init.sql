-- 🔧 사용자 및 데이터베이스 생성
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stock_data') THEN
        CREATE DATABASE stock_data;
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
        CREATE USER admin WITH ENCRYPTED PASSWORD 'securepassword';
        ALTER ROLE admin WITH SUPERUSER;
        GRANT ALL PRIVILEGES ON DATABASE stock_data TO admin;
    END IF;
END $$;

-- ✅ DB 연결
\c stock_data;

-- ✅ 관심 종목 테이블
CREATE TABLE IF NOT EXISTS watchlist (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) UNIQUE NOT NULL,
    alias VARCHAR(50) DEFAULT '',
    is_active BOOLEAN DEFAULT TRUE,
    data_source VARCHAR(10) DEFAULT 'NAVER',
    is_open BOOLEAN DEFAULT TRUE,
    region VARCHAR DEFAULT 'ETC',
    icon VARCHAR(50) DEFAULT 'activity',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ 실시간 가격 저장 테이블
CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_price_per_minute UNIQUE (ticker, created_at)
);

-- ✅ 일별 가격 저장 테이블
CREATE TABLE IF NOT EXISTS stock_daily_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    price_date DATE NOT NULL,
    open_price NUMERIC(10, 2),
    high_price NUMERIC(10, 2),
    low_price NUMERIC(10, 2),
    close_price NUMERIC(10, 2),
    volume BIGINT,
    exchange_rate DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_daily UNIQUE (ticker, price_date)
);

-- ✅ AI 예측 결과 저장
CREATE TABLE IF NOT EXISTS ai_predictions (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    predicted_price NUMERIC(10,2) NOT NULL,
    prediction_period VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ Quant 분석 결과 저장
CREATE TABLE IF NOT EXISTS quant_results (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    analysis_result NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ 주식 그룹 테이블 (아이콘 포함)
CREATE TABLE IF NOT EXISTS stock_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    icon VARCHAR(50) DEFAULT ''
);

-- ✅ 주식 그룹 매핑 테이블
CREATE TABLE IF NOT EXISTS stock_group_mapping (
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES stock_groups(id),
    ticker VARCHAR(20) REFERENCES watchlist(ticker)
);

-- ✅ 기본 그룹 데이터 추가 (icon도 함께)
INSERT INTO stock_groups (name, icon) VALUES
('AI 관련', '🧠'), 
('방산 관련', '🚀'), 
('IT 대기업', '💻'), 
('반도체', '🔋') 
ON CONFLICT (name) DO NOTHING;

-- ✅ 초기 관심 종목
INSERT INTO watchlist (ticker, alias, is_active, data_source, is_open)
VALUES
    ('NVDL', 'NVIDIA ETF', TRUE, 'NAVER', TRUE),
    ('012450.KS', '한화에어로스페이스', TRUE, 'NAVER', TRUE),
    ('^IXIC', 'NASDAQ Composite', TRUE, 'NAVER', TRUE),
    ('^KQ11', 'KOSDAQ Index', TRUE, 'NAVER', TRUE),
    ('^GSPC', 'S&P 500', TRUE, 'NAVER', TRUE),
    ('AAPL', 'Apple Inc.', TRUE, 'NAVER', TRUE)
ON CONFLICT (ticker) DO NOTHING;

-- ✅ 종목별 region 설정
UPDATE watchlist SET region = '한국' WHERE ticker = '012450.KS';
UPDATE watchlist SET region = '미국' WHERE ticker IN ('AAPL', 'NVDL');
UPDATE watchlist SET region = '지수' WHERE ticker IN ('^IXIC', '^GSPC', '^KQ11');

-- ✅ 그룹-종목 매핑
INSERT INTO stock_group_mapping (group_id, ticker) VALUES
  (2, '012450.KS'),  -- 방산
  (3, 'AAPL'),       -- IT 대기업
  (1, 'NVDL'),       -- AI 관련
  (4, 'NVDL'),       -- 반도체
  (3, 'NVDL')        -- IT 대기업
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS watchlist_group_map (
    watchlist_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    PRIMARY KEY (watchlist_id, group_id),
    FOREIGN KEY (watchlist_id) REFERENCES watchlist(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES stock_groups(id) ON DELETE CASCADE
);