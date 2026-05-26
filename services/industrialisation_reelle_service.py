from sqlalchemy import text
from database import engine


def initialiser_industrialisation_reelle():

    statements = [
        """
        CREATE TABLE IF NOT EXISTS ocr_reel_v3 (
            id SERIAL PRIMARY KEY,
            nom_fichier VARCHAR(255),
            moteur VARCHAR(100),
            texte_extrait TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS openai_analyses_v3 (
            id SERIAL PRIMARY KEY,
            type_analyse VARCHAR(100),
            prompt TEXT,
            resultat TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fec_import_reel_v3 (
            id SERIAL PRIMARY KEY,
            nom_fichier VARCHAR(255),
            journal_code VARCHAR(50),
            compte VARCHAR(50),
            piece VARCHAR(255),
            libelle TEXT,
            debit NUMERIC(14,2),
            credit NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS banques_import_reel_v3 (
            id SERIAL PRIMARY KEY,
            nom_fichier VARCHAR(255),
            date_operation DATE,
            libelle TEXT,
            montant NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS api_rest_v3 (
            id SERIAL PRIMARY KEY,
            endpoint VARCHAR(255),
            methode VARCHAR(20),
            statut VARCHAR(50),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS monitoring_production_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(255),
            statut VARCHAR(50),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS files_attente_ia_v3 (
            id SERIAL PRIMARY KEY,
            job_type VARCHAR(100),
            payload TEXT,
            statut VARCHAR(50),
            priorite INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ged_probatoire_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            nom_document VARCHAR(255),
            type_document VARCHAR(100),
            hash_sha256 TEXT,
            chemin TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))

        existing = conn.execute(text("SELECT COUNT(*) FROM api_rest_v3")).scalar() or 0

        if existing == 0:
            endpoints = [
                ("/api/v3/clients", "GET", "Clients cabinet"),
                ("/api/v3/ecritures", "GET", "Écritures comptables"),
                ("/api/v3/ocr", "POST", "Analyse OCR"),
                ("/api/v3/fec/import", "POST", "Import FEC"),
                ("/api/v3/banque/import", "POST", "Import bancaire"),
                ("/api/v3/dashboard", "GET", "Dashboard cabinet"),
            ]

            for endpoint, methode, description in endpoints:
                conn.execute(text("""
                    INSERT INTO api_rest_v3 (endpoint, methode, statut, description)
                    VALUES (:endpoint, :methode, 'PRET', :description)
                """), {
                    "endpoint": endpoint,
                    "methode": methode,
                    "description": description,
                })

            conn.execute(text("""
                INSERT INTO monitoring_production_v3 (service, statut, message)
                VALUES ('GUNICORN', 'OK', 'Serveur applicatif actif')
            """))

            conn.execute(text("""
                INSERT INTO monitoring_production_v3 (service, statut, message)
                VALUES ('POSTGRES', 'OK', 'Base métier disponible')
            """))

            conn.execute(text("""
                INSERT INTO files_attente_ia_v3 (job_type, payload, statut, priorite)
                VALUES ('OCR_REEL', 'Traitement pièce comptable', 'EN_ATTENTE', 1)
            """))


def dashboard_industrialisation_reelle():

    stats = {}

    queries = {
        "ocr_reel": "SELECT COUNT(*) FROM ocr_reel_v3",
        "openai_analyses": "SELECT COUNT(*) FROM openai_analyses_v3",
        "fec_import_reel": "SELECT COUNT(*) FROM fec_import_reel_v3",
        "banques_import_reel": "SELECT COUNT(*) FROM banques_import_reel_v3",
        "api_rest": "SELECT COUNT(*) FROM api_rest_v3",
        "monitoring": "SELECT COUNT(*) FROM monitoring_production_v3",
        "files_attente_ia": "SELECT COUNT(*) FROM files_attente_ia_v3",
        "ged_probatoire": "SELECT COUNT(*) FROM ged_probatoire_v3",
    }

    with engine.connect() as conn:
        for key, query in queries.items():
            try:
                stats[key] = conn.execute(text(query)).scalar() or 0
            except Exception:
                stats[key] = 0

    return stats


