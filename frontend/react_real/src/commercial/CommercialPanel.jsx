import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function CommercialPanel() {

    const [dashboard, setDashboard] = useState(null);
    const [action, setAction] = useState(null);

    async function refresh() {

        const response = await getJson(
            "/commercial/dashboard"
        );

        if (response.success) {
            setDashboard(response.data);
        }
    }

    async function lancer(endpoint) {

        const response = await getJson(endpoint);

        setAction(response);

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

            <h2>Commercialisation SaaS</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>

                <Card
                    label="Abonnements"
                    value={dashboard.abonnements}
                />

                <Card
                    label="Onboardings"
                    value={dashboard.onboardings}
                />

                <Card
                    label="Cloud Public"
                    value={dashboard.cloud_public}
                />

            </div>

            <div style={{
                display: "flex",
                gap: "12px",
                marginTop: "18px"
            }}>

                <button
                    onClick={() => lancer("/commercial/stripe")}
                    style={buttonBlue}
                >
                    Stripe SaaS
                </button>

                <button
                    onClick={() => lancer("/commercial/onboarding")}
                    style={buttonGreen}
                >
                    Onboarding
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
                color: "#06b6d4"
            }}>
                {value}
            </div>

        </div>
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
