import React from "react";
import {
  PawPrint,
  ChartCandlestick,
  Settings,
  CircleUserRound,
} from "lucide-react";

const TopNav = () => {
  return (
    <div className="flex items-center justify-between h-12 px-4 border-b border-gray-300 bg-">
      {/* 로고 및 시스템 이름 */}
      <div className="flex items-center space-x-2 font-bold text-lg text-black">
        <PawPrint className="w-5 h-5" />
        <span>우리코난 AI 시스템</span>
      </div>

      {/* 메뉴 항목 */}
      <div className="flex items-center space-x-6 text-sm text-gray-800">
        <div className="flex items-center gap-1 cursor-pointer hover:text-blue-600">
          <ChartCandlestick className="w-4 h-4" />
          <span>주식 분석</span>
        </div>
        <div className="flex items-center gap-1 cursor-pointer hover:text-blue-600">
          <Settings className="w-4 h-4" />
          <span>설정</span>
        </div>
        <div className="flex items-center gap-1 cursor-pointer hover:text-blue-600">
          <CircleUserRound className="w-4 h-4" />
          <span>계정</span>
        </div>
      </div>
    </div>
  );
};

export default TopNav;