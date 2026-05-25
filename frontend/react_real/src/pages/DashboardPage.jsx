import React, { useEffect } from "react";

import { theme } from "../theme/theme";

import useCockpitLive from "../hooks/useCockpitLive";

import LiveModuleCard from "../widgets/live/LiveModuleCard";
import LiveActivityFeed from "../widgets/live/LiveActivityFeed";
import LiveAlerts from "../widgets/live/LiveAlerts";
import SkeletonCard from "../widgets/live/SkeletonCard";

import { useToast } from "../context/ToastContext";

export default function DashboardPage() {

    const {
        data,
        loading,
        error,
        refresh
    } = useCockpitLive(10000);

    const { pushToast } = useToast();

    useEffect(() => {

        pushToast(
            "Cockpit ComptaPilot V3 connecté",
            "success"
        );

    }, []);

    useEffect(() => {

        if (error) {

            pushToast(
                "Erreur chargement APIs live",
                "error"
            );
        }

    }, [error]);

    const financier = data?.financier?.data?.finance;
    const production = data?.production?.stats;
    const orchestration = data?.orchestration?.data;
    const securite = data?.securite?.data;
    const reglementaire = data?.reglementaire?.data;
    const commercial = data?.commercial?.data;
    const goLive = data?.goLive?.data;

    return (
        <div>

            <section
                className="cockpit-grid"
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
                    gap: theme.spacing.lg
                }}
            >

                {loading ? (
                    <>
                        <SkeletonCard />
                        <SkeletonCard />
                        <SkeletonCard />
                        <SkeletonCard />
                    </>
                ) : (
                    <>
                        <LiveModuleCard
                            title="CA"
                            payload={data.financier}
                            metric={financier?.chiffre_affaires
                                ? `${financier.chiffre_affaires} €`
                                : "—"}
                        />

                        <LiveModuleCard
                            title="Trésorerie"
                            payload={data.financier}
                            metric={financier?.tresorerie
                                ? `${financier.tresorerie} €`
                                : "—"}
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
                            metric={goLive?.score_readiness
                                ? `${goLive.score_readiness} %`
                                : "—"}
                        />
                    </>
                )}

            </section>

            <section
                className="cockpit-two-columns"
                style={{
                    marginTop: theme.spacing.xl,
                    display: "grid",
                    gridTemplateColumns: "2fr 1fr",
                    gap: theme.spacing.lg
                }}
            >

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

            <div style={{
                marginTop: theme.spacing.xl
            }}>

                <button
                    onClick={() => {
                        refresh();

                        pushToast(
                            "Cockpit actualisé",
                            "info"
                        );
                    }}
                    style={{
                        background:
                            "linear-gradient(135deg,#2563eb,#38bdf8)",
                        color: "white",
                        border: 0,
                        borderRadius: "14px",
                        padding: "14px 20px",
                        cursor: "pointer",
                        fontWeight: "bold"
                    }}
                >
                    Actualiser les données live
                </button>

            </div>

        </div>
    );
}
