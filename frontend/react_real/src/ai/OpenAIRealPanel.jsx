import React, { useEffect, useState } from "react";
import { API, getJson } from "../api/apiClient";

export default function OpenAIRealPanel() {

    const [dashboard, setDashboard] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    async function loadDashboard() {
        try {
            const data = await getJson("/openai/dashboard");

            if (data.success) {
                setDashboard(data.data);
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function lancerAnalyse() {
        setLoading(true);

        try {
            const response = await API.post("/openai/analyse-facture", {
                texte: "FACTURE TEST REACT HT 1000 TVA 200 TTC 1200 FOURNISSEUR PREMIUM"
            });

            setResult(response.data);
            await loadDashboard();

        } catch (e) {
            setResult({
                success: false,
                error: e.message
            });
        }

        setLoading(false);
    }

    useEffect(() => {
        loadDashboard();
    }, []);

    return (
        <section style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px",
            marginTop: "24px"
        }}>
            <h2>OpenAI Comptable Réel</h2>

            {dashboard && (
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                    gap: "14px",
                    marginTop: "18px"
                }}>
                    <Card label="Mode IA" value={dashboard.enabled ? "API ACTIVE" : "FALLBACK"} />
                    <Card label="Modèle" value={dashboard.model} />
                    <Card label="Analyses" value={dashboard.total} />
                </div>
            )}

            <button onClick={lancerAnalyse} disabled={loading} style={{
                background: "#7c3aed",
                color: "white",
                border: 0,
                padding: "12px 16px",
                borderRadius: "12px",
                cursor: "pointer",
                fontWeight: "bold",
                marginTop: "18px"
            }}>
                {loading ? "Analyse en cours..." : "Analyser facture avec OpenAI"}
            </button>

            {result && (
                <pre style={{
                    background: "#020617",
                    padding: "16px",
                    borderRadius: "12px",
                    marginTop: "18px",
                    whiteSpace: "pre-wrap"
                }}>
                    {JSON.stringify(result, null, 2)}
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
            <div style={{ color: "#94a3b8", marginBottom: "8px" }}>
                {label}
            </div>

            <div style={{
                fontSize: "22px",
                fontWeight: "bold",
                color: "#c4b5fd"
            }}>
                {value}
            </div>
        </div>
    );
}
