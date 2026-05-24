from datetime import datetime
from sqlalchemy import text
from database import engine


def initialiser_ia_industrielle():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS ia_jobs_v3 (
            id SERIAL PRIMARY KEY,
            type_job VARCHAR(100),
            statut VARCHAR(50),
            priorite INTEGER DEFAULT 1,
            payload TEXT,
            resultat TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS audit_legal_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            action VARCHAR(255),
            module VARCHAR(100),
            detail TEXT,
            adresse_ip VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS api_jwt_tokens_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            token TEXT,
            expiration TIMESTAMP,
            actif BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS imports_fec_v3 (
            id SERIAL PRIMARY KEY,
            nom_fichier VARCHAR(255),
            statut VARCHAR(50),
            nb_ecritures INTEGER DEFAULT 0,
            rapport TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS imports_bancaires_v3 (
            id SERIAL PRIMARY KEY,
            banque VARCHAR(255),
            nom_fichier VARCHAR(255),
            nb_operations INTEGER DEFAULT 0,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS rapprochements_bancaires_v3 (
            id SERIAL PRIMARY KEY,
            reference_operation VARCHAR(255),
            statut VARCHAR(50),
            score_matching INTEGER,
            commentaire TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS lettrage_automatique_v3 (
            id SERIAL PRIMARY KEY,
            compte VARCHAR(50),
            piece VARCHAR(255),
            statut VARCHAR(50),
            score_ia INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS dashboard_temps_reel_v3 (
            id SERIAL PRIMARY KEY,
            indicateur VARCHAR(255),
            valeur NUMERIC(14,2),
            categorie VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS exports_pdf_v3 (
            id SERIAL PRIMARY KEY,
            type_document VARCHAR(100),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS liasses_fiscales_v3 (
            id SERIAL PRIMARY KEY,
            exercice VARCHAR(50),
            statut VARCHAR(50),
            chemin_generation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS plaquettes_v3 (
            id SERIAL PRIMARY KEY,
            exercice VARCHAR(50),
            statut VARCHAR(50),
            chemin_generation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    with engine.begin() as conn:

        for statement in statements:
            conn.execute(text(statement))

        existing = conn.execute(text("""
            SELECT COUNT(*)
            FROM ia_jobs_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO ia_jobs_v3
                (type_job, statut, priorite, payload)
                VALUES
                (
                    'OCR_FACTURE',
                    'EN_ATTENTE',
                    1,
                    'Analyse OCR comptable'
                )
            """))

            conn.execute(text("""
                INSERT INTO ia_jobs_v3
                (type_job, statut, priorite, payload)
                VALUES
                (
                    'RAPPROCHEMENT_BANCAIRE',
                    'EN_ATTENTE',
                    2,
                    'Matching bancaire IA'
                )
            """))

            conn.execute(text("""
                INSERT INTO dashboard_temps_reel_v3
                (indicateur, valeur, categorie)
                VALUES
                ('Dossiers actifs', 12, 'CABINET')
            """))

            conn.execute(text("""
                INSERT INTO dashboard_temps_reel_v3
                (indicateur, valeur, categorie)
                VALUES
                ('Pièces OCR traitées', 248, 'IA')
            """))

            conn.execute(text("""
                INSERT INTO dashboard_temps_reel_v3
                (indicateur, valeur, categorie)
                VALUES
                ('Écritures générées', 1260, 'COMPTABILITE')
            """))


def dashboard_ia():

    stats = {}

    queries = {
        "jobs_ia": "SELECT COUNT(*) FROM ia_jobs_v3",
        "audit_legal": "SELECT COUNT(*) FROM audit_legal_v3",
        "tokens_jwt": "SELECT COUNT(*) FROM api_jwt_tokens_v3",
        "imports_fec": "SELECT COUNT(*) FROM imports_fec_v3",
        "imports_bancaires": "SELECT COUNT(*) FROM imports_bancaires_v3",
        "rapprochements": "SELECT COUNT(*) FROM rapprochements_bancaires_v3",
        "lettrage": "SELECT COUNT(*) FROM lettrage_automatique_v3",
        "dashboard": "SELECT COUNT(*) FROM dashboard_temps_reel_v3",
        "exports_pdf": "SELECT COUNT(*) FROM exports_pdf_v3",
        "liasses": "SELECT COUNT(*) FROM liasses_fiscales_v3",
        "plaquettes": "SELECT COUNT(*) FROM plaquettes_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats
