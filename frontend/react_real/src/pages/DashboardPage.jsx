import React, { useEffect, useState } from "react";
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
        <section>
            <h2>Dashboard Temps Réel</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
                gap: "20px",
                marginTop: "20px"
            }}>
                {Object.entries(data).map(([endpoint, payload]) => (
                    <StatCard
                        key={endpoint}
                        title={endpoint}
                        value={payload.success ? "ONLINE" : "ERROR"}
                    />
                ))}
            </div>
        </section>
    );
}
