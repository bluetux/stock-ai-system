// src/App.jsx
// import React from "react";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import HomePage from "./pages/HomePage";
// import DashboardLayout from "./components/layouts/DashboardLayout";
// import Dashboard from "./pages/Dashboard";
// import StockDetailPage from "./pages/StockDetailPage";

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<HomePage />} />
//         <Route path="/dashboard" element={<DashboardLayout />}>
//           <Route index element={<Dashboard />} />
//           <Route path="stocks/:ticker" element={<StockDetailPage />} />
//         </Route>
//       </Routes>
//     </Router>
//   );
// }

// export default App;

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DashboardLayout from "./components/layouts/DashboardLayout";
import DashboardMain from "./pages/Dashboard";
import StockDetailPage from "./pages/StockDetailPage";
import SettingsLayout from "./components/layouts/SettingsLayout";
import WatchlistSettingsPage from "./pages/settings/WatchlistSettingsPage";
import GroupSettingsPage from "./pages/settings/GroupSettingsPage";
import AccountPage from "./pages/AccountPage";
import TopNav from "./components/TopNav";

function App() {
  return (
    <Router>
      <TopNav />
      <Routes>
        <Route path="/" element={<HomePage />} />

        {/* Dashboard (주식분석) */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardMain />} />
          <Route path="stocks/:ticker" element={<StockDetailPage />} />
        </Route>

        {/* Settings */}
        <Route path="/dashboard/settings" element={<SettingsLayout />}>
          <Route path="watchlist" element={<WatchlistSettingsPage />} />
          <Route path="groups" element={<GroupSettingsPage />} />
        </Route>

        {/* Account (아직 미구현) */}
        <Route path="/account" element={<AccountPage />} />
      </Routes>
    </Router>
  );
}

export default App;