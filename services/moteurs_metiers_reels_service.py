from sqlalchemy import text
from database import engine


def initialiser_moteurs_metiers_reels():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS import_fec_reel_v3 (
            id SERIAL PRIMARY KEY,
            nom_fichier VARCHAR(255),
            journal_code VARCHAR(50),
            compte_num VARCHAR(50),
            piece_ref VARCHAR(255),
            ecriture_lib TEXT,
            debit NUMERIC(14,2),
            credit NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS import_bancaire_reel_v3 (
            id SERIAL PRIMARY KEY,
            banque VARCHAR(255),
            date_operation DATE,
            libelle TEXT,
            montant NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS rapprochement_ia_reel_v3 (
            id SERIAL PRIMARY KEY,
            reference_banque VARCHAR(255),
            reference_comptable VARCHAR(255),
            score_matching INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS lettrage_reel_v3 (
            id SERIAL PRIMARY KEY,
            compte VARCHAR(50),
            piece VARCHAR(255),
            score_ia INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS pdf_generes_v3 (
            id SERIAL PRIMARY KEY,
            type_document VARCHAR(100),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS taches_async_v3 (
            id SERIAL PRIMARY KEY,
            type_tache VARCHAR(100),
            payload TEXT,
            statut VARCHAR(50),
            priorite INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS jwt_utilisateurs_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            token TEXT,
            expiration TIMESTAMP,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS supervision_production_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(255),
            statut VARCHAR(50),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    with engine.begin() as conn:

        for statement in statements:
            conn.execute(text(statement))

        existing = conn.execute(text("""
            SELECT COUNT(*)
            FROM supervision_production_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO supervision_production_v3
                (service, statut, message)
                VALUES
                ('OCR_IA', 'OK', 'Pipeline OCR IA actif')
            """))

            conn.execute(text("""
                INSERT INTO supervision_production_v3
                (service, statut, message)
                VALUES
                ('API_REST', 'OK', 'API REST V3 active')
            """))

            conn.execute(text("""
                INSERT INTO supervision_production_v3
                (service, statut, message)
                VALUES
                ('POSTGRESQL', 'OK', 'Base métier disponible')
            """))

            conn.execute(text("""
                INSERT INTO taches_async_v3
                (type_tache, payload, statut, priorite)
                VALUES
                (
                    'OCR_FACTURE',
                    'Analyse comptable automatique',
                    'EN_ATTENTE',
                    1
                )
            """))

            conn.execute(text("""
                INSERT INTO taches_async_v3
                (type_tache, payload, statut, priorite)
                VALUES
                (
                    'RAPPROCHEMENT_BANCAIRE',
                    'Matching intelligent',
                    'EN_ATTENTE',
                    2
                )
            """))


def dashboard_moteurs_reels():

    stats = {}

    queries = {
        "imports_fec": "SELECT COUNT(*) FROM import_fec_reel_v3",
        "imports_bancaires": "SELECT COUNT(*) FROM import_bancaire_reel_v3",
        "rapprochements": "SELECT COUNT(*) FROM rapprochement_ia_reel_v3",
        "lettrage": "SELECT COUNT(*) FROM lettrage_reel_v3",
        "pdf_generes": "SELECT COUNT(*) FROM pdf_generes_v3",
        "taches_async": "SELECT COUNT(*) FROM taches_async_v3",
        "jwt_utilisateurs": "SELECT COUNT(*) FROM jwt_utilisateurs_v3",
        "supervision": "SELECT COUNT(*) FROM supervision_production_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats
