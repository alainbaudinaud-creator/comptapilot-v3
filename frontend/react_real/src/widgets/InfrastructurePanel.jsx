import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function InfrastructurePanel() {

    const [stats, setStats] = useState(null);

    useEffect(() => {

        async function load() {

            try {

                const data = await getJson("/integrations");

                if (data.success) {
                    setStats(data.stats);
                }

            } catch (e) {
                console.error(e);
            }
        }

        load();

        const timer = setInterval(load, 5000);

        return () => clearInterval(timer);

    }, []);

    if (!stats) {
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

            <h2>Infrastructure Live</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))",
                gap: "14px",
                marginTop: "16px"
            }}>

                <Card label="OpenAI" value={stats.openai_requests} />
                <Card label="OCR Docs" value={stats.ocr_documents} />
                <Card label="Socket.IO" value={stats.socketio_events} />
                <Card label="Celery" value={stats.celery_jobs} />
                <Card label="CPU %" value={stats.cpu_usage} />
                <Card label="RAM %" value={stats.ram_usage} />

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
                color: "#38bdf8"
            }}>
                {value}
            </div>

        </div>
    );
}
