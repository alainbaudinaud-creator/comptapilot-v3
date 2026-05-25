import React from "react";
import { theme } from "../theme/theme";

export default function Header() {
    return (
        <header style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: theme.spacing.xl
        }}>
            <div>
                <h1 style={{
                    margin: 0,
                    fontSize: "34px",
                    letterSpacing: "-0.04em"
                }}>
                    Cockpit SaaS
                </h1>

                <p style={{
                    margin: "8px 0 0",
                    color: theme.colors.textSecondary
                }}>
                    Supervision temps réel de la plateforme ComptaPilot V3
                </p>
            </div>

            <div style={{
                display: "flex",
                alignItems: "center",
                gap: theme.spacing.md
            }}>
                <div style={{
                    padding: "10px 14px",
                    borderRadius: theme.radius.full,
                    background: "rgba(22,163,74,0.15)",
                    color: "#86efac",
                    border: "1px solid rgba(34,197,94,0.35)",
                    fontWeight: "bold"
                }}>
                    ● Production ready
                </div>

                <button style={{
                    background: "linear-gradient(135deg,#2563eb,#38bdf8)",
                    color: "white",
                    border: 0,
                    borderRadius: theme.radius.button,
                    padding: "12px 16px",
                    cursor: "pointer",
                    fontWeight: "bold"
                }}>
                    Nouvelle analyse
                </button>
            </div>
        </header>
    );
}
