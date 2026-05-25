import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function ReglementairePanel() {

    const [dashboard, setDashboard] = useState(null);
    const [action, setAction] = useState(null);

    async function refresh() {

        const response = await getJson(
            "/reglementaire/dashboard"
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

            <h2>Réglementaire & Banking</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>

                <Card
                    label="DSP2"
                    value={dashboard.banques_connectees}
                />

                <Card
                    label="PEPPOL/PDP"
                    value={dashboard.factures_peppol}
                />

                <Card
                    label="Statut"
                    value={dashboard.statut}
                />

            </div>

            <div style={{
                display: "flex",
                gap: "12px",
                marginTop: "18px"
            }}>

                <button
                    onClick={() => lancer("/reglementaire/dsp2")}
                    style={buttonBlue}
                >
                    DSP2
                </button>

                <button
                    onClick={() => lancer("/reglementaire/peppol")}
                    style={buttonGreen}
                >
                    PEPPOL
                </button>

                <button
                    onClick={() => lancer("/reglementaire/tva")}
                    style={buttonPurple}
                >
                    TVA IA
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
                color: "#f97316"
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

const buttonPurple = {
    ...buttonBlue,
    background: "#7c3aed"
};
