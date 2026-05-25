from sqlalchemy import text
from database import engine


def initialiser_automatisation_cabinet():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS rapprochement_bancaire_auto_v3 (
            id SERIAL PRIMARY KEY,
            reference_banque VARCHAR(255),
            reference_comptable VARCHAR(255),
            montant NUMERIC(14,2),
            score_matching INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS lettrage_auto_v3 (
            id SERIAL PRIMARY KEY,
            compte VARCHAR(50),
            piece VARCHAR(255),
            montant NUMERIC(14,2),
            score_ia INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS balance_temps_reel_v3 (
            id SERIAL PRIMARY KEY,
            compte VARCHAR(50),
            libelle VARCHAR(255),
            debit NUMERIC(14,2),
            credit NUMERIC(14,2),
            solde NUMERIC(14,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS pdf_comptables_v3 (
            id SERIAL PRIMARY KEY,
            type_document VARCHAR(100),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS liasses_fiscales_auto_v3 (
            id SERIAL PRIMARY KEY,
            exercice VARCHAR(20),
            chemin_generation TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS plaquettes_annuelles_v3 (
            id SERIAL PRIMARY KEY,
            exercice VARCHAR(20),
            chemin_generation TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS notifications_cabinet_v3 (
            id SERIAL PRIMARY KEY,
            type_notification VARCHAR(100),
            message TEXT,
            niveau VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS scheduler_taches_v3 (
            id SERIAL PRIMARY KEY,
            type_tache VARCHAR(100),
            frequence VARCHAR(100),
            statut VARCHAR(50),
            prochaine_execution TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS emails_cabinet_v3 (
            id SERIAL PRIMARY KEY,
            destinataire VARCHAR(255),
            sujet VARCHAR(255),
            contenu TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS signatures_electroniques_v3 (
            id SERIAL PRIMARY KEY,
            document_nom VARCHAR(255),
            hash_signature TEXT,
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
            FROM notifications_cabinet_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO notifications_cabinet_v3
                (type_notification, message, niveau, statut)
                VALUES
                (
                    'CLOTURE',
                    'Clôture comptable à contrôler',
                    'IMPORTANT',
                    'ACTIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO notifications_cabinet_v3
                (type_notification, message, niveau, statut)
                VALUES
                (
                    'TVA',
                    'Déclaration TVA à produire',
                    'ALERTE',
                    'ACTIVE'
                )
            """))

            conn.execute(text("""
                INSERT INTO scheduler_taches_v3
                (type_tache, frequence, statut, prochaine_execution)
                VALUES
                (
                    'RAPPROCHEMENT_BANCAIRE',
                    'QUOTIDIEN',
                    'ACTIF',
                    NOW()
                )
            """))

            conn.execute(text("""
                INSERT INTO scheduler_taches_v3
                (type_tache, frequence, statut, prochaine_execution)
                VALUES
                (
                    'RELANCE_CLIENT',
                    'HEBDOMADAIRE',
                    'ACTIF',
                    NOW()
                )
            """))

            conn.execute(text("""
                INSERT INTO balance_temps_reel_v3
                (compte, libelle, debit, credit, solde)
                VALUES
                ('706000', 'Prestations', 0, 125000, -125000)
            """))

            conn.execute(text("""
                INSERT INTO balance_temps_reel_v3
                (compte, libelle, debit, credit, solde)
                VALUES
                ('401000', 'Fournisseurs', 22000, 18000, 4000)
            """))

            conn.execute(text("""
                INSERT INTO balance_temps_reel_v3
                (compte, libelle, debit, credit, solde)
                VALUES
                ('512000', 'Banque', 98500, 65000, 33500)
            """))


def dashboard_automatisation():

    stats = {}

    queries = {
        "rapprochements": "SELECT COUNT(*) FROM rapprochement_bancaire_auto_v3",
        "lettrage": "SELECT COUNT(*) FROM lettrage_auto_v3",
        "balance": "SELECT COUNT(*) FROM balance_temps_reel_v3",
        "pdf": "SELECT COUNT(*) FROM pdf_comptables_v3",
        "liasses": "SELECT COUNT(*) FROM liasses_fiscales_auto_v3",
        "plaquettes": "SELECT COUNT(*) FROM plaquettes_annuelles_v3",
        "notifications": "SELECT COUNT(*) FROM notifications_cabinet_v3",
        "scheduler": "SELECT COUNT(*) FROM scheduler_taches_v3",
        "emails": "SELECT COUNT(*) FROM emails_cabinet_v3",
        "signatures": "SELECT COUNT(*) FROM signatures_electroniques_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats
