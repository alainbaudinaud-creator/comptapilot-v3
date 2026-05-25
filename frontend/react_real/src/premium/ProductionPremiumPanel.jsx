import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function ProductionPremiumPanel() {

    const [stats, setStats] = useState(null);

    useEffect(() => {

        async function load() {

            try {

                const response = await getJson("/production-premium");

                if (response.success) {
                    setStats(response.stats);
                }

            } catch (e) {
                console.error(e);
            }
        }

        load();

        const timer = setInterval(load, 7000);

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

            <h2>Production Premium</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(200px,1fr))",
                gap: "14px",
                marginTop: "20px"
            }}>

                <Card label="OCR Docs" value={stats.ocr_documents} />
                <Card label="OpenAI" value={stats.openai_analyses} />
                <Card label="Exports FEC" value={stats.exports_fec} />
                <Card label="PDF" value={stats.pdf_generes} />
                <Card label="CPU %" value={stats.cpu_usage} />
                <Card label="RAM %" value={stats.ram_usage} />

            </div>

            <div style={{
                marginTop: "28px"
            }}>

                <h3>Logs production</h3>

                {stats.logs.map((log) => (

                    <div
                        key={log.id}
                        style={{
                            background: "#111827",
                            padding: "14px",
                            borderRadius: "12px",
                            marginBottom: "10px"
                        }}
                    >

                        <strong>{log.type_traitement}</strong>

                        <p>{log.fichier}</p>

                        <small>{log.resultat} · {log.statut}</small>

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
                color: "#38bdf8"
            }}>
                {value}
            </div>

        </div>
    );
}
