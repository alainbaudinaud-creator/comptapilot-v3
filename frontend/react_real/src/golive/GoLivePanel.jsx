import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function GoLivePanel() {

    const [dashboard, setDashboard] = useState(null);
    const [rapport, setRapport] = useState(null);

    async function refresh() {
        const response = await getJson("/go-live/dashboard");

        if (response.success) {
            setDashboard(response.data);
        }
    }

    async function genererRapport() {
        const response = await getJson("/go-live/rapport");
        setRapport(response);
        refresh();
    }

    useEffect(() => {
        refresh();
    }, []);

    if (!dashboard) {
        return null;
    }

    return (
        <section style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px",
            marginTop: "24px"
        }}>
            <h2>Go Live SaaS</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>
                <Card label="Readiness" value={`${dashboard.score_readiness} %`} />
                <Card label="Checks OK" value={`${dashboard.ok_checks}/${dashboard.total_checks}`} />
                <Card label="Statut" value={dashboard.statut} />
            </div>

            <button
                onClick={genererRapport}
                style={{
                    background: "#16a34a",
                    color: "white",
                    border: 0,
                    padding: "12px 16px",
                    borderRadius: "12px",
                    cursor: "pointer",
                    fontWeight: "bold",
                    marginTop: "18px"
                }}
            >
                Générer rapport Go Live
            </button>

            {rapport && (
                <pre style={{
                    background: "#020617",
                    padding: "14px",
                    borderRadius: "12px",
                    marginTop: "18px",
                    whiteSpace: "pre-wrap"
                }}>
                    {JSON.stringify(rapport, null, 2)}
                </pre>
            )}
        </section>
    );
}

function Card({ label, value }) {
    return (
        <div style={{
            background: "#111827",
            borderRadius: "12px",
            padding: "14px"
        }}>
            <div style={{ color: "#94a3b8", marginBottom: "8px" }}>
                {label}
            </div>

            <div style={{
                fontSize: "22px",
                fontWeight: "bold",
                color: "#22c55e"
            }}>
                {value}
            </div>
        </div>
    );
}
