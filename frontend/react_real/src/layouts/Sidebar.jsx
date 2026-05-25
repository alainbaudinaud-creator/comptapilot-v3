import React from "react";
import { theme } from "../theme/theme";

export default function Sidebar() {
    const groups = [
        {
            title: "Pilotage",
            items: ["Cockpit", "Production", "Analytics", "Monitoring"]
        },
        {
            title: "Métier",
            items: ["OCR IA", "TVA", "FEC", "Clients"]
        },
        {
            title: "Plateforme",
            items: ["Sécurité", "Intégrations", "Cloud", "Paramètres"]
        }
    ];

    return (
        <aside style={{
            width: "280px",
            minHeight: "100vh",
            background: "rgba(15,23,42,0.92)",
            backdropFilter: "blur(18px)",
            borderRight: `1px solid ${theme.colors.border}`,
            padding: theme.spacing.lg,
            position: "sticky",
            top: 0
        }}>
            <div style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                marginBottom: theme.spacing.xl
            }}>
                <div style={{
                    width: "42px",
                    height: "42px",
                    borderRadius: theme.radius.md,
                    background: "linear-gradient(135deg,#2563eb,#38bdf8)",
                    display: "grid",
                    placeItems: "center",
                    fontWeight: "bold"
                }}>
                    CP
                </div>

                <div>
                    <strong>ComptaPilot V3</strong>
                    <div style={{
                        color: theme.colors.textSecondary,
                        fontSize: "12px"
                    }}>
                        ERP IA SaaS
                    </div>
                </div>
            </div>

            {groups.map((group) => (
                <div key={group.title} style={{ marginBottom: theme.spacing.lg }}>
                    <div style={{
                        color: theme.colors.textSecondary,
                        fontSize: "12px",
                        textTransform: "uppercase",
                        letterSpacing: "0.08em",
                        marginBottom: theme.spacing.sm
                    }}>
                        {group.title}
                    </div>

                    {group.items.map((item, index) => (
                        <button
                            key={item}
                            style={{
                                width: "100%",
                                display: "flex",
                                alignItems: "center",
                                gap: "10px",
                                padding: "12px 14px",
                                marginBottom: "6px",
                                borderRadius: theme.radius.button,
                                border: index === 0 && group.title === "Pilotage"
                                    ? `1px solid ${theme.colors.primaryLight}`
                                    : "1px solid transparent",
                                background: index === 0 && group.title === "Pilotage"
                                    ? "linear-gradient(135deg,rgba(37,99,235,0.45),rgba(56,189,248,0.18))"
                                    : "transparent",
                                color: theme.colors.text,
                                textAlign: "left",
                                cursor: "pointer"
                            }}
                        >
                            <span style={{
                                width: "8px",
                                height: "8px",
                                borderRadius: theme.radius.full,
                                background: index === 0 && group.title === "Pilotage"
                                    ? theme.colors.primaryLight
                                    : theme.colors.border
                            }} />
                            {item}
                        </button>
                    ))}
                </div>
            ))}
        </aside>
    );
}
