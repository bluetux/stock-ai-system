from fastapi import APIRouter, Depends
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/groups", tags=["Groups"])

@router.get("/")
def get_groups_with_stocks(db=Depends(get_db)):
    # 1. 그룹에 속한 종목들
    group_query = text("""
        SELECT 
            g.id AS group_id,
            g.name AS group_name,
            w.region,
            g.icon,
            w.ticker,
            w.alias
        FROM stock_group_mapping m
        JOIN watchlist w ON m.ticker = w.ticker
        JOIN stock_groups g ON m.group_id = g.id
        ORDER BY w.region, g.name, w.alias;
    """)
    group_rows = db.execute(group_query).mappings().all()

    grouped = {}

    for row in group_rows:
        region = row["region"]
        group_id = row["group_id"]

        if region not in grouped:
            grouped[region] = {}

        if group_id not in grouped[region]:
            grouped[region][group_id] = {
                "id": group_id,
                "name": row["group_name"],
                "icon": row["icon"],
                "stocks": [],
            }

        grouped[region][group_id]["stocks"].append({
            "ticker": row["ticker"],
            "alias": row["alias"]
        })

    # 2. 전체 종목 리스트
    all_stocks_query = text("SELECT ticker, alias, region FROM watchlist")
    all_stocks = db.execute(all_stocks_query).mappings().all()

    # 3. 이미 그룹에 속한 종목들 set
    grouped_tickers = {row["ticker"] for row in group_rows}

    # 4. 미소속 종목을 ETC 그룹에 추가
    for stock in all_stocks:
        if stock["ticker"] not in grouped_tickers:
            region = stock["region"]
            if region not in grouped:
                grouped[region] = {}

            if 0 not in grouped[region]:  # group_id 0 → ETC
                grouped[region][0] = {
                    "id": 0,
                    "name": "ETC",
                    "icon": "folder",
                    "stocks": []
                }

            grouped[region][0]["stocks"].append({
                "ticker": stock["ticker"],
                "alias": stock["alias"]
            })

    return grouped