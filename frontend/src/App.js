import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./pages/HomePage";
import DashboardLayout from "./components/layouts/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import StockDetailPage from "./pages/StockDetailPage";

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/dashboard/*" element={<DashboardLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="stocks/:ticker" element={<StockDetailPage />} />
      </Route>
    </Routes>
  </Router>
);

export default App;
