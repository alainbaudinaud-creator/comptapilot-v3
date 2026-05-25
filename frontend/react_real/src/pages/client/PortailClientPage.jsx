import React from "react";

export default function PortailClientPage() {

    return (
        <section>
            <h2>Portail Client</h2>

            <div style={{
                background: "#0f172a",
                border: "1px solid #334155",
                borderRadius: "18px",
                padding: "24px"
            }}>
                <h3>Documents disponibles</h3>
                <p>Liasses, plaquettes, justificatifs, messages cabinet et notifications.</p>

                <ul>
                    <li>Plaquette annuelle 2025</li>
                    <li>Liasse fiscale 2025</li>
                    <li>Déclaration TVA</li>
                    <li>Factures électroniques PDP</li>
                </ul>
            </div>
        </section>
    );
}
