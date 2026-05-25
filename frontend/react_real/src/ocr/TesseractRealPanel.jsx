import React, { useEffect, useState } from "react";
import { API, getJson } from "../api/apiClient";

export default function TesseractRealPanel() {

    const [dashboard, setDashboard] = useState(null);
    const [resultat, setResultat] = useState(null);
    const [loading, setLoading] = useState(false);

    async function loadDashboard() {

        try {

            const response = await getJson("/tesseract/dashboard");

            if (response.success) {
                setDashboard(response.data);
            }

        } catch (e) {
            console.error(e);
        }
    }

    async function lancerOCR() {

        setLoading(true);

        try {

            const formData = new FormData();

            formData.append(
                "nom_fichier",
                "facture_reelle_demo.pdf"
            );

            const response = await API.post(
                "/tesseract/analyse",
                formData
            );

            setResultat(response.data);

            await loadDashboard();

        } catch (e) {

            setResultat({
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

            <h2>OCR Tesseract Réel</h2>

            {dashboard && (

                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                    gap: "14px",
                    marginTop: "18px"
                }}>

                    <Card
                        label="Documents OCR"
                        value={dashboard.documents}
                    />

                    <Card
                        label="Moteur"
                        value="TESSERACT"
                    />

                </div>
            )}

            <button
                onClick={lancerOCR}
                disabled={loading}
                style={{
                    background: "#16a34a",
                    color: "white",
                    border: 0,
                    padding: "12px 16px",
                    borderRadius: "12px",
                    cursor: "pointer",
                    fontWeight: "bold",
                    marginTop: "18px"
                }}
            >

                {loading ? "OCR en cours..." : "Lancer OCR"}

            </button>

            {resultat && (

                <pre style={{
                    background: "#020617",
                    padding: "16px",
                    borderRadius: "12px",
                    marginTop: "18px",
                    whiteSpace: "pre-wrap"
                }}>

                    {JSON.stringify(resultat, null, 2)}

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
                color: "#4ade80"
            }}>
                {value}
            </div>

        </div>
    );
}
