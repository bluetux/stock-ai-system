// 📁 frontend/src/components/layout/Layout.js
import React, { useState } from "react";
import SidebarPrimary from "./SidebarOne";
import SidebarSecondary from "./SidebarTwo";
import { Outlet } from "react-router-dom";

const Layout = () => {
  const [selectedCategory, setSelectedCategory] = useState("korea");
  const [selectedGroup, setSelectedGroup] = useState(null);

  const groups = {
    korea: [
      { id: "defense", name: "방산 관련", icon: "🛡️" },
      { id: "aerospace", name: "우주항공", icon: "🚀" },
    ],
    us: [
      { id: "it", name: "IT 대기업", icon: "💻" },
      { id: "semiconductor", name: "반도체", icon: "🔋" },
    ],
  };

  return (
    <div className="flex min-h-screen bg-gray-900 text-white">
      <SidebarPrimary
        selectedCategory={selectedCategory}
        onSelect={(id) => {
          setSelectedCategory(id);
          setSelectedGroup(null); // 그룹 초기화
        }}
      />
      <SidebarSecondary
        category={selectedCategory}
        groups={groups}
        selectedGroup={selectedGroup}
        onSelectGroup={setSelectedGroup}
      />
      <main className="flex-1 p-4 overflow-y-auto bg-gray-100 text-black">
        <Outlet context={{ selectedCategory, selectedGroup }} />
      </main>
    </div>
  );
};

export default Layout;
