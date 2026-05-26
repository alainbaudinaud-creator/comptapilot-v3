from sqlalchemy import text
from database import engine


def initialiser_saas_realtime():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS websocket_sessions_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            canal VARCHAR(100),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS jwt_sessions_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            token TEXT,
            expiration TIMESTAMP,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS portail_clients_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            email VARCHAR(255),
            acces_mobile BOOLEAN DEFAULT TRUE,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS applications_mobiles_v3 (
            id SERIAL PRIMARY KEY,
            plateforme VARCHAR(50),
            version VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS websocket_events_v3 (
            id SERIAL PRIMARY KEY,
            type_event VARCHAR(100),
            payload TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS multi_tenant_v3 (
            id SERIAL PRIMARY KEY,
            tenant_code VARCHAR(100),
            tenant_nom VARCHAR(255),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    with engine.begin() as conn:

        for statement in statements:
            conn.execute(text(statement))

        existing = conn.execute(text("""
            SELECT COUNT(*)
            FROM multi_tenant_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO multi_tenant_v3
                (tenant_code, tenant_nom, statut)
                VALUES
                (
                    'CABINET_DEMO',
                    'Cabinet ComptaPilot Demo',
                    'ACTIF'
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_sessions_v3
                (utilisateur, canal, statut)
                VALUES
                (
                    'admin@comptapilot.local',
                    'dashboard_temps_reel',
                    'CONNECTE'
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_events_v3
                (type_event, payload, statut)
                VALUES
                (
                    'NOUVELLE_ECRITURE',
                    'Ecriture comptable générée automatiquement',
                    'EMIS'
                )
            """))

            conn.execute(text("""
                INSERT INTO applications_mobiles_v3
                (plateforme, version, statut)
                VALUES
                (
                    'ANDROID',
                    'V3.0',
                    'ACTIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO applications_mobiles_v3
                (plateforme, version, statut)
                VALUES
                (
                    'IOS',
                    'V3.0',
                    'ACTIVE'
                )
            """))


def dashboard_saas_realtime():

    stats = {}

    queries = {
        "websocket_sessions": "SELECT COUNT(*) FROM websocket_sessions_v3",
        "jwt_sessions": "SELECT COUNT(*) FROM jwt_sessions_v3",
        "portail_clients": "SELECT COUNT(*) FROM portail_clients_v3",
        "applications_mobiles": "SELECT COUNT(*) FROM applications_mobiles_v3",
        "websocket_events": "SELECT COUNT(*) FROM websocket_events_v3",
        "multi_tenant": "SELECT COUNT(*) FROM multi_tenant_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats


