import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

// 📌 통화 포맷 유틸 함수
const formatCurrency = (value, region, exchangeRate, displayCurrency) => {
  if (value == null) return "-";

  let amount = value;
  if (region === "미국" && displayCurrency === "KRW" && exchangeRate) {
    amount = value * exchangeRate;
  }

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
  const [displayCurrency, setDisplayCurrency] = useState("USD");
  const [exchangeRate, setExchangeRate] = useState(null);

  useEffect(() => {
    fetch(`/api/stocks/${ticker}`)
      .then((res) => res.json())
      .then((data) => setStock(data))
      .catch((err) => console.error("❌ 종목 데이터 오류:", err));

    fetch("/api/exchange/usd-krw")
      .then((res) => res.json())
      .then((data) => setExchangeRate(data.usd_krw))
      .catch((err) => console.error("❌ 환율 데이터 오류:", err));
  }, [ticker]);

  if (!stock) {
    return (
      <div className="text-gray-500 p-6 text-center">종목 정보를 불러오는 중입니다...</div>
    );
  }

  const finalExchangeRate = stock.exchange_rate ?? exchangeRate;

  return (
    <div className="bg-white text-black min-h-screen p-6">
      {/* 헤더 */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-1">{stock.alias}</h1>
        <div className="text-sm text-gray-500">
          {stock.region} · {stock.ticker}
        </div>
      </div>

      {/* ✅ 가격 및 상태 박스 */}
      <div className="bg-white p-6 shadow rounded-lg border mb-6">
        <div className="flex justify-between items-center">
          <div>
            <div className="text-4xl font-bold text-gray-800 mb-2">
              {formatCurrency(stock.price, stock.region, finalExchangeRate, displayCurrency)}
            </div>
            <div className="text-sm text-gray-500">현재가 기준</div>
            <div className="mt-2 text-sm text-gray-500">
              시장 상태:{" "}
              <span className={stock.is_open ? "text-green-600" : "text-red-500"}>
                {stock.is_open ? "장 열림" : "장 마감"}
              </span>
            </div>
          </div>

          {stock.region === "미국" && (
            <div>
              <label className="text-sm text-gray-600 mr-2">표시 통화:</label>
              <select
                value={displayCurrency}
                onChange={(e) => setDisplayCurrency(e.target.value)}
                className="border border-gray-300 text-sm rounded px-2 py-1"
              >
                <option value="USD">$ USD</option>
                <option value="KRW">₩ 원화</option>
              </select>
            </div>
          )}
        </div>
      </div>

      {/* ✅ 상세 정보 박스 */}
      <div className="bg-gray-50 p-5 rounded-lg border shadow-sm">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>시가: <span className="font-medium">{formatCurrency(stock.open, stock.region, finalExchangeRate, displayCurrency)}</span></div>
          <div>고가: <span className="font-medium">{formatCurrency(stock.high, stock.region, finalExchangeRate, displayCurrency)}</span></div>
          <div>저가: <span className="font-medium">{formatCurrency(stock.low, stock.region, finalExchangeRate, displayCurrency)}</span></div>
          <div>거래량: <span className="font-medium">{stock.volume?.toLocaleString() ?? "-"}</span></div>
          <div>전일 종가: <span className="font-medium">{formatCurrency(stock.previous_close, stock.region, finalExchangeRate, displayCurrency)}</span></div>
        </div>
      </div>
    </div>
  );
};

export default StockDetailPage;