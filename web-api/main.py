# 📌 파일: web-api/main.py
from fastapi import FastAPI
from routers import ai, groups, quant, stocks, watchlist, exchange
import os

app = FastAPI(title="Stock Dashboard API")

# 라우터 등록
app.include_router(ai.router)
app.include_router(groups.router)
app.include_router(quant.router)
app.include_router(stocks.router)
app.include_router(watchlist.router)
app.include_router(exchange.router)

# 기본 루트
@app.get("/")
def read_root():
    return {"message": "Stock Dashboard API is running"}

@app.get("/debug/routes")
def debug_routes():
    return [route.path for route in app.routes]


# 실행 설정 (uvicorn 실행 시 자동 적용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
