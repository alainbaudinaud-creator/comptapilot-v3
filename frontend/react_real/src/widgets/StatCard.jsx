import React from "react";

export default function StatCard({ title, value }) {

    return (

        <div style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px"
        }}>

            <div style={{
                color: "#94a3b8",
                marginBottom: "10px"
            }}>
                {title}
            </div>

            <div style={{
                fontSize: "32px",
                fontWeight: "bold",
                color: "#22c55e"
            }}>
                {value}
            </div>

        </div>
    );
}
