// src/components/layouts/DashboardLayout.jsx
import React, { useEffect, useState } from "react";
import SidebarOne from "./SidebarOne";
import SidebarTwo from "./SidebarTwo";
import { Outlet } from "react-router-dom";

const DashboardLayout = () => {
  const [groups, setGroups] = useState({});
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);

  useEffect(() => {
    fetch("/api/groups/")
      .then((res) => res.json())
      .then((data) => {
        setGroups(data);
        // 초기 region 설정
        if (Object.keys(data).length > 0) {
          setSelectedRegion(Object.keys(data)[0]);
        }
      })
      .catch((err) => console.error("그룹 로딩 실패:", err));
  }, []);

  return (
    <div className="flex h-full bg-main text-black">
      <SidebarOne
        groups={groups}
        selectedGroup={selectedGroup}
        setSelectedGroup={setSelectedGroup}
        selectedRegion={selectedRegion}
        setSelectedRegion={setSelectedRegion}
      />
      <SidebarTwo selectedGroup={selectedGroup} groups={groups} />
      <div className="flex-1 overflow-auto p-4 border-l border-gray-200">
        <div className="h-full">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;