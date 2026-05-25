from sqlalchemy import text
from database import engine


def initialiser_finalisation_industrielle():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS react_frontend_v3 (
            id SERIAL PRIMARY KEY,
            module VARCHAR(100),
            version VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS websocket_live_v3 (
            id SERIAL PRIMARY KEY,
            canal VARCHAR(100),
            evenement VARCHAR(255),
            payload TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS jwt_security_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            role_utilisateur VARCHAR(100),
            token_hash TEXT,
            expiration TIMESTAMP,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS openai_structured_v3 (
            id SERIAL PRIMARY KEY,
            type_analyse VARCHAR(100),
            modele_ia VARCHAR(100),
            prompt_utilise TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS tesseract_ocr_v3 (
            id SERIAL PRIMARY KEY,
            fichier_source VARCHAR(255),
            langue_ocr VARCHAR(20),
            texte_extrait TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS rapprochement_ia_live_v3 (
            id SERIAL PRIMARY KEY,
            reference_banque VARCHAR(255),
            reference_comptable VARCHAR(255),
            score_ia INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS lettrage_ia_live_v3 (
            id SERIAL PRIMARY KEY,
            compte VARCHAR(50),
            piece VARCHAR(255),
            score_ia INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS pdf_professionnels_v3 (
            id SERIAL PRIMARY KEY,
            type_document VARCHAR(100),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS stripe_saas_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            abonnement VARCHAR(100),
            stripe_customer_id VARCHAR(255),
            stripe_subscription_id VARCHAR(255),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS devops_supervision_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(100),
            environnement VARCHAR(50),
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
            FROM react_frontend_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO react_frontend_v3
                (module, version, statut)
                VALUES
                (
                    'DASHBOARD_REACT',
                    'V3.0',
                    'ACTIF'
                )
            """))

            conn.execute(text("""
                INSERT INTO websocket_live_v3
                (canal, evenement, payload, statut)
                VALUES
                (
                    'dashboard_live',
                    'NOUVELLE_ANALYSE_IA',
                    'Analyse IA temps réel',
                    'EMIS'
                )
            """))

            conn.execute(text("""
                INSERT INTO openai_structured_v3
                (type_analyse, modele_ia, prompt_utilise, statut)
                VALUES
                (
                    'ANALYSE_FACTURE',
                    'GPT-5.5',
                    'Analyse comptable structurée',
                    'ACTIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO tesseract_ocr_v3
                (fichier_source, langue_ocr, texte_extrait, statut)
                VALUES
                (
                    'facture_demo.pdf',
                    'fra',
                    'Texte OCR extrait automatiquement',
                    'TRAITE'
                )
            """))

            conn.execute(text("""
                INSERT INTO stripe_saas_v3
                (client_id, abonnement, stripe_customer_id, stripe_subscription_id, statut)
                VALUES
                (
                    1,
                    'PRO_CABINET',
                    'cus_demo_v3',
                    'sub_demo_v3',
                    'ACTIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO devops_supervision_v3
                (service, environnement, cpu, memoire, statut)
                VALUES
                (
                    'COMPTAPILOT_API',
                    'PRODUCTION',
                    22.5,
                    48.0,
                    'OK'
                )
            """))

            conn.execute(text("""
                INSERT INTO rapprochement_ia_live_v3
                (reference_banque, reference_comptable, score_ia, statut)
                VALUES
                (
                    'BANK-2026-001',
                    'ECR-2026-001',
                    96,
                    'RAPPROCHE'
                )
            """))

            conn.execute(text("""
                INSERT INTO lettrage_ia_live_v3
                (compte, piece, score_ia, statut)
                VALUES
                (
                    '411000',
                    'FAC-2026-001',
                    94,
                    'LETTRE'
                )
            """))


def dashboard_finalisation_industrielle():

    stats = {}

    queries = {
        "react_frontend": "SELECT COUNT(*) FROM react_frontend_v3",
        "websocket_live": "SELECT COUNT(*) FROM websocket_live_v3",
        "jwt_security": "SELECT COUNT(*) FROM jwt_security_v3",
        "openai": "SELECT COUNT(*) FROM openai_structured_v3",
        "tesseract": "SELECT COUNT(*) FROM tesseract_ocr_v3",
        "rapprochement_ia": "SELECT COUNT(*) FROM rapprochement_ia_live_v3",
        "lettrage_ia": "SELECT COUNT(*) FROM lettrage_ia_live_v3",
        "pdf": "SELECT COUNT(*) FROM pdf_professionnels_v3",
        "stripe": "SELECT COUNT(*) FROM stripe_saas_v3",
        "devops": "SELECT COUNT(*) FROM devops_supervision_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats
