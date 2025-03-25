// src/components/layouts/DashboardLayout.jsx
import React, { useEffect, useState } from "react";
import SidebarOne from "./SidebarOne";
import SidebarTwo from "./SidebarTwo";
import { Outlet } from "react-router-dom";

const DashboardLayout = () => {
  const [groups, setGroups] = useState({});
  const [selectedGroup, setSelectedGroup] = useState(null);

  useEffect(() => {
    fetch("/api/groups/")
      .then((res) => res.json())
      .then((data) => setGroups(data))
      .catch((err) => console.error("그룹 로딩 실패:", err));
  }, []);

  return (
    <div className="flex h-screen bg-main text-black">
      <SidebarOne
        groups={groups}
        selectedGroup={selectedGroup}
        setSelectedGroup={setSelectedGroup}
      />
      <SidebarTwo selectedGroup={selectedGroup} groups={groups} />
      <div className="flex-1 overflow-y-auto p-4 border-l border-gray-200">
        <Outlet />
      </div>
    </div>
  );
};

export default DashboardLayout;