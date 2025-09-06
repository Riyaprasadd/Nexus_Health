import { Route, Routes } from "react-router-dom";
import React from "react";
import "./i18n"; // language setup
import Sidebar from "./components/Sidebar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chatbot from "./pages/Chatbot";
import ResetPassword from "./pages/ResetPassword";
import ResetPasswordConfirm from "./pages/ResetPasswordConfirm";

// inside <Routes>
<Route path="/reset-password/confirm" element={<ResetPasswordConfirm />} />

function App() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar />
      <div style={{ flex: 1, padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/reset-password" element={<ResetPassword />} /> {/* ✅ reset link works */}
          <Route path="/reset-password/confirm" element={<ResetPasswordConfirm />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
