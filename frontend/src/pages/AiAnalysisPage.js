// src/pages/AiAnalysisPage.js
import React, { useState } from 'react';
import TopNav from '../components/TopNav';
import Sidebar from '../components/Sidebar';
import AnalysisContent from '../components/AnalysisContent';

function AiAnalysisPage() {
  const [section, setSection] = useState('analysis');  // current tab

  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col">
      <TopNav current={section} onNavigate={setSection} />
      <div className="flex flex-1">
        {section === 'analysis' && <Sidebar />}
        <div className="flex-1 bg-gray-800">
          {section === 'analysis' && <AnalysisContent />}
          {section === 'settings' && <div className="p-6">🔧 설정 페이지 (곧 구현)</div>}
          {section === 'account' && <div className="p-6">👤 계정 설정 페이지 (곧 구현)</div>}
        </div>
      </div>
    </div>
  );
}

export default AiAnalysisPage;
