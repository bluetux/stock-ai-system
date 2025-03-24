// import React from "react";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import HomePage from "./pages/HomePage";
// import DashboardLayout from "./components/layouts/DashboardLayout";
// import Dashboard from "./pages/Dashboard";
// import StockDetailPage from "./pages/StockDetailPage";

// console.log("✅ App.jsx: Component Loaded"); // ← 여기 추가

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<HomePage />} />

//         {/* ✅ Layout with nested routes */}
//         <Route path="/dashboard/*" element={<DashboardLayout />}>
//           <Route index element={<Dashboard />} />
//           <Route path="stocks/:ticker" element={<StockDetailPage />} />
//         </Route>
//       </Routes>
//     </Router>
//   );
// }

// export default App;

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";

console.log("🔥 App.jsx 렌더");

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
