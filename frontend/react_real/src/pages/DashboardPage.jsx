import React, { useEffect, useState } from "react";
import StatCard from "../widgets/StatCard";
import NotificationsPanel from "../widgets/NotificationsPanel";
import LiveDashboardPanel from "../widgets/LiveDashboardPanel";
import InfrastructurePanel from "../widgets/InfrastructurePanel";
import FinancialDashboard from "../finance/FinancialDashboard";
import SocketLivePanel from "../widgets/SocketLivePanel";
import ProductionPremiumPanel from "../premium/ProductionPremiumPanel";
import IntegrationsProductionPanel from "../production/IntegrationsProductionPanel";
import OpenAIRealPanel from "../ai/OpenAIRealPanel";
import TesseractRealPanel from "../ocr/TesseractRealPanel";
import { chargerDashboard } from "../api/dashboardApi";

export default function DashboardPage() {

    const [data, setData] = useState({});

    useEffect(() => {

        async function load() {

            const result = await chargerDashboard();

            setData(result);
        }

        load();

        const timer = setInterval(load, 10000);

        return () => clearInterval(timer);

    }, []);

    return (

        <section>

            <h2>Dashboard Temps Réel</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
                gap: "20px",
                marginTop: "20px"
            }}>

                {Object.entries(data).map(([endpoint, payload]) => (

                    <StatCard
                        key={endpoint}
                        title={endpoint}
                        value={payload.success ? "ONLINE" : "ERROR"}
                    />

                ))}

            </div>

            <FinancialDashboard />

            <InfrastructurePanel />

            <ProductionPremiumPanel />

            <IntegrationsProductionPanel />

            <OpenAIRealPanel />

            <TesseractRealPanel />

            <SocketLivePanel />

            <LiveDashboardPanel />

            <NotificationsPanel />

        </section>
    );
}
