// 📁 frontend/src/components/TopNav.js
import React from "react";

const TopNav = () => {
  return (
    <div className="bg-[#1f2937] text-white h-12 flex items-center justify-between px-4">
      <div className="font-bold text-lg">📊 AI 분석 시스템</div>
      <div className="space-x-4 text-sm">
        <button>주식 분석</button>
        <button>설정</button>
        <button>계정 설정</button>
      </div>
    </div>
  );
};

export default TopNav;
