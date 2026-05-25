import React from "react";
import { theme } from "../../theme/theme";

export default function LiveActivityFeed({ data }) {

    const items = [
        {
            label: "Dashboard financier",
            ok: data?.financier?.success
        },
        {
            label: "Production premium",
            ok: data?.production?.success
        },
        {
            label: "Orchestration workers",
            ok: data?.orchestration?.success
        },
        {
            label: "Sécurité probatoire",
            ok: data?.securite?.success
        },
        {
            label: "Réglementaire",
            ok: data?.reglementaire?.success
        },
        {
            label: "Go Live",
            ok: data?.goLive?.success
        }
    ];

    return (
        <div style={{
            background: theme.colors.backgroundSecondary,
            border: `1px solid ${theme.colors.border}`,
            borderRadius: theme.radius.card,
            padding: theme.spacing.lg
        }}>
            <h2>Activité live</h2>

            {items.map((item) => (
                <div key={item.label} style={{
                    display: "flex",
                    justifyContent: "space-between",
                    padding: "14px 0",
                    borderBottom: "1px solid #1e293b"
                }}>
                    <span>{item.label}</span>

                    <strong style={{
                        color: item.ok ? "#22c55e" : "#ef4444"
                    }}>
                        {item.ok ? "ONLINE" : "OFFLINE"}
                    </strong>
                </div>
            ))}
        </div>
    );
}
