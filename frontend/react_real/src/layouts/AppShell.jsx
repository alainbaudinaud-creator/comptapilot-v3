import React from "react";
import { theme } from "../theme/theme";

export default function AppShell({ children }) {
    return (
        <div style={{
            minHeight: "100vh",
            background: `radial-gradient(circle at top left, #0f172a, ${theme.colors.background} 45%)`,
            color: theme.colors.text,
            display: "flex",
            fontFamily: "Inter, Arial, sans-serif"
        }}>
            {children}
        </div>
    );
}
