import React from "react";
import { theme } from "../../theme/theme";
import LiveStatusBadge from "./LiveStatusBadge";

export default function LiveModuleCard({ title, payload, metric }) {

    const success = Boolean(payload?.success);

    return (
        <div style={{
            background: theme.colors.backgroundSecondary,
            border: `1px solid ${theme.colors.border}`,
            borderRadius: theme.radius.card,
            padding: theme.spacing.lg
        }}>
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: theme.spacing.md
            }}>
                <div style={{ color: theme.colors.textSecondary }}>
                    {title}
                </div>

                <LiveStatusBadge success={success} />
            </div>

            <div style={{
                fontSize: "26px",
                fontWeight: "bold",
                color: success ? "#22c55e" : "#ef4444"
            }}>
                {metric ?? (success ? "OK" : "Erreur")}
            </div>

            {!success && (
                <p style={{
                    color: "#fca5a5",
                    marginTop: theme.spacing.sm
                }}>
                    {payload?.error || "Module indisponible"}
                </p>
            )}
        </div>
    );
}
