import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function EnterprisePanel() {

    const [dashboard, setDashboard] = useState(null);
    const [action, setAction] = useState(null);

    async function refresh() {

        const response = await getJson(
            "/enterprise/dashboard"
        );

        if (response.success) {
            setDashboard(response.data);
        }
    }

    async function lancer(endpoint) {

        const response = await getJson(endpoint);

        setAction(response);
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

            <h2>Enterprise Grade</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>

                {dashboard.modules.map((m, index) => (

                    <div
                        key={index}
                        style={{
                            background: "#111827",
                            borderRadius: "12px",
                            padding: "14px"
                        }}
                    >

                        <strong>{m.module}</strong>

                        <p>{m.detail}</p>

                        <small>
                            {m.statut} · {m.niveau}
                        </small>

                    </div>

                ))}

            </div>

            <div style={{
                display: "flex",
                gap: "12px",
                marginTop: "18px"
            }}>

                <button
                    onClick={() => lancer("/enterprise/mfa")}
                    style={buttonBlue}
                >
                    MFA
                </button>

                <button
                    onClick={() => lancer("/enterprise/backup")}
                    style={buttonGreen}
                >
                    Backup Cloud
                </button>

                <button
                    onClick={() => lancer("/enterprise/predictif")}
                    style={buttonPurple}
                >
                    IA Predictive
                </button>

            </div>

            {action && (

                <pre style={{
                    background: "#020617",
                    padding: "14px",
                    borderRadius: "12px",
                    marginTop: "18px",
                    whiteSpace: "pre-wrap"
                }}>

                    {JSON.stringify(action, null, 2)}

                </pre>

            )}

        </section>
    );
}

const buttonBlue = {
    background: "#2563eb",
    color: "white",
    border: 0,
    padding: "12px 16px",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold"
};

const buttonGreen = {
    ...buttonBlue,
    background: "#16a34a"
};

const buttonPurple = {
    ...buttonBlue,
    background: "#7c3aed"
};
