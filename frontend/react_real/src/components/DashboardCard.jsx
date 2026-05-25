import React from "react";
import { theme } from "../theme/theme";

export default function DashboardCard({
    title,
    value,
    color = "#38bdf8",
    subtitle = ""
}) {
    return (
        <div
            className="fade-card"
            style={{
                background: "linear-gradient(180deg,rgba(15,23,42,0.98),rgba(17,24,39,0.96))",
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.card,
                padding: theme.spacing.lg,
                boxShadow: theme.shadow.card
            }}
        >
            <div style={{
                color: theme.colors.textSecondary,
                marginBottom: theme.spacing.sm
            }}>
                {title}
            </div>

            <div style={{
                fontSize: "30px",
                fontWeight: "bold",
                color
            }}>
                {value}
            </div>

            {subtitle && (
                <div style={{
                    marginTop: theme.spacing.sm,
                    color: theme.colors.textSecondary,
                    fontSize: "13px"
                }}>
                    {subtitle}
                </div>
            )}
        </div>
    );
}
