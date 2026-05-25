import React, { useEffect, useState } from "react";
import {
    websocketStats,
    websocketPush,
    websocketPushOCR
} from "../live/websocketService";

export default function SocketLivePanel() {

    const [stats, setStats] = useState(null);
    const [events, setEvents] = useState([]);

    async function refreshStats() {
        try {
            const data = await websocketStats();

            if (data.success) {
                setStats(data.stats);
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function pushDashboard() {
        try {
            const response = await websocketPush();

            if (response.success) {
                setEvents((prev) => [response.event, ...prev].slice(0, 12));
                refreshStats();
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function pushOCR() {
        try {
            const response = await websocketPushOCR("facture_live.pdf");

            if (response.success) {
                setEvents((prev) => [response.event, ...prev].slice(0, 12));
                refreshStats();
            }
        } catch (e) {
            console.error(e);
        }
    }

    useEffect(() => {
        refreshStats();

        const timer = setInterval(refreshStats, 5000);

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
            <h2>Live temps réel compatible</h2>

            {stats && (
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))",
                    gap: "14px",
                    marginTop: "16px"
                }}>
                    <Card label="Événements" value={stats.events} />
                    <Card label="Mode" value={stats.mode} />
                    <Card label="Statut" value={stats.status} />
                </div>
            )}

            <div style={{
                display: "flex",
                gap: "12px",
                marginTop: "18px"
            }}>
                <button onClick={pushDashboard} style={buttonStyle}>
                    Push Dashboard
                </button>

                <button onClick={pushOCR} style={buttonStyleSecondary}>
                    Push OCR
                </button>
            </div>

            <div style={{ marginTop: "24px" }}>
                {events.map((event, index) => (
                    <div key={index} style={{
                        background: "#111827",
                        borderRadius: "12px",
                        padding: "14px",
                        marginBottom: "10px"
                    }}>
                        <strong>{event.event}</strong>

                        <pre style={{ whiteSpace: "pre-wrap" }}>
                            {JSON.stringify(event, null, 2)}
                        </pre>
                    </div>
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

const buttonStyle = {
    background: "#2563eb",
    color: "white",
    border: 0,
    padding: "12px 16px",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold"
};

const buttonStyleSecondary = {
    ...buttonStyle,
    background: "#16a34a"
};
