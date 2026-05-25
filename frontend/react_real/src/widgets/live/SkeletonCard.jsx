import React from "react";
import { theme } from "../../theme/theme";

export default function SkeletonCard() {
    return (
        <div
            className="fade-card"
            style={{
                background: "linear-gradient(180deg,rgba(15,23,42,0.98),rgba(17,24,39,0.96))",
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.card,
                padding: theme.spacing.lg,
                minHeight: "130px"
            }}
        >
            <div
                className="skeleton"
                style={{
                    width: "40%",
                    height: "16px",
                    borderRadius: "8px",
                    marginBottom: "24px"
                }}
            />

            <div
                className="skeleton"
                style={{
                    width: "70%",
                    height: "42px",
                    borderRadius: "12px"
                }}
            />
        </div>
    );
}
