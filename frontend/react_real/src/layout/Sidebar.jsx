import React from "react";

export default function Sidebar({ onNavigate }) {

    const menus = [
        { key: "dashboard", label: "Dashboard" },
        { key: "cabinet", label: "Cabinet" },
        { key: "production", label: "Production IA" },
        { key: "client", label: "Portail Client" }
    ];

    return (
        <aside style={{
            width: "250px",
            background: "#0f172a",
            minHeight: "100vh",
            padding: "20px",
            borderRight: "1px solid #334155"
        }}>
            <h2 style={{ color: "#38bdf8" }}>
                ComptaPilot V3
            </h2>

            <div style={{ marginTop: "30px" }}>
                {menus.map((menu) => (
                    <button
                        key={menu.key}
                        onClick={() => onNavigate(menu.key)}
                        style={{
                            display: "block",
                            width: "100%",
                            textAlign: "left",
                            padding: "12px",
                            marginBottom: "8px",
                            background: "#111827",
                            color: "white",
                            border: "1px solid #334155",
                            borderRadius: "10px",
                            cursor: "pointer"
                        }}
                    >
                        {menu.label}
                    </button>
                ))}
            </div>
        </aside>
    );
}
