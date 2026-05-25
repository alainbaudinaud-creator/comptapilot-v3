import React from "react";
import { theme } from "../theme/theme";
import useCockpitLive from "../hooks/useCockpitLive";
import LiveModuleCard from "../widgets/live/LiveModuleCard";
import LiveActivityFeed from "../widgets/live/LiveActivityFeed";
import LiveAlerts from "../widgets/live/LiveAlerts";

export default function DashboardPage() {

    const {
        data,
        loading,
        error,
        refresh
    } = useCockpitLive(10000);

    const financier = data?.financier?.data?.finance;
    const production = data?.production?.stats;
    const orchestration = data?.orchestration?.data;
    const securite = data?.securite?.data;
    const reglementaire = data?.reglementaire?.data;
    const commercial = data?.commercial?.data;
    const goLive = data?.goLive?.data;

    return (
        <div>
            <header style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                marginBottom: theme.spacing.xl
            }}>
                <div>
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
                        Supervision SaaS live — données connectées aux APIs V3
                    </p>
                </div>

                <button
                    onClick={refresh}
                    style={{
                        background: theme.colors.primary,
                        color: "white",
                        border: 0,
                        borderRadius: theme.radius.button,
                        padding: "12px 16px",
                        cursor: "pointer",
                        fontWeight: "bold"
                    }}
                >
                    Rafraîchir
                </button>
            </header>

            {loading && (
                <p style={{ color: theme.colors.textSecondary }}>
                    Chargement du cockpit live...
                </p>
            )}

            {error && (
                <p style={{ color: theme.colors.danger }}>
                    {error}
                </p>
            )}

            <section style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
                gap: theme.spacing.lg
            }}>
                <LiveModuleCard
                    title="CA"
                    payload={data.financier}
                    metric={financier?.chiffre_affaires ? `${financier.chiffre_affaires} €` : "—"}
                />

                <LiveModuleCard
                    title="Trésorerie"
                    payload={data.financier}
                    metric={financier?.tresorerie ? `${financier.tresorerie} €` : "—"}
                />

                <LiveModuleCard
                    title="Production premium"
                    payload={data.production}
                    metric={production?.traitements_total ?? "—"}
                />

                <LiveModuleCard
                    title="Workers"
                    payload={data.orchestration}
                    metric={orchestration?.workers ?? "—"}
                />

                <LiveModuleCard
                    title="Audits légaux"
                    payload={data.securite}
                    metric={securite?.audits ?? "—"}
                />

                <LiveModuleCard
                    title="Readiness"
                    payload={data.goLive}
                    metric={goLive?.score_readiness ? `${goLive.score_readiness} %` : "—"}
                />
            </section>

            <section style={{
                marginTop: theme.spacing.xl,
                display: "grid",
                gridTemplateColumns: "2fr 1fr",
                gap: theme.spacing.lg
            }}>
                <LiveActivityFeed data={data} />

                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: theme.spacing.lg
                }}>
                    <LiveModuleCard
                        title="Réglementaire"
                        payload={data.reglementaire}
                        metric={reglementaire?.statut ?? "—"}
                    />

                    <LiveModuleCard
                        title="Commercial SaaS"
                        payload={data.commercial}
                        metric={commercial?.cloud_public ?? "—"}
                    />

                    <LiveModuleCard
                        title="Enterprise"
                        payload={data.enterprise}
                        metric={data?.enterprise?.data?.cloud_status ?? "—"}
                    />
                </div>
            </section>

            <section style={{
                marginTop: theme.spacing.xl
            }}>
                <LiveAlerts data={data} />
            </section>
        </div>
    );
}
