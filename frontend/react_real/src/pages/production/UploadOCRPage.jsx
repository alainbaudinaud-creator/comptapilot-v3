import React, { useState } from "react";
import { postForm, getJson } from "../../api/apiClient";

export default function UploadOCRPage() {

    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    async function lancerDemoOCR() {
        setError("");

        try {
            const data = await getJson("/ocr-ia/demo");
            setResult(data);
        } catch (e) {
            setError("Erreur pendant la démo OCR IA.");
        }
    }

    async function envoyerFichier() {
        setError("");

        if (!file) {
            setError("Choisis une pièce à analyser.");
            return;
        }

        try {
            const formData = new FormData();
            formData.append("piece", file);

            const data = await postForm("/ocr-ia/upload", formData);
            setResult(data);

        } catch (e) {
            setError("Upload OCR non disponible côté API pour le moment.");
        }
    }

    return (
        <section>
            <h2>Upload OCR IA</h2>

            <div style={{
                background: "#0f172a",
                border: "1px solid #334155",
                borderRadius: "18px",
                padding: "24px"
            }}>
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                    style={{ marginBottom: "16px" }}
                />

                <div style={{ display: "flex", gap: "12px" }}>
                    <button onClick={envoyerFichier} style={buttonStyle}>
                        Analyser la pièce
                    </button>

                    <button onClick={lancerDemoOCR} style={buttonStyleSecondary}>
                        Démo OCR IA
                    </button>
                </div>

                {error && (
                    <p style={{ color: "#fca5a5" }}>{error}</p>
                )}

                {result && (
                    <pre style={{
                        marginTop: "20px",
                        background: "#020617",
                        padding: "16px",
                        borderRadius: "12px",
                        whiteSpace: "pre-wrap"
                    }}>
                        {JSON.stringify(result, null, 2)}
                    </pre>
                )}
            </div>
        </section>
    );
}

const buttonStyle = {
    background: "#16a34a",
    color: "white",
    border: 0,
    padding: "12px 16px",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold"
};

const buttonStyleSecondary = {
    ...buttonStyle,
    background: "#2563eb"
};
