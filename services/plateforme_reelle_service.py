from sqlalchemy import text
from database import engine


def initialiser_plateforme_reelle():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS react_live_dashboard_v3 (
            id SERIAL PRIMARY KEY,
            widget VARCHAR(100),
            statut VARCHAR(50),
            websocket_channel VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS openai_real_requests_v3 (
            id SERIAL PRIMARY KEY,
            type_analyse VARCHAR(100),
            modele VARCHAR(100),
            tokens_utilises INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS ocr_pdf_real_v3 (
            id SERIAL PRIMARY KEY,
            fichier_source VARCHAR(255),
            moteur_ocr VARCHAR(100),
            pages_detectees INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS portail_client_live_v3 (
            id SERIAL PRIMARY KEY,
            client_nom VARCHAR(255),
            nb_documents INTEGER,
            nb_notifications INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS websocket_live_real_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            evenement VARCHAR(255),
            latence_ms INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS production_deploiement_v3 (
            id SERIAL PRIMARY KEY,
            environnement VARCHAR(50),
            version_app VARCHAR(50),
            disponibilite NUMERIC(5,2),
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
            FROM react_live_dashboard_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO react_live_dashboard_v3
                (widget, statut, websocket_channel)
                VALUES
                (
                    'DASHBOARD_TEMPS_REEL',
                    'ACTIF',
                    'dashboard_live'
                )
            """))

            conn.execute(text("""
                INSERT INTO openai_real_requests_v3
                (type_analyse, modele, tokens_utilises, statut)
                VALUES
                (
                    'ANALYSE_COMPTABLE',
                    'GPT-5.5',
                    3200,
                    'SUCCESS'
                )
            """))

            conn.execute(text("""
                INSERT INTO ocr_pdf_real_v3
                (fichier_source, moteur_ocr, pages_detectees, statut)
                VALUES
                (
                    'facture_reelle.pdf',
                    'TESSERACT',
                    3,
                    'TRAITE'
                )
            """))

            conn.execute(text("""
                INSERT INTO portail_client_live_v3
                (client_nom, nb_documents, nb_notifications, statut)
                VALUES
                (
                    'Cabinet Demo',
                    18,
                    4,
                    'ONLINE'
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_live_real_v3
                (utilisateur, evenement, latence_ms, statut)
                VALUES
                (
                    'admin@comptapilot.local',
                    'UPDATE_DASHBOARD',
                    42,
                    'LIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO production_deploiement_v3
                (environnement, version_app, disponibilite, statut)
                VALUES
                (
                    'PRODUCTION',
                    'V3.0',
                    99.99,
                    'ONLINE'
                )
            """))


def dashboard_plateforme_reelle():

    stats = {}

    queries = {
        "react_dashboard": "SELECT COUNT(*) FROM react_live_dashboard_v3",
        "openai_real": "SELECT COUNT(*) FROM openai_real_requests_v3",
        "ocr_real": "SELECT COUNT(*) FROM ocr_pdf_real_v3",
        "portail_live": "SELECT COUNT(*) FROM portail_client_live_v3",
        "websocket_live": "SELECT COUNT(*) FROM websocket_live_real_v3",
        "production": "SELECT COUNT(*) FROM production_deploiement_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats

