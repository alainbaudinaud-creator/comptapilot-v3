import React, { useEffect, useState } from "react";
import Sidebar from "../layout/Sidebar";
import StatCard from "../widgets/StatCard";
import { chargerDashboard } from "../api/dashboardApi";

export default function DashboardPage() {

    const [data, setData] = useState({});

    useEffect(() => {

        async function load() {

            const result = await chargerDashboard();

            setData(result);
        }

        load();

    }, []);

    return (

        <div style={{
            display: "flex",
            background: "#020617",
            color: "#e5e7eb"
        }}>

            <Sidebar />

            <main style={{
                flex: 1,
                padding: "30px"
            }}>

                <h1>
                    Dashboard Temps Réel ComptaPilot V3
                </h1>

                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
                    gap: "20px",
                    marginTop: "30px"
                }}>

                    {Object.entries(data).map(([endpoint, payload]) => (

                        <StatCard
                            key={endpoint}
                            title={endpoint}
                            value={
                                payload.success
                                    ? "ONLINE"
                                    : "ERROR"
                            }
                        />

                    ))}

                </div>

            </main>

        </div>
    );
}
