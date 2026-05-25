import React, { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import Header from "./layout/Header";
import Sidebar from "./layout/Sidebar";
import CabinetPage from "./pages/cabinet/CabinetPage";
import PortailClientPage from "./pages/client/PortailClientPage";
import ProductionPage from "./pages/production/ProductionPage";
import { isAuthenticated, logout } from "./auth/authService";

export default function App() {

    const [logged, setLogged] = useState(isAuthenticated());
    const [page, setPage] = useState("dashboard");
    const [user, setUser] = useState({
        email: localStorage.getItem("comptapilot_user") || "admin@comptapilot.local"
    });

    function handleLogin(nextUser) {
        setUser(nextUser);
        setLogged(true);
    }

    function handleLogout() {
        logout();
        setLogged(false);
    }

    if (!logged) {
        return <LoginPage onLogin={handleLogin} />;
    }

    return (
        <div style={{
            display: "flex",
            minHeight: "100vh",
            background: "#020617",
            color: "#e5e7eb"
        }}>
            <Sidebar onNavigate={setPage} />

            <main style={{
                flex: 1,
                padding: "30px"
            }}>
                <Header user={user} onLogout={handleLogout} />

                {page === "dashboard" && <DashboardPage embedded />}
                {page === "cabinet" && <CabinetPage />}
                {page === "production" && <ProductionPage />}
                {page === "client" && <PortailClientPage />}
            </main>
        </div>
    );
}
