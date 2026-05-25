import React, { useEffect, useState } from "react";
import { getJson } from "../api/apiClient";

export default function NotificationsPanel() {

    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        async function load() {
            try {
                const data = await getJson("/live/notifications");

                if (data.success) {
                    setNotifications(data.notifications);
                }
            } catch (e) {
                setNotifications([]);
            }
        }

        load();

        const timer = setInterval(load, 10000);

        return () => clearInterval(timer);
    }, []);

    return (
        <section style={{
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "20px",
            marginTop: "24px"
        }}>
            <h2>Notifications live</h2>

            {notifications.length === 0 && (
                <p style={{ color: "#94a3b8" }}>Aucune notification active.</p>
            )}

            {notifications.map((n) => (
                <div key={n.id} style={{
                    padding: "12px",
                    borderRadius: "12px",
                    background: "#111827",
                    marginBottom: "10px"
                }}>
                    <strong>{n.type_notification}</strong>
                    <p style={{ margin: "6px 0" }}>{n.message}</p>
                    <small>{n.niveau} · {n.statut}</small>
                </div>
            ))}
        </section>
    );
}
