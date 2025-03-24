import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import React from "react";

// 📌 통화 포맷 유틸 함수
const formatCurrency = (value, region, exchangeRate, displayCurrency) => {
    if (value == null) return "-";

    let amount = value;

    // 미국 주식 + KRW 표시일 경우 환산
    if (region === "미국" && displayCurrency === "KRW" && exchangeRate) {
        amount = value * exchangeRate;
    }

    // 소수점 처리 & 천 단위 콤마
    const formatted = amount.toLocaleString(region === "미국" ? "en-US" : "ko-KR", {
        minimumFractionDigits: region === "미국" ? 2 : 0,
        maximumFractionDigits: region === "미국" ? 2 : 0,
    });

    if (region === "미국") {
        return displayCurrency === "KRW" ? `${formatted}원` : `$${formatted}`;
    } else {
        return `${formatted}원`;
    }
};

const StockDetailPage = () => {
    const { ticker } = useParams();
    const [stock, setStock] = useState(null);
    const [displayCurrency, setDisplayCurrency] = useState("USD"); // 기본: USD
    const [exchangeRate, setExchangeRate] = useState(null);

    useEffect(() => {
        // 종목 데이터
        fetch(`/api/stocks/${ticker}`)
            .then((res) => res.json())
            .then((data) => setStock(data))
            .catch((err) => console.error("❌ 종목 데이터 오류:", err));

        // 환율 데이터
        fetch("/api/exchange/usd-krw")
            .then(res => res.json())
            .then(data => {
                console.log("💱 환율 데이터:", data);
                setExchangeRate(data.usd_krw);
            });
    }, [ticker]);

    if (!stock) return <div className="text-white p-6">종목 정보를 불러오는 중입니다...</div>;

    // 환율 보정: stock.exchange_rate가 없으면 외부에서 받은 exchangeRate 사용
    const finalExchangeRate = stock.exchange_rate ?? exchangeRate;

    return (
        <div className="bg-[#2a2f3a] text-white min-h-screen p-6">
            {/* 헤더 영역 */}
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-white mb-2">{stock.alias}</h1>
                <div className="text-gray-300 text-sm">
                    {stock.region} · {stock.ticker}
                </div>
            </div>

            {/* 가격 및 시장 상태 */}
            <div className="bg-gray-800 p-6 rounded-md shadow-md mb-6">
                <div className="flex justify-between items-center">
                    <div>
                        <div className="text-4xl font-bold text-white mb-2">
                            {formatCurrency(stock.price, stock.region, finalExchangeRate, displayCurrency)}
                        </div>
                        <div className="text-sm text-gray-400">현재가 기준</div>
                        <div className="mt-2 text-sm text-gray-400">
                            시장 상태:{" "}
                            <span className={stock.is_open ? "text-green-400" : "text-red-400"}>
                                {stock.is_open ? "장 열림" : "장 마감"}
                            </span>
                        </div>
                    </div>

                    {stock.region === "미국" && (
                        <div>
                            <label className="text-sm text-gray-300 mr-2">표시 통화:</label>
                            <select
                                value={displayCurrency}
                                onChange={(e) => setDisplayCurrency(e.target.value)}
                                className="bg-gray-700 text-white p-1 rounded"
                            >
                                <option value="USD">$ USD</option>
                                <option value="KRW">₩ 원화</option>
                            </select>
                        </div>
                    )}
                </div>
            </div>

            {/* 상세 정보 */}
            <div className="bg-gray-700 p-4 rounded-md shadow">
                <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>시가: <span className="text-white">{formatCurrency(stock.open, stock.region, finalExchangeRate, displayCurrency)}</span></div>
                    <div>고가: <span className="text-white">{formatCurrency(stock.high, stock.region, finalExchangeRate, displayCurrency)}</span></div>
                    <div>저가: <span className="text-white">{formatCurrency(stock.low, stock.region, finalExchangeRate, displayCurrency)}</span></div>
                    <div>거래량: <span className="text-white">{stock.volume?.toLocaleString() ?? "-"}</span></div>
                    <div>전일 종가: <span className="text-white">{formatCurrency(stock.previous_close, stock.region, finalExchangeRate, displayCurrency)}</span></div>
                </div>
            </div>
        </div>
    );
};

export default StockDetailPage;
