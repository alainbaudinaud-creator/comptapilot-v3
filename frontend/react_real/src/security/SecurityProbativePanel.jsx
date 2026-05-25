import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function SecurityProbativePanel() {

    const [data, setData] = useState(null);
    const [lastAction, setLastAction] = useState(null);

    async function refresh() {
        const response = await getJson("/securite-probatoire/dashboard");
        if (response.success) {
            setData(response.data);
        }
    }

    async function action(endpoint) {
        const response = await getJson(endpoint);
        setLastAction(response);
        await refresh();
    }

    useEffect(() => {
        refresh();
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
            <h2>Sécurité & Probatoire</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                gap: "14px",
                marginTop: "18px"
            }}>
                <Card label="Tenants" value={data.tenants} />
                <Card label="Audits" value={data.audits} />
                <Card label="Archives" value={data.archives} />
                <Card label="Signatures" value={data.signatures} />
            </div>

            <div style={{ display: "flex", gap: "12px", marginTop: "18px" }}>
                <button style={buttonStyle} onClick={() => action("/securite-probatoire/audit")}>
                    Audit légal
                </button>

                <button style={buttonStyleGreen} onClick={() => action("/securite-probatoire/archive")}>
                    Archiver document
                </button>

                <button style={buttonStylePurple} onClick={() => action("/securite-probatoire/signature")}>
                    Signer document
                </button>
            </div>

            {lastAction && (
                <pre style={{
                    background: "#020617",
                    padding: "14px",
                    borderRadius: "12px",
                    marginTop: "18px",
                    whiteSpace: "pre-wrap"
                }}>
                    {JSON.stringify(lastAction, null, 2)}
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
            <div style={{ color: "#94a3b8", marginBottom: "8px" }}>{label}</div>
            <div style={{ fontSize: "22px", fontWeight: "bold", color: "#22c55e" }}>{value}</div>
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

const buttonStyleGreen = { ...buttonStyle, background: "#16a34a" };
const buttonStylePurple = { ...buttonStyle, background: "#7c3aed" };
