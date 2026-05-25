import React from "react";

import { theme } from "../theme/theme";

import { useCockpit } from "./CockpitContext";

export default function QuickNavigation() {

    const { widgets, toggleFavorite } = useCockpit();

    return (
        <div
            className="fade-card"
            style={{
                background:
                    "linear-gradient(180deg,rgba(15,23,42,0.98),rgba(17,24,39,0.96))",
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.card,
                padding: "24px",
                marginBottom: "28px"
            }}
        >

            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "20px",
                gap: "20px",
                flexWrap: "wrap"
            }}>

                <div>

                    <h2 style={{
                        margin: 0,
                        fontSize: "24px"
                    }}>
                        Navigation intelligente
                    </h2>

                    <p style={{
                        marginTop: "8px",
                        color: theme.colors.textSecondary
                    }}>
                        Personnalisez votre cockpit SaaS.
                    </p>

                </div>

                <input
                    placeholder="Recherche rapide..."
                    style={{
                        background: "#0f172a",
                        border: `1px solid ${theme.colors.border}`,
                        color: "white",
                        borderRadius: "14px",
                        padding: "12px 16px",
                        minWidth: "240px",
                        outline: "none"
                    }}
                />

            </div>

            <div style={{
                display: "grid",
                gridTemplateColumns:
                    "repeat(auto-fit,minmax(220px,1fr))",
                gap: "18px"
            }}>

                {widgets.map((widget) => (

                    <div
                        key={widget.id}
                        className="fade-card"
                        style={{
                            background: "rgba(255,255,255,0.03)",
                            border: `1px solid ${theme.colors.border}`,
                            borderRadius: "18px",
                            padding: "18px"
                        }}
                    >

                        <div style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            marginBottom: "14px"
                        }}>

                            <div style={{
                                fontWeight: "bold",
                                fontSize: "18px"
                            }}>
                                {widget.title}
                            </div>

                            <button
                                onClick={() =>
                                    toggleFavorite(widget.id)
                                }
                                style={{
                                    background: "transparent",
                                    border: 0,
                                    cursor: "pointer",
                                    fontSize: "18px"
                                }}
                            >
                                {widget.favorite ? "⭐" : "☆"}
                            </button>

                        </div>

                        <div style={{
                            color: theme.colors.textSecondary,
                            lineHeight: 1.6,
                            marginBottom: "18px"
                        }}>
                            {widget.description}
                        </div>

                        <button style={{
                            width: "100%",
                            background:
                                "linear-gradient(135deg,#2563eb,#38bdf8)",
                            border: 0,
                            color: "white",
                            padding: "12px",
                            borderRadius: "12px",
                            cursor: "pointer",
                            fontWeight: "bold"
                        }}>
                            Ouvrir le module
                        </button>

                    </div>

                ))}

            </div>

        </div>
    );
}
