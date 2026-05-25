import React from "react";
import ReactDOM from "react-dom/client";

import AppShell from "./layouts/AppShell";
import Sidebar from "./layouts/Sidebar";
import DashboardPage from "./pages/DashboardPage";

function App() {

    return (

        <AppShell>

            <Sidebar />

            <main style={{
                flex: 1,
                padding: "32px"
            }}>

                <DashboardPage />

            </main>

        </AppShell>
    );
}

ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <App />
);
