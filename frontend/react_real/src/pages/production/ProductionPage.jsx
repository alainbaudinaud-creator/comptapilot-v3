import React, { useState } from "react";
import { getJson } from "../../api/apiClient";

export default function ProductionPage() {

    const [result, setResult] = useState(null);

    async function lancerDemoOCR() {
        const data = await getJson("/ocr-ia/demo");
        setResult(data);
    }

    return (
        <section>
            <h2>Production Comptable IA</h2>

            <div style={{
                background: "#0f172a",
                border: "1px solid #334155",
                borderRadius: "18px",
                padding: "24px"
            }}>
                <p>
                    Pipeline : OCR → analyse facture → comptes → écriture équilibrée.
                </p>

                <button onClick={lancerDemoOCR} style={{
                    background: "#16a34a",
                    color: "white",
                    border: 0,
                    padding: "12px 16px",
                    borderRadius: "12px",
                    cursor: "pointer",
                    fontWeight: "bold"
                }}>
                    Lancer démo OCR IA
                </button>

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
