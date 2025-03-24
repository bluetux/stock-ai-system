// src/components/layouts/DashboardLayout.jsx
import { Outlet } from "react-router-dom";
import TopNav from "../TopNav";
import SidebarOne from "./SidebarOne";
import SidebarTwo from "./SidebarTwo";

console.log("🧱 DashboardLayout 렌더 시작");

const DashboardLayout = () => {
  return (
    <div className="flex flex-col h-screen">
      <TopNav />
      <div className="flex flex-1 overflow-hidden">
        <SidebarOne />
        <SidebarTwo />
        <div className="flex-1 overflow-y-auto p-4">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
