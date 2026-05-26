from sqlalchemy import text
from database import engine


def initialiser_temps_reel():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS notifications_react_live_v3 (
                id SERIAL PRIMARY KEY,
                utilisateur VARCHAR(255),
                type_notification VARCHAR(100),
                message TEXT,
                niveau VARCHAR(50),
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS websocket_events_live_v3 (
                id SERIAL PRIMARY KEY,
                canal VARCHAR(100),
                evenement VARCHAR(255),
                payload TEXT,
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM notifications_react_live_v3
        """)).scalar() or 0

        if existing == 0:
            conn.execute(text("""
                INSERT INTO notifications_react_live_v3
                (utilisateur, type_notification, message, niveau, statut)
                VALUES
                ('admin@comptapilot.local', 'OCR', 'Nouvelle analyse OCR IA disponible', 'INFO', 'ACTIVE')
            """))

            conn.execute(text("""
                INSERT INTO notifications_react_live_v3
                (utilisateur, type_notification, message, niveau, statut)
                VALUES
                ('admin@comptapilot.local', 'TVA', 'Contrôle TVA à valider', 'IMPORTANT', 'ACTIVE')
            """))

            conn.execute(text("""
                INSERT INTO websocket_events_live_v3
                (canal, evenement, payload, statut)
                VALUES
                ('dashboard_live', 'REFRESH_STATS', 'Actualisation dashboard V3', 'EMIS')
            """))


def liste_notifications():
    initialiser_temps_reel()

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, type_notification, message, niveau, statut, created_at
            FROM notifications_react_live_v3
            ORDER BY created_at DESC
            LIMIT 20
        """)).mappings().all()

    return [dict(row) for row in rows]


def stats_temps_reel():
    initialiser_temps_reel()

    with engine.connect() as conn:
        notifications = conn.execute(text("""
            SELECT COUNT(*) FROM notifications_react_live_v3
        """)).scalar() or 0

        events = conn.execute(text("""
            SELECT COUNT(*) FROM websocket_events_live_v3
        """)).scalar() or 0

    return {
        "notifications": notifications,
        "websocket_events": events,
        "websocket_status": "READY",
        "live_mode": True,
    }


