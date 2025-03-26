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
      <div className="flex flex-col h-screen">
        <TopNav />
        <main className="flex-1 overflow-auto">
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
        </main>
      </div>
    </Router>
  );
}

export default App;