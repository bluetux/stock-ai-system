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

-- 📌 주가 데이터 테이블 (1년치 데이터 저장 가능)
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ UNIQUE 제약 조건 추가 (기존 DB에서도 자동 적용됨)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'unique_ticker_date') THEN
        ALTER TABLE stock_data ADD CONSTRAINT unique_ticker_date UNIQUE (ticker, created_at);
    END IF;
END $$;

-- 📌 관심 종목 테이블 (별칭 & 활성화 상태 추가)
CREATE TABLE IF NOT EXISTS watchlist (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    alias VARCHAR(50) DEFAULT '',  -- ✅ 별칭 추가
    is_active BOOLEAN DEFAULT TRUE,  -- ✅ 모니터링 활성화 여부 추가
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ 기존 DB에서도 `watchlist` 테이블 변경 사항이 적용되도록 설정
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'watchlist' AND column_name = 'alias') THEN
        ALTER TABLE watchlist ADD COLUMN alias VARCHAR(50) DEFAULT '';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'watchlist' AND column_name = 'is_active') THEN
        ALTER TABLE watchlist ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
    END IF;
END $$;

-- 📌 AI 예측 결과 저장 테이블 (과거 데이터도 유지)
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
-- 주식 데이터 테이블 (미국/한국 주식 구분 추가)
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    country VARCHAR(10) CHECK (country IN ('US', 'KR')) NOT NULL DEFAULT 'US',
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_ticker_date UNIQUE (ticker, created_at)  -- ✅ UNIQUE 추가
);

-- 주식 그룹 테이블 추가 (예: AI 관련, 방산 관련 등)
CREATE TABLE IF NOT EXISTS stock_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 주식과 그룹을 연결하는 테이블
CREATE TABLE IF NOT EXISTS stock_group_mapping (
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES stock_groups(id),
    ticker VARCHAR(10) REFERENCES stock_data(ticker)
);

CREATE TABLE IF NOT EXISTS stock_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 초기 그룹 데이터 추가
INSERT INTO stock_groups (name) VALUES 
('AI 관련'), 
('방산 관련'), 
('IT 대기업'), 
('반도체') 
ON CONFLICT (name) DO NOTHING;


-- 📌 초기 관심 종목 데이터 추가 (중복 방지)
INSERT INTO watchlist (ticker, alias, is_active, created_at)
VALUES
    ('NVDL', 'NVIDIA ETF', TRUE, NOW()),
    ('012450.KS', '한화에어로스페이스', TRUE, NOW())
    ('^IXIC', 'NASDAQ Composite', TRUE, NOW()),
    ('^KQ11', 'KOSDAQ Index', TRUE, NOW())
ON CONFLICT (ticker) DO NOTHING;
