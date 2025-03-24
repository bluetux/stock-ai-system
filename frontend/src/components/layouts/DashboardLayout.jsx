import React, { useEffect, useState } from "react";
import SidebarOne from "../layouts/SidebarOne";
import SidebarTwo from "../layouts/SidebarTwo";
import TopNav from "../TopNav";
import { Outlet } from "react-router-dom";

const DashboardLayout = () => {
  const [groups, setGroups] = useState({});
  const [selectedRegion, setSelectedRegion] = useState(null);

  useEffect(() => {
    fetch("/api/groups")
      .then((res) => res.json())
      .then((data) => setGroups(data))
      .catch((err) => console.error("❌ 그룹 데이터 에러:", err));
  }, []);

  return (
    <div className="flex flex-col h-screen">
      <TopNav />
      <div className="flex flex-1 overflow-hidden">
        <SidebarOne
          groups={groups}
          selectedRegion={selectedRegion}
          setSelectedRegion={setSelectedRegion}
        />
        <SidebarTwo selectedRegion={selectedRegion} groups={groups} />
        <div className="flex-1 bg-white overflow-y-auto">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;

