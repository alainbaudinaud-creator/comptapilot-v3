import React from "react";

export default function Sidebar() {

    const menus = [
        "Dashboard",
        "Clients",
        "Production",
        "OCR IA",
        "TVA",
        "Liasse",
        "PDP",
        "GED",
        "API",
        "Cloud"
    ];

    return (

        <aside style={{
            width: "240px",
            background: "#0f172a",
            minHeight: "100vh",
            padding: "20px",
            borderRight: "1px solid #334155"
        }}>

            <h2 style={{
                color: "#38bdf8"
            }}>
                ComptaPilot V3
            </h2>

            <div style={{
                marginTop: "30px"
            }}>

                {menus.map((menu) => (

                    <div
                        key={menu}
                        style={{
                            padding: "12px",
                            marginBottom: "8px",
                            background: "#111827",
                            borderRadius: "10px",
                            cursor: "pointer"
                        }}
                    >
                        {menu}
                    </div>

                ))}

            </div>

        </aside>
    );
}
