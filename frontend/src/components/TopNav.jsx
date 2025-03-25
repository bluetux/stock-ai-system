import React from "react";
import { useNavigate } from "react-router-dom";
import {
  PawPrint,
  ChartCandlestick,
  Settings,
  CircleUserRound,
} from "lucide-react";

const TopNav = () => {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-between bg-main border-b border-gray-300 px-6 py-3 shadow-sm">
      {/* 왼쪽 - 로고 */}
      <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate("/")}>
        <PawPrint className="w-6 h-6 text-black" />
        <span className="text-lg font-semibold text-black">우리코난 AI 시스템</span>
      </div>

      {/* 오른쪽 - 메뉴 */}
      <div className="flex gap-6 items-center text-sm font-medium text-gray-700">
        <div className="flex gap-1 items-center cursor-pointer" onClick={() => navigate("/dashboard")}>
          <ChartCandlestick size={16} />
          <span>주식 분석</span>
        </div>
        <div className="flex gap-1 items-center cursor-pointer" onClick={() => navigate("/dashboard/settings/watchlist")}>
          <Settings size={16} />
          <span>설정</span>
        </div>
        <div className="flex gap-1 items-center cursor-pointer" onClick={() => navigate("/account")}>
          <CircleUserRound size={16} />
          <span>계정</span>
        </div>
      </div>
    </div>
  );
};

export default TopNav;