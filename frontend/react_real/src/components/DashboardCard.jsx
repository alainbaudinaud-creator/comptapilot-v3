import React from "react";
import { theme } from "../theme/theme";

export default function DashboardCard({
    title,
    value,
    color = "#2563eb"
}) {

    return (

        <div style={{
            background: theme.colors.backgroundSecondary,
            border: `1px solid ${theme.colors.border}`,
            borderRadius: theme.radius.card,
            padding: theme.spacing.lg
        }}>

            <div style={{
                color: theme.colors.textSecondary,
                marginBottom: theme.spacing.sm
            }}>
                {title}
            </div>

            <div style={{
                fontSize: "28px",
                fontWeight: "bold",
                color
            }}>
                {value}
            </div>

        </div>
    );
}
