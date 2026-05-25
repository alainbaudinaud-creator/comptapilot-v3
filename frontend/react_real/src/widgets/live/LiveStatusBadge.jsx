import React from "react";
import { theme } from "../../theme/theme";

export default function LiveStatusBadge({ success }) {

    return (
        <span style={{
            display: "inline-block",
            padding: "6px 10px",
            borderRadius: "999px",
            fontSize: "12px",
            fontWeight: "bold",
            color: "white",
            background: success ? theme.colors.success : theme.colors.danger
        }}>
            {success ? "LIVE" : "ERROR"}
        </span>
    );
}
