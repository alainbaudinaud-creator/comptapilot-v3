import React, { useEffect, useState } from "react";

export default function CloudProductionPanel() {

    const [serverTime, setServerTime] = useState("");

    useEffect(() => {

        const timer = setInterval(() => {

            setServerTime(
                new Date().toISOString()
            );

        }, 1000);

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

            <h2>Cloud Production</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>

                <Card label="Redis" value="READY" />
                <Card label="Celery" value="READY" />
                <Card label="Grafana" value="READY" />
                <Card label="Prometheus" value="READY" />
                <Card label="Kubernetes" value="READY" />
                <Card label="CI/CD" value="READY" />

            </div>

            <div style={{
                marginTop: "18px",
                color: "#94a3b8"
            }}>
                Infrastructure cloud live : {serverTime}
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
                color: "#38bdf8"
            }}>
                {value}
            </div>

        </div>
    );
}
