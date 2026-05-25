import React, { useEffect, useState } from "react";
import {
    websocketStats,
    websocketPush
} from "../live/websocketService";

export default function LiveDashboardPanel() {

    const [stats, setStats] = useState(null);
    const [events, setEvents] = useState([]);

    useEffect(() => {

        async function refresh() {

            try {

                const data = await websocketStats();

                if (data.success) {
                    setStats(data.stats);
                }

            } catch (e) {
                console.error(e);
            }
        }

        async function simulatePush() {

            try {

                const response = await websocketPush();

                if (response.success) {

                    setEvents((prev) => [
                        response.event,
                        ...prev
                    ].slice(0, 10));
                }

            } catch (e) {
                console.error(e);
            }
        }

        refresh();

        const statsTimer = setInterval(refresh, 5000);

        const pushTimer = setInterval(simulatePush, 8000);

        return () => {
            clearInterval(statsTimer);
            clearInterval(pushTimer);
        };

    }, []);

    return (

        <section style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px",
            marginTop: "24px"
        }}>

            <h2>Websocket Live Dashboard</h2>

            {stats && (

                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))",
                    gap: "14px",
                    marginTop: "16px"
                }}>

                    <Card
                        label="Sessions"
                        value={stats.sessions}
                    />

                    <Card
                        label="Messages"
                        value={stats.messages}
                    />

                    <Card
                        label="Latence"
                        value={`${stats.latency_ms} ms`}
                    />

                    <Card
                        label="Mode"
                        value={stats.websocket_status}
                    />

                </div>

            )}

            <div style={{
                marginTop: "24px"
            }}>

                <h3>Flux live</h3>

                {events.map((event, index) => (

                    <div
                        key={index}
                        style={{
                            background: "#111827",
                            padding: "12px",
                            borderRadius: "12px",
                            marginBottom: "10px"
                        }}
                    >
                        <strong>{event.event}</strong>

                        <p>{event.message}</p>

                        <small>{event.timestamp}</small>

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

            <div style={{
                color: "#94a3b8",
                marginBottom: "8px"
            }}>
                {label}
            </div>

            <div style={{
                fontSize: "24px",
                fontWeight: "bold",
                color: "#22c55e"
            }}>
                {value}
            </div>

        </div>
    );
}
