import React from "react";

export default function CabinetPage() {

    const cards = [
        "Onboarding clients",
        "Production comptable",
        "Révision",
        "Clôture",
        "Liasses fiscales",
        "Plaquettes"
    ];

    return (
        <section>
            <h2>Cabinet</h2>

            <div style={gridStyle}>
                {cards.map((item) => (
                    <div key={item} style={cardStyle}>
                        <h3>{item}</h3>
                        <p>Workflow opérationnel V3</p>
                    </div>
                ))}
            </div>
        </section>
    );
}

const gridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
    gap: "18px"
};

const cardStyle = {
    background: "#0f172a",
    border: "1px solid #334155",
    borderRadius: "18px",
    padding: "20px"
};
