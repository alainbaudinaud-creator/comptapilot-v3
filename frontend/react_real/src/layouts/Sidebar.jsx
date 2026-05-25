import React from "react";
import { theme } from "../theme/theme";

export default function Sidebar() {

    const items = [

        "Dashboard",
        "Production",
        "IA",
        "TVA",
        "Analytics",
        "Clients",
        "Paramètres"
    ];

    return (

        <aside style={{
            width: "260px",
            background: theme.colors.backgroundSecondary,
            borderRight: `1px solid ${theme.colors.border}`,
            padding: theme.spacing.lg
        }}>

            <h2 style={{
                marginBottom: theme.spacing.xl
            }}>
                ComptaPilot V3
            </h2>

            <nav style={{
                display: "flex",
                flexDirection: "column",
                gap: theme.spacing.sm
            }}>

                {items.map(item => (

                    <button
                        key={item}
                        style={{
                            background: "transparent",
                            border: 0,
                            color: theme.colors.text,
                            textAlign: "left",
                            padding: theme.spacing.md,
                            borderRadius: theme.radius.button,
                            cursor: "pointer"
                        }}
                    >
                        {item}
                    </button>

                ))}

            </nav>

        </aside>
    );
}
