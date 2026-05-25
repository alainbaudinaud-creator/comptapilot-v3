import React from "react";
import { theme } from "../theme/theme";

export default function AppShell({ children }) {

    return (

        <div style={{
            minHeight: "100vh",
            background: theme.colors.background,
            color: theme.colors.text,
            display: "flex"
        }}>

            {children}

        </div>
    );
}
