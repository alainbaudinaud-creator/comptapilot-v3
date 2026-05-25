import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function WorkersPanel() {

    const [dashboard, setDashboard] = useState(null);
    const [logs, setLogs] = useState([]);

    async function refreshDashboard() {

        try {

            const response = await getJson("/orchestration/dashboard");

            if (response.success) {
                setDashboard(response.data);
            }

        } catch (e) {
            console.error(e);
        }
    }

    async function lancerPDF() {

        const response = await getJson("/orchestration/pdf");

        if (response.success) {

            setLogs(prev => [
                response.resultat,
                ...prev
            ]);

            refreshDashboard();
        }
    }

    async function lancerExcel() {

        const response = await getJson("/orchestration/excel");

        if (response.success) {

            setLogs(prev => [
                response.resultat,
                ...prev
            ]);

            refreshDashboard();
        }
    }

    useEffect(() => {

        refreshDashboard();

        const timer = setInterval(
            refreshDashboard,
            8000
        );

        return () => clearInterval(timer);

    }, []);

    return (

        <section style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px",
            marginTop: "24px"
        }}>

            <h2>Workers Redis / Celery</h2>

            {dashboard && (

                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                    gap: "14px",
                    marginTop: "18px"
                }}>

                    <Card label="Redis" value={dashboard.redis} />
                    <Card label="Celery" value={dashboard.celery} />
                    <Card label="Workers" value={dashboard.workers} />

                </div>
            )}

            <div style={{
                display: "flex",
                gap: "12px",
                marginTop: "18px"
            }}>

                <button
                    onClick={lancerPDF}
                    style={buttonStyle}
                >
                    Générer PDF
                </button>

                <button
                    onClick={lancerExcel}
                    style={buttonStyleExcel}
                >
                    Générer Excel
                </button>

            </div>

            <div style={{
                marginTop: "22px"
            }}>

                {logs.map((log, index) => (

                    <pre
                        key={index}
                        style={{
                            background: "#020617",
                            padding: "12px",
                            borderRadius: "12px",
                            marginBottom: "10px",
                            whiteSpace: "pre-wrap"
                        }}
                    >

                        {JSON.stringify(log, null, 2)}

                    </pre>

                ))}

            </div>

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

            <div style={{
                color: "#94a3b8",
                marginBottom: "8px"
            }}>
                {label}
            </div>

            <div style={{
                fontSize: "22px",
                fontWeight: "bold",
                color: "#f59e0b"
            }}>
                {value}
            </div>

        </div>
    );
}

const buttonStyle = {
    background: "#2563eb",
    color: "white",
    border: 0,
    padding: "12px 16px",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold"
};

const buttonStyleExcel = {
    ...buttonStyle,
    background: "#16a34a"
};
