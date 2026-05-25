import React from "react";
import DashboardCard from "../components/DashboardCard";
import { theme } from "../theme/theme";

export default function DashboardPage() {

    const cards = [

        {
            title: "Clients actifs",
            value: 126,
            color: "#22c55e"
        },

        {
            title: "Documents OCR",
            value: 2485,
            color: "#3b82f6"
        },

        {
            title: "Analyses IA",
            value: 1932,
            color: "#8b5cf6"
        },

        {
            title: "TVA contrôlées",
            value: 71,
            color: "#f59e0b"
        },

        {
            title: "Exports FEC",
            value: 19,
            color: "#06b6d4"
        },

        {
            title: "Workers actifs",
            value: 4,
            color: "#ef4444"
        }
    ];

    return (

        <div>

            <header style={{
                marginBottom: theme.spacing.xl
            }}>

                <h1 style={{
                    fontSize: "38px",
                    marginBottom: theme.spacing.sm
                }}>
                    Cockpit ComptaPilot V3
                </h1>

                <p style={{
                    color: theme.colors.textSecondary,
                    fontSize: "16px"
                }}>
                    Plateforme ERP IA SaaS — supervision globale
                </p>

            </header>

            <section style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
                gap: theme.spacing.lg
            }}>

                {cards.map(card => (

                    <DashboardCard
                        key={card.title}
                        title={card.title}
                        value={card.value}
                        color={card.color}
                    />

                ))}

            </section>

            <section style={{
                marginTop: theme.spacing.xl,
                display: "grid",
                gridTemplateColumns: "2fr 1fr",
                gap: theme.spacing.lg
            }}>

                <div style={{
                    background: theme.colors.backgroundSecondary,
                    border: `1px solid ${theme.colors.border}`,
                    borderRadius: theme.radius.card,
                    padding: theme.spacing.lg
                }}>

                    <h2 style={{
                        marginBottom: theme.spacing.lg
                    }}>
                        Activité plateforme
                    </h2>

                    <Activity
                        label="OCR facture fournisseur"
                        status="SUCCESS"
                    />

                    <Activity
                        label="Analyse OpenAI comptable"
                        status="SUCCESS"
                    />

                    <Activity
                        label="Export FEC"
                        status="SUCCESS"
                    />

                    <Activity
                        label="Synchronisation DSP2"
                        status="RUNNING"
                    />

                    <Activity
                        label="Contrôle TVA"
                        status="SUCCESS"
                    />

                </div>

                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: theme.spacing.lg
                }}>

                    <Panel
                        title="Infrastructure"
                        value="Kubernetes READY"
                        color="#22c55e"
                    />

                    <Panel
                        title="Sécurité"
                        value="MFA ACTIVE"
                        color="#3b82f6"
                    />

                    <Panel
                        title="Monitoring"
                        value="Grafana ONLINE"
                        color="#8b5cf6"
                    />

                    <Panel
                        title="Production"
                        value="PUBLIC READY"
                        color="#f59e0b"
                    />

                </div>

            </section>

            <section style={{
                marginTop: theme.spacing.xl,
                background: theme.colors.backgroundSecondary,
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.card,
                padding: theme.spacing.lg
            }}>

                <h2 style={{
                    marginBottom: theme.spacing.lg
                }}>
                    Alertes prioritaires
                </h2>

                <Alert
                    color="#f59e0b"
                    text="3 contrôles TVA à valider"
                />

                <Alert
                    color="#3b82f6"
                    text="Nouvelle synchronisation bancaire disponible"
                />

                <Alert
                    color="#22c55e"
                    text="Tous les workers Celery sont opérationnels"
                />

            </section>

        </div>
    );
}

function Activity({ label, status }) {

    return (

        <div style={{
            display: "flex",
            justifyContent: "space-between",
            padding: "14px 0",
            borderBottom: "1px solid #1e293b"
        }}>

            <span>{label}</span>

            <strong style={{
                color:
                    status === "SUCCESS"
                        ? "#22c55e"
                        : "#f59e0b"
            }}>
                {status}
            </strong>

        </div>
    );
}

function Panel({ title, value, color }) {

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
                fontSize: "20px",
                fontWeight: "bold",
                color
            }}>
                {value}
            </div>

        </div>
    );
}

function Alert({ text, color }) {

    return (

        <div style={{
            background: "#020617",
            borderLeft: `4px solid ${color}`,
            padding: "14px",
            borderRadius: "10px",
            marginBottom: "12px"
        }}>
            {text}
        </div>
    );
}
