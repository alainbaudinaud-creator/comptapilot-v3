import React from "react";

export default function Header({ user, onLogout }) {

    return (
        <header style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "24px"
        }}>
            <div>
                <h1 style={{ margin: 0 }}>ComptaPilot V3</h1>
                <p style={{ margin: "6px 0 0", color: "#94a3b8" }}>
                    Plateforme cabinet cloud moderne
                </p>
            </div>

            <div style={{
                display: "flex",
                alignItems: "center",
                gap: "12px"
            }}>
                <span>{user?.email || "admin@comptapilot.local"}</span>

                <button onClick={onLogout} style={{
                    background: "#334155",
                    color: "white",
                    border: 0,
                    padding: "10px 12px",
                    borderRadius: "10px",
                    cursor: "pointer"
                }}>
                    Déconnexion
                </button>
            </div>
        </header>
    );
}
