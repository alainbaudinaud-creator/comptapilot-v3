from sqlalchemy import text
from database import engine


def initialiser_cloud_industriel():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS celery_jobs_v3 (
            id SERIAL PRIMARY KEY,
            type_job VARCHAR(100),
            payload TEXT,
            statut VARCHAR(50),
            priorite INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS redis_cache_v3 (
            id SERIAL PRIMARY KEY,
            cache_key VARCHAR(255),
            cache_value TEXT,
            expiration TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS frontend_sessions_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            frontend VARCHAR(100),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS websocket_realtime_v3 (
            id SERIAL PRIMARY KEY,
            canal VARCHAR(100),
            evenement VARCHAR(255),
            payload TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS cloud_scaling_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(100),
            nb_instances INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS portail_mobile_v3 (
            id SERIAL PRIMARY KEY,
            plateforme VARCHAR(50),
            version VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS facturation_saas_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            abonnement VARCHAR(100),
            montant NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS supervision_cloud_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(100),
            cpu NUMERIC(8,2),
            memoire NUMERIC(8,2),
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
            FROM supervision_cloud_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO supervision_cloud_v3
                (service, cpu, memoire, statut)
                VALUES
                ('API_V3', 18.5, 42.0, 'OK')
            """))

            conn.execute(text("""
                INSERT INTO supervision_cloud_v3
                (service, cpu, memoire, statut)
                VALUES
                ('POSTGRESQL', 11.0, 38.0, 'OK')
            """))

            conn.execute(text("""
                INSERT INTO supervision_cloud_v3
                (service, cpu, memoire, statut)
                VALUES
                ('WEBSOCKET', 9.0, 22.0, 'OK')
            """))

            conn.execute(text("""
                INSERT INTO cloud_scaling_v3
                (service, nb_instances, statut)
                VALUES
                ('COMPTAPILOT_API', 3, 'SCALING_OK')
            """))

            conn.execute(text("""
                INSERT INTO portail_mobile_v3
                (plateforme, version, statut)
                VALUES
                ('ANDROID', '3.0', 'ACTIVE')
            """))

            conn.execute(text("""
                INSERT INTO portail_mobile_v3
                (plateforme, version, statut)
                VALUES
                ('IOS', '3.0', 'ACTIVE')
            """))

            conn.execute(text("""
                INSERT INTO celery_jobs_v3
                (type_job, payload, statut, priorite)
                VALUES
                (
                    'OCR_MASSIF',
                    'Traitement OCR batch',
                    'EN_ATTENTE',
                    1
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_realtime_v3
                (canal, evenement, payload, statut)
                VALUES
                (
                    'dashboard',
                    'NOUVELLE_ECRITURE',
                    'Écriture générée automatiquement',
                    'EMIS'
                )
            """))


def dashboard_cloud_industriel():

    stats = {}

    queries = {
        "celery_jobs": "SELECT COUNT(*) FROM celery_jobs_v3",
        "redis_cache": "SELECT COUNT(*) FROM redis_cache_v3",
        "frontend_sessions": "SELECT COUNT(*) FROM frontend_sessions_v3",
        "websocket_realtime": "SELECT COUNT(*) FROM websocket_realtime_v3",
        "cloud_scaling": "SELECT COUNT(*) FROM cloud_scaling_v3",
        "portail_mobile": "SELECT COUNT(*) FROM portail_mobile_v3",
        "facturation_saas": "SELECT COUNT(*) FROM facturation_saas_v3",
        "supervision_cloud": "SELECT COUNT(*) FROM supervision_cloud_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats

