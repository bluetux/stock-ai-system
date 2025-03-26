// 📌 파일 위치: frontend/src/pages/HomePage.js
import React from 'react';

function HomePage() {
  return (
    <div className="bg-gray-900 text-white h-full flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold mb-4">OurConan Stock Dashboard</h1>
      <p className="text-lg text-gray-300 mb-6">AI 기반 주식 분석 및 퀀트 투자 시스템</p>
      <div className="flex flex-wrap justify-center gap-4">
        <a href="/dashboard" className="border border-green-400 text-green-400 px-6 py-2 rounded hover:bg-green-400 hover:text-black transition">AI 분석 시스템</a>
        <a href="/comfy-ui" className="border border-green-400 text-green-400 px-6 py-2 rounded hover:bg-green-400 hover:text-black transition">Comfy UI</a>
        <a href="/jupyter" className="border border-green-400 text-green-400 px-6 py-2 rounded hover:bg-green-400 hover:text-black transition">Jupyter Notebook</a>
      </div>
    </div>
  );
}

export default HomePage;
