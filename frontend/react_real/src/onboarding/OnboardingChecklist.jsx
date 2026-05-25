import React from "react";

import { onboardingSteps } from "./onboardingSteps";
import { theme } from "../theme/theme";

export default function OnboardingChecklist() {

    return (
        <div
            className="fade-card"
            style={{
                background:
                    "linear-gradient(180deg,rgba(15,23,42,0.98),rgba(17,24,39,0.96))",
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.card,
                padding: "28px"
            }}
        >

            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "26px"
            }}>

                <div>

                    <h2 style={{
                        margin: 0,
                        fontSize: "24px"
                    }}>
                        Onboarding intelligent
                    </h2>

                    <p style={{
                        color: theme.colors.textSecondary,
                        marginTop: "10px"
                    }}>
                        Finalisez rapidement votre environnement SaaS.
                    </p>

                </div>

                <div style={{
                    background: "rgba(37,99,235,0.18)",
                    color: "#7dd3fc",
                    borderRadius: "999px",
                    padding: "10px 14px",
                    fontWeight: "bold"
                }}>
                    40% complété
                </div>

            </div>

            <div style={{
                display: "flex",
                flexDirection: "column",
                gap: "18px"
            }}>

                {onboardingSteps.map((step) => {

                    const background =
                        step.status === "done"
                            ? "rgba(22,163,74,0.12)"
                            : step.status === "current"
                                ? "rgba(37,99,235,0.16)"
                                : "rgba(255,255,255,0.03)";

                    const border =
                        step.status === "done"
                            ? "#22c55e"
                            : step.status === "current"
                                ? "#38bdf8"
                                : "#334155";

                    return (

                        <div
                            key={step.id}
                            style={{
                                display: "flex",
                                gap: "18px",
                                alignItems: "flex-start",
                                padding: "18px",
                                borderRadius: "18px",
                                border: `1px solid ${border}`,
                                background
                            }}
                        >

                            <div style={{
                                width: "34px",
                                height: "34px",
                                borderRadius: "999px",
                                display: "grid",
                                placeItems: "center",
                                fontWeight: "bold",
                                background:
                                    step.status === "done"
                                        ? "#16a34a"
                                        : step.status === "current"
                                            ? "#2563eb"
                                            : "#1e293b"
                            }}>
                                {step.status === "done"
                                    ? "✓"
                                    : step.id}
                            </div>

                            <div>

                                <div style={{
                                    fontWeight: "bold",
                                    marginBottom: "8px"
                                }}>
                                    {step.title}
                                </div>

                                <div style={{
                                    color: theme.colors.textSecondary,
                                    lineHeight: 1.6
                                }}>
                                    {step.description}
                                </div>

                            </div>

                        </div>

                    );

                })}

            </div>

        </div>
    );
}
