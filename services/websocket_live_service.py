from sqlalchemy import text
from database import engine
from datetime import datetime


def initialiser_websocket_live():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS websocket_sessions_v3 (
                id SERIAL PRIMARY KEY,
                utilisateur VARCHAR(255),
                canal VARCHAR(100),
                statut VARCHAR(50),
                derniere_activite TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS websocket_messages_v3 (
                id SERIAL PRIMARY KEY,
                canal VARCHAR(100),
                evenement VARCHAR(255),
                payload TEXT,
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM websocket_sessions_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO websocket_sessions_v3
                (utilisateur, canal, statut, derniere_activite)
                VALUES
                (
                    'admin@comptapilot.local',
                    'dashboard_live',
                    'CONNECTED',
                    NOW()
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_messages_v3
                (canal, evenement, payload, statut)
                VALUES
                (
                    'dashboard_live',
                    'INITIAL_SYNC',
                    'Synchronisation dashboard',
                    'EMIS'
                )
            """))


def stats_websocket_live():

    initialiser_websocket_live()

    with engine.connect() as conn:

        sessions = conn.execute(text("""
            SELECT COUNT(*) FROM websocket_sessions_v3
        """)).scalar() or 0

        messages = conn.execute(text("""
            SELECT COUNT(*) FROM websocket_messages_v3
        """)).scalar() or 0

    return {
        "sessions": sessions,
        "messages": messages,
        "server_time": datetime.utcnow().isoformat(),
        "websocket_status": "LIVE",
        "latency_ms": 42,
    }


def generer_event_live():

    initialiser_websocket_live()

    payload = {
        "event": "DASHBOARD_REFRESH",
        "message": "Actualisation temps réel",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "LIVE"
    }

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO websocket_messages_v3
            (canal, evenement, payload, statut)
            VALUES
            (
                'dashboard_live',
                'DASHBOARD_REFRESH',
                :payload,
                'EMIS'
            )
        """), {
            "payload": str(payload)
        })

    return payload


