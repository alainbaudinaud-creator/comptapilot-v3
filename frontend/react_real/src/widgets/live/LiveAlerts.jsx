import React from "react";
import { theme } from "../../theme/theme";

export default function LiveAlerts({ data }) {

    const alerts = [];

    if (data?.goLive?.data?.score_readiness === 100) {
        alerts.push({
            color: "#22c55e",
            text: "Readiness Go-Live validée à 100 %"
        });
    }

    if (data?.orchestration?.data?.redis === "READY") {
        alerts.push({
            color: "#3b82f6",
            text: "Redis / Celery prêts pour l’orchestration"
        });
    }

    if (data?.reglementaire?.data?.statut === "REGLEMENTAIRE_READY") {
        alerts.push({
            color: "#f59e0b",
            text: "DSP2 / PEPPOL / TVA avancée prêts"
        });
    }

    return (
        <div style={{
            background: theme.colors.backgroundSecondary,
            border: `1px solid ${theme.colors.border}`,
            borderRadius: theme.radius.card,
            padding: theme.spacing.lg
        }}>
            <h2>Alertes cockpit</h2>

            {alerts.map((alert, index) => (
                <div key={index} style={{
                    background: "#020617",
                    borderLeft: `4px solid ${alert.color}`,
                    padding: "14px",
                    borderRadius: "10px",
                    marginBottom: "12px"
                }}>
                    {alert.text}
                </div>
            ))}
        </div>
    );
}
