import React from "react";
import SidebarOne from "../SidebarOne";
import SidebarTwo from "../SidebarTwo";
import { Routes, Route } from "react-router-dom";
import Dashboard from "../../pages/Dashboard";
import StockDetailPage from "../../pages/StockDetailPage";
import GroupDashboardPage from "../../pages/GroupDashboardPage";

const SidebarLayout = () => {
  return (
    <div className="flex flex-1 overflow-hidden">
      <SidebarOne />
      <SidebarTwo />
      <div className="flex-1 overflow-y-auto p-4">
        <Routes>
          <Route path="" element={<Dashboard />} />
          <Route path="group/:groupId" element={<GroupDashboardPage />} />
          <Route path="stocks/:ticker" element={<StockDetailPage />} />
        </Routes>
      </div>
    </div>
  );
};

export default SidebarLayout;
