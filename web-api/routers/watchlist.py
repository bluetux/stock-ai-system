from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from db import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/api/watchlist", tags=["Watchlist"])

# ✅ Pydantic 모델 정의
class WatchItem(BaseModel):
    ticker: str
    alias: str
    region: str
    is_active: bool
    icon: str
    group_ids: list[int] = []

# ✅ 관심종목 전체 조회
@router.get("/")
def get_watchlist(db=Depends(get_db)):
    rows = db.execute(text("SELECT * FROM watchlist")).mappings().all()

    # 각 종목에 대해 그룹 ID 조회 추가
    enriched = []
    for row in rows:
        group_rows = db.execute(
            text("SELECT group_id FROM stock_group_mapping WHERE ticker = :ticker"),
            {"ticker": row["ticker"]}
        ).mappings().all()

        group_ids = [gr["group_id"] for gr in group_rows]
        enriched.append({**row, "group_ids": group_ids})

    return {"watchlist": enriched}

# ✅ 관심종목 추가/수정
@router.post("/")
def save_watch_item(item: WatchItem, db=Depends(get_db)):
    # 기존 데이터 존재 여부 확인
    existing = db.execute(
        text("SELECT * FROM watchlist WHERE ticker = :ticker"),
        {"ticker": item.ticker}
    ).fetchone()

    if existing:
        # ✅ 업데이트
        db.execute(
            text("""
                UPDATE watchlist
                SET alias = :alias,
                    region = :region,
                    is_active = :is_active,
                    icon = :icon
                WHERE ticker = :ticker
            """),
            item.dict()
        )
    else:
        # ✅ 새로 추가
        db.execute(
            text("""
                INSERT INTO watchlist (ticker, alias, region, is_active, icon)
                VALUES (:ticker, :alias, :region, :is_active, :icon)
            """),
            item.dict()
        )

    # ✅ 기존 그룹 매핑 삭제
    db.execute(
        text("DELETE FROM stock_group_mapping WHERE ticker = :ticker"),
        {"ticker": item.ticker}
    )

    # ✅ 새로운 그룹 매핑 추가
    for group_id in item.group_ids:
        db.execute(
            text("INSERT INTO stock_group_mapping (ticker, group_id) VALUES (:ticker, :group_id)"),
            {"ticker": item.ticker, "group_id": group_id}
        )

    db.commit()
    return {"message": "Saved"}

# ✅ 관심종목 삭제
@router.delete("/{ticker}")
async def remove_from_watchlist(ticker: str, db=Depends(get_db)):
    # 삭제
    db.execute(
        text("DELETE FROM stock_group_mapping WHERE ticker = :ticker"),
        {"ticker": ticker}
    )
    db.execute(
        text("DELETE FROM watchlist WHERE ticker = :ticker"),
        {"ticker": ticker}
    )
    db.commit()
    return {"message": f"{ticker} removed from watchlist"}