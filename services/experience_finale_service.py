from sqlalchemy import text
from database import engine


def initialiser_experience_finale():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS ui_ux_premium_v3 (
            id SERIAL PRIMARY KEY,
            module VARCHAR(100),
            theme VARCHAR(100),
            version VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS websocket_live_final_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            evenement VARCHAR(255),
            payload TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS onboarding_saas_v3 (
            id SERIAL PRIMARY KEY,
            cabinet_nom VARCHAR(255),
            email VARCHAR(255),
            plan_saas VARCHAR(100),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS billing_stripe_final_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            stripe_customer_id VARCHAR(255),
            stripe_subscription_id VARCHAR(255),
            montant_mensuel NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS portail_clients_final_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            acces_mobile BOOLEAN,
            acces_documents BOOLEAN,
            derniere_connexion TIMESTAMP,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS mobile_flutter_v3 (
            id SERIAL PRIMARY KEY,
            plateforme VARCHAR(50),
            version_mobile VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS production_haute_disponibilite_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(255),
            disponibilite NUMERIC(5,2),
            replication_active BOOLEAN,
            autoscaling BOOLEAN,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS supervision_live_final_v3 (
            id SERIAL PRIMARY KEY,
            environnement VARCHAR(50),
            cpu NUMERIC(8,2),
            memoire NUMERIC(8,2),
            websocket_actifs INTEGER,
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
            FROM onboarding_saas_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO ui_ux_premium_v3
                (module, theme, version, statut)
                VALUES
                (
                    'DASHBOARD_EXECUTIF',
                    'PREMIUM_DARK',
                    'V3.0',
                    'ACTIF'
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_live_final_v3
                (utilisateur, evenement, payload, statut)
                VALUES
                (
                    'admin@comptapilot.local',
                    'LIVE_DASHBOARD',
                    'Actualisation temps réel',
                    'EMIS'
                )
            """))

            conn.execute(text("""
                INSERT INTO onboarding_saas_v3
                (cabinet_nom, email, plan_saas, statut)
                VALUES
                (
                    'Cabinet Demo',
                    'contact@cabinet-demo.fr',
                    'ENTERPRISE',
                    'ACTIF'
                )
            """))

            conn.execute(text("""
                INSERT INTO billing_stripe_final_v3
                (client_id, stripe_customer_id, stripe_subscription_id, montant_mensuel, statut)
                VALUES
                (
                    1,
                    'cus_live_demo',
                    'sub_live_demo',
                    399.00,
                    'ACTIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO portail_clients_final_v3
                (client_id, acces_mobile, acces_documents, derniere_connexion, statut)
                VALUES
                (
                    1,
                    TRUE,
                    TRUE,
                    NOW(),
                    'CONNECTE'
                )
            """))

            conn.execute(text("""
                INSERT INTO mobile_flutter_v3
                (plateforme, version_mobile, statut)
                VALUES
                (
                    'ANDROID',
                    '3.0.0',
                    'PUBLIEE'
                )
            """))

            conn.execute(text("""
                INSERT INTO mobile_flutter_v3
                (plateforme, version_mobile, statut)
                VALUES
                (
                    'IOS',
                    '3.0.0',
                    'PUBLIEE'
                )
            """))

            conn.execute(text("""
                INSERT INTO production_haute_disponibilite_v3
                (service, disponibilite, replication_active, autoscaling, statut)
                VALUES
                (
                    'COMPTAPILOT_API',
                    99.99,
                    TRUE,
                    TRUE,
                    'ONLINE'
                )
            """))

            conn.execute(text("""
                INSERT INTO supervision_live_final_v3
                (environnement, cpu, memoire, websocket_actifs, statut)
                VALUES
                (
                    'PRODUCTION',
                    19.5,
                    44.0,
                    28,
                    'OK'
                )
            """))


def dashboard_experience_finale():

    stats = {}

    queries = {
        "ui_ux": "SELECT COUNT(*) FROM ui_ux_premium_v3",
        "websocket_live": "SELECT COUNT(*) FROM websocket_live_final_v3",
        "onboarding": "SELECT COUNT(*) FROM onboarding_saas_v3",
        "billing": "SELECT COUNT(*) FROM billing_stripe_final_v3",
        "portail_clients": "SELECT COUNT(*) FROM portail_clients_final_v3",
        "flutter_mobile": "SELECT COUNT(*) FROM mobile_flutter_v3",
        "haute_disponibilite": "SELECT COUNT(*) FROM production_haute_disponibilite_v3",
        "supervision_live": "SELECT COUNT(*) FROM supervision_live_final_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats

