import React from "react";
import { theme } from "../theme/theme";

export default function WelcomeHero() {

    return (
        <div
            className="fade-card"
            style={{
                background:
                    "linear-gradient(135deg, rgba(37,99,235,0.28), rgba(124,58,237,0.22))",
                border: `1px solid ${theme.colors.primaryLight}`,
                borderRadius: theme.radius.card,
                padding: "32px",
                marginBottom: "32px",
                position: "relative",
                overflow: "hidden"
            }}
        >

            <div style={{
                maxWidth: "760px",
                position: "relative",
                zIndex: 2
            }}>

                <div style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "10px",
                    background: "rgba(255,255,255,0.08)",
                    borderRadius: "999px",
                    padding: "8px 14px",
                    marginBottom: "20px",
                    fontWeight: "bold"
                }}>
                    ✨ ERP IA Nouvelle Génération
                </div>

                <h1 style={{
                    fontSize: "52px",
                    lineHeight: 1.05,
                    margin: 0,
                    letterSpacing: "-0.05em"
                }}>
                    Bienvenue dans
                    <br />
                    ComptaPilot V3
                </h1>

                <p style={{
                    marginTop: "22px",
                    color: theme.colors.textSecondary,
                    fontSize: "18px",
                    lineHeight: 1.7
                }}>
                    Centralisez votre production comptable,
                    votre conformité réglementaire,
                    vos automatisations IA
                    et votre pilotage financier
                    dans une seule plateforme moderne.
                </p>

                <div style={{
                    display: "flex",
                    gap: "14px",
                    flexWrap: "wrap",
                    marginTop: "28px"
                }}>

                    <button style={{
                        background:
                            "linear-gradient(135deg,#2563eb,#38bdf8)",
                        color: "white",
                        border: 0,
                        borderRadius: "14px",
                        padding: "14px 18px",
                        cursor: "pointer",
                        fontWeight: "bold"
                    }}>
                        Commencer le setup
                    </button>

                    <button style={{
                        background: "rgba(255,255,255,0.06)",
                        color: "white",
                        border: "1px solid rgba(255,255,255,0.08)",
                        borderRadius: "14px",
                        padding: "14px 18px",
                        cursor: "pointer",
                        fontWeight: "bold"
                    }}>
                        Voir la démo live
                    </button>

                </div>

            </div>

        </div>
    );
}
