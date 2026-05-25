import React from "react";
import ReactDOM from "react-dom/client";

import AppShell from "./layouts/AppShell";
import Sidebar from "./layouts/Sidebar";
import Header from "./layouts/Header";
import DashboardPage from "./pages/DashboardPage";

import { ToastProvider } from "./context/ToastContext";
import { CockpitProvider } from "./cockpit/CockpitContext";

function App() {
    return (
        <ToastProvider>

            <CockpitProvider>

                <AppShell>

                    <Sidebar />

                    <main
                        className="app-main"
                        style={{
                            flex: 1,
                            padding: "32px",
                            maxWidth: "1600px",
                            margin: "0 auto",
                            width: "100%"
                        }}
                    >
                        <Header />

                        <DashboardPage />

                    </main>

                </AppShell>

            </CockpitProvider>

        </ToastProvider>
    );
}

ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <App />
);
