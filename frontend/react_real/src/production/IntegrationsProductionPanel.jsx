import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function IntegrationsProductionPanel() {

    const [data, setData] = useState(null);

    useEffect(() => {
        async function load() {
            try {
                const response = await getJson("/integrations-production");

                if (response.success) {
                    setData(response.data);
                }
            } catch (e) {
                console.error(e);
            }
        }

        load();
        const timer = setInterval(load, 12000);
        return () => clearInterval(timer);
    }, []);

    if (!data) {
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
            <h2>Intégrations Production</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>
                {data.items.map((item) => (
                    <div key={item.id} style={{
                        background: "#111827",
                        borderRadius: "14px",
                        padding: "16px",
                        border: "1px solid #334155"
                    }}>
                        <strong>{item.integration}</strong>
                        <p>{item.message}</p>
                        <small>{item.statut} · {item.mode_execution}</small>
                    </div>
                ))}
            </div>
        </section>
    );
}
