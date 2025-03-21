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

\c stock_data;

-- ✅ 실시간 주가 데이터 테이블
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    country VARCHAR(10) CHECK (country IN ('US', 'KR')) NOT NULL DEFAULT 'US',
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_ticker_date UNIQUE (ticker, created_at)  
);

-- ✅ 과거 주가 데이터 테이블
CREATE TABLE IF NOT EXISTS stock_history (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    country VARCHAR(10) CHECK (country IN ('US', 'KR')) NOT NULL DEFAULT 'US',
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT unique_ticker_date_history UNIQUE (ticker, created_at)
);

-- 📌 관심 종목 테이블 (별칭 & 활성화 상태 추가)
CREATE TABLE IF NOT EXISTS watchlist (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    alias VARCHAR(50) DEFAULT '',  -- ✅ 별칭 추가
    is_active BOOLEAN DEFAULT TRUE,  -- ✅ 모니터링 활성화 여부 추가
    data_source VARCHAR(10) DEFAULT 'NAVER',  -- ✅ 데이터 소스 추가
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ 기존 `watchlist` 테이블 변경 사항 적용
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'watchlist' AND column_name = 'alias') THEN
        ALTER TABLE watchlist ADD COLUMN alias VARCHAR(50) DEFAULT '';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'watchlist' AND column_name = 'is_active') THEN
        ALTER TABLE watchlist ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'watchlist' AND column_name = 'data_source') THEN
        ALTER TABLE watchlist ADD COLUMN data_source VARCHAR(10) DEFAULT 'NAVER';
    END IF;
END $$;

-- 📌 AI 예측 결과 저장 테이블
CREATE TABLE IF NOT EXISTS ai_predictions (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    predicted_price NUMERIC(10,2) NOT NULL,
    prediction_period VARCHAR(10) NOT NULL,  -- ✅ 예측 기간 (1D, 1W, 1M 등)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 📌 Quant 분석 결과 저장 테이블
CREATE TABLE IF NOT EXISTS quant_results (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    analysis_result NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 📌 주식 그룹 테이블 (예: AI 관련, 방산 관련 등)
CREATE TABLE IF NOT EXISTS stock_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 📌 주식과 그룹을 연결하는 테이블
CREATE TABLE IF NOT EXISTS stock_group_mapping (
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES stock_groups(id),
    ticker VARCHAR(10) REFERENCES watchlist(ticker)
);

-- 📌 초기 주식 그룹 데이터 추가
INSERT INTO stock_groups (name) VALUES 
('AI 관련'), 
('방산 관련'), 
('IT 대기업'), 
('반도체') 
ON CONFLICT (name) DO NOTHING;

-- 📌 초기 관심 종목 데이터 추가 (중복 방지)
INSERT INTO watchlist (ticker, alias, is_active, data_source, created_at)
VALUES
    ('NVDL', 'NVIDIA ETF', TRUE, 'TWELVE', NOW()),
    ('012450.KS', '한화에어로스페이스', TRUE, 'NAVER', NOW()),
    ('^IXIC', 'NASDAQ Composite', TRUE, 'TWELVE', NOW()),
    ('^KQ11', 'KOSDAQ Index', TRUE, 'NAVER', NOW()),
    ('^GSPC', 'S&P 500', TRUE, 'TWELVE', NOW())
ON CONFLICT (ticker) DO NOTHING;
