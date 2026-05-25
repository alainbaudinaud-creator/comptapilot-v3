import React from "react";

import { theme } from "../theme/theme";

import { aiInsights } from "./insights";

export default function AICommandCenter() {

    function getColor(level) {

        switch (level) {

            case "CRITICAL":
                return "#ef4444";

            case "HIGH":
                return "#f59e0b";

            case "MEDIUM":
                return "#38bdf8";

            default:
                return "#22c55e";
        }
    }

    return (
        <div
            className="fade-card"
            style={{
                background:
                    "linear-gradient(135deg, rgba(37,99,235,0.14), rgba(124,58,237,0.12))",
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.card,
                padding: "28px",
                marginBottom: "32px"
            }}
        >

            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: "20px",
                flexWrap: "wrap",
                marginBottom: "26px"
            }}>

                <div>

                    <div style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "10px",
                        background: "rgba(255,255,255,0.06)",
                        padding: "8px 14px",
                        borderRadius: "999px",
                        marginBottom: "14px",
                        fontWeight: "bold"
                    }}>
                        🤖 IA COPILOT ACTIVE
                    </div>

                    <h2 style={{
                        margin: 0,
                        fontSize: "30px",
                        letterSpacing: "-0.04em"
                    }}>
                        AI Command Center
                    </h2>

                    <p style={{
                        marginTop: "10px",
                        color: theme.colors.textSecondary,
                        lineHeight: 1.7,
                        maxWidth: "760px"
                    }}>
                        Supervision intelligente temps réel,
                        recommandations IA,
                        détection de risques,
                        analyses automatiques
                        et assistance métier proactive.
                    </p>

                </div>

                <div style={{
                    background:
                        "linear-gradient(135deg,#2563eb,#7c3aed)",
                    padding: "18px",
                    borderRadius: "20px",
                    minWidth: "180px"
                }}>

                    <div style={{
                        color: "rgba(255,255,255,0.7)",
                        marginBottom: "8px"
                    }}>
                        Score IA Global
                    </div>

                    <div style={{
                        fontSize: "42px",
                        fontWeight: "bold"
                    }}>
                        94
                    </div>

                </div>

            </div>

            <div style={{
                display: "grid",
                gridTemplateColumns:
                    "repeat(auto-fit,minmax(280px,1fr))",
                gap: "18px"
            }}>

                {aiInsights.map((insight) => (

                    <div
                        key={insight.id}
                        className="fade-card"
                        style={{
                            background: "rgba(255,255,255,0.04)",
                            border:
                                `1px solid ${getColor(insight.level)}`,
                            borderRadius: "18px",
                            padding: "20px"
                        }}
                    >

                        <div style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            marginBottom: "14px"
                        }}>

                            <div style={{
                                fontWeight: "bold"
                            }}>
                                {insight.title}
                            </div>

                            <div style={{
                                background: getColor(insight.level),
                                color: "white",
                                padding: "6px 10px",
                                borderRadius: "999px",
                                fontSize: "12px",
                                fontWeight: "bold"
                            }}>
                                {insight.level}
                            </div>

                        </div>

                        <div style={{
                            color: theme.colors.textSecondary,
                            lineHeight: 1.7,
                            minHeight: "72px"
                        }}>
                            {insight.message}
                        </div>

                        <button style={{
                            marginTop: "18px",
                            width: "100%",
                            background:
                                "linear-gradient(135deg,#2563eb,#38bdf8)",
                            color: "white",
                            border: 0,
                            borderRadius: "12px",
                            padding: "12px",
                            cursor: "pointer",
                            fontWeight: "bold"
                        }}>
                            {insight.action}
                        </button>

                    </div>

                ))}

            </div>

        </div>
    );
}
