// 📁 frontend/src/utils/currency.js

export const formatCurrency = (value, region) => {
    if (value === null || value === undefined || isNaN(value)) return "-";
    const num = Number(value);
    const symbol = region === "한국" ? "₩" : "$";
    return `${symbol}${num.toLocaleString()}`;
  };
  