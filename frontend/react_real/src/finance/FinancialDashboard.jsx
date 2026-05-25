import React, { useEffect, useState } from "react";
import {
    ResponsiveContainer,
    LineChart,
    Line,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip
} from "recharts";

import { getJson } from "../api/apiClient";

export default function FinancialDashboard() {

    const [data, setData] = useState(null);

    useEffect(() => {

        async function load() {

            try {

                const response = await getJson("/dashboard-financier");

                if (response.success) {
                    setData(response.data);
                }

            } catch (e) {
                console.error(e);
            }
        }

        load();

        const timer = setInterval(load, 8000);

        return () => clearInterval(timer);

    }, []);

    if (!data) {
        return null;
    }

    const finance = data.finance;
    const production = data.production;

    return (

        <section style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px",
            marginTop: "24px"
        }}>

            <h2>Dashboard Financier Premium</h2>

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
                gap: "16px",
                marginTop: "20px"
            }}>

                <Card
                    title="CA"
                    value={`${finance.chiffre_affaires} €`}
                />

                <Card
                    title="Trésorerie"
                    value={`${finance.tresorerie} €`}
                />

                <Card
                    title="TVA"
                    value={`${finance.tva_due} €`}
                />

                <Card
                    title="Résultat"
                    value={`${finance.resultat} €`}
                />

            </div>

            <div style={{
                height: "340px",
                marginTop: "30px"
            }}>

                <ResponsiveContainer width="100%" height="100%">

                    <LineChart data={data.charts}>

                        <CartesianGrid stroke="#334155" />

                        <XAxis dataKey="mois" />

                        <YAxis />

                        <Tooltip />

                        <Line
                            type="monotone"
                            dataKey="ca"
                            stroke="#38bdf8"
                            strokeWidth={3}
                        />

                        <Line
                            type="monotone"
                            dataKey="tresorerie"
                            stroke="#22c55e"
                            strokeWidth={3}
                        />

                        <Line
                            type="monotone"
                            dataKey="resultat"
                            stroke="#f59e0b"
                            strokeWidth={3}
                        />

                    </LineChart>

                </ResponsiveContainer>

            </div>

            <div style={{
                marginTop: "30px",
                background: "#111827",
                borderRadius: "14px",
                padding: "18px"
            }}>

                <h3>Production Cabinet Live</h3>

                <p>Dossiers : {production.dossiers}</p>

                <p>Révisions : {production.revisions}</p>

                <p>Liasses : {production.liasses}</p>

                <p>TVA : {production.tva}</p>

                <p>Statut : {production.statut}</p>

            </div>

        </section>
    );
}

function Card({ title, value }) {

    return (

        <div style={{
            background: "#111827",
            borderRadius: "14px",
            padding: "18px"
        }}>

            <div style={{
                color: "#94a3b8",
                marginBottom: "10px"
            }}>
                {title}
            </div>

            <div style={{
                fontSize: "28px",
                fontWeight: "bold",
                color: "#38bdf8"
            }}>
                {value}
            </div>

        </div>
    );
}
