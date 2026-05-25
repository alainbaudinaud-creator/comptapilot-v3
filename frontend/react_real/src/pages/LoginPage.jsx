import React, { useState } from "react";
import { loginDemo } from "../auth/authService";

export default function LoginPage({ onLogin }) {

    const [email, setEmail] = useState("admin@comptapilot.local");
    const [password, setPassword] = useState("demo");

    function handleSubmit(event) {
        event.preventDefault();

        const result = loginDemo(email, password);

        if (result.success) {
            onLogin(result.user);
        }
    }

    return (
        <div style={{
            minHeight: "100vh",
            display: "grid",
            placeItems: "center",
            background: "#020617",
            color: "#e5e7eb"
        }}>
            <form onSubmit={handleSubmit} style={{
                width: "420px",
                background: "#0f172a",
                padding: "32px",
                borderRadius: "24px",
                border: "1px solid #334155"
            }}>
                <h1>ComptaPilot V3</h1>
                <p>Connexion SaaS cabinet</p>

                <input
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={inputStyle}
                    placeholder="Email"
                />

                <input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type="password"
                    style={inputStyle}
                    placeholder="Mot de passe"
                />

                <button style={buttonStyle}>
                    Connexion
                </button>
            </form>
        </div>
    );
}

const inputStyle = {
    width: "100%",
    padding: "14px",
    marginTop: "14px",
    borderRadius: "12px",
    border: "1px solid #334155",
    background: "#020617",
    color: "white"
};

const buttonStyle = {
    width: "100%",
    padding: "14px",
    marginTop: "20px",
    borderRadius: "12px",
    border: "0",
    background: "#2563eb",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer"
};
