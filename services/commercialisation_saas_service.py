from sqlalchemy import text
from database import engine


def initialiser_commercialisation_saas():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS utilisateurs_roles_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            role_utilisateur VARCHAR(100),
            permissions TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS rgpd_conformite_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            type_consentement VARCHAR(100),
            statut VARCHAR(50),
            date_validation TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS tva_moteur_v3 (
            id SERIAL PRIMARY KEY,
            periode VARCHAR(20),
            tva_collectee NUMERIC(14,2),
            tva_deductible NUMERIC(14,2),
            tva_a_payer NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS pdf_professionnels_final_v3 (
            id SERIAL PRIMARY KEY,
            type_document VARCHAR(100),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS liasse_fiscale_final_v3 (
            id SERIAL PRIMARY KEY,
            exercice VARCHAR(20),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS plaquette_annuelle_final_v3 (
            id SERIAL PRIMARY KEY,
            exercice VARCHAR(20),
            chemin_document TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS portail_client_responsive_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            plateforme VARCHAR(50),
            derniere_connexion TIMESTAMP,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS kubernetes_cluster_v3 (
            id SERIAL PRIMARY KEY,
            cluster_nom VARCHAR(255),
            nb_nodes INTEGER,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS cicd_pipeline_v3 (
            id SERIAL PRIMARY KEY,
            pipeline_nom VARCHAR(255),
            environnement VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS supervision_production_final_v3 (
            id SERIAL PRIMARY KEY,
            service VARCHAR(255),
            disponibilite NUMERIC(5,2),
            incident VARCHAR(255),
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
            FROM utilisateurs_roles_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO utilisateurs_roles_v3
                (utilisateur, role_utilisateur, permissions, statut)
                VALUES
                (
                    'admin@comptapilot.local',
                    'SUPER_ADMIN',
                    'ALL_PRIVILEGES',
                    'ACTIF'
                )
            """))

            conn.execute(text("""
                INSERT INTO rgpd_conformite_v3
                (client_id, type_consentement, statut, date_validation)
                VALUES
                (
                    1,
                    'TRAITEMENT_DONNEES',
                    'VALIDE',
                    NOW()
                )
            """))

            conn.execute(text("""
                INSERT INTO tva_moteur_v3
                (periode, tva_collectee, tva_deductible, tva_a_payer, statut)
                VALUES
                (
                    '2026-05',
                    24000,
                    9000,
                    15000,
                    'CALCULEE'
                )
            """))

            conn.execute(text("""
                INSERT INTO liasse_fiscale_final_v3
                (exercice, chemin_document, statut)
                VALUES
                (
                    '2025',
                    '/liasses/liasse_2025.pdf',
                    'GENEREE'
                )
            """))

            conn.execute(text("""
                INSERT INTO plaquette_annuelle_final_v3
                (exercice, chemin_document, statut)
                VALUES
                (
                    '2025',
                    '/plaquettes/plaquette_2025.pdf',
                    'GENEREE'
                )
            """))

            conn.execute(text("""
                INSERT INTO portail_client_responsive_v3
                (client_id, plateforme, derniere_connexion, statut)
                VALUES
                (
                    1,
                    'MOBILE',
                    NOW(),
                    'CONNECTE'
                )
            """))

            conn.execute(text("""
                INSERT INTO kubernetes_cluster_v3
                (cluster_nom, nb_nodes, statut)
                VALUES
                (
                    'COMPTAPILOT_CLUSTER',
                    3,
                    'ONLINE'
                )
            """))

            conn.execute(text("""
                INSERT INTO cicd_pipeline_v3
                (pipeline_nom, environnement, statut)
                VALUES
                (
                    'DEPLOY_PRODUCTION',
                    'PROD',
                    'SUCCESS'
                )
            """))

            conn.execute(text("""
                INSERT INTO supervision_production_final_v3
                (service, disponibilite, incident, statut)
                VALUES
                (
                    'COMPTAPILOT_API',
                    99.98,
                    'AUCUN',
                    'OK'
                )
            """))


def dashboard_commercialisation():

    stats = {}

    queries = {
        "roles": "SELECT COUNT(*) FROM utilisateurs_roles_v3",
        "rgpd": "SELECT COUNT(*) FROM rgpd_conformite_v3",
        "tva": "SELECT COUNT(*) FROM tva_moteur_v3",
        "pdf": "SELECT COUNT(*) FROM pdf_professionnels_final_v3",
        "liasse": "SELECT COUNT(*) FROM liasse_fiscale_final_v3",
        "plaquette": "SELECT COUNT(*) FROM plaquette_annuelle_final_v3",
        "portail": "SELECT COUNT(*) FROM portail_client_responsive_v3",
        "kubernetes": "SELECT COUNT(*) FROM kubernetes_cluster_v3",
        "cicd": "SELECT COUNT(*) FROM cicd_pipeline_v3",
        "supervision": "SELECT COUNT(*) FROM supervision_production_final_v3",
    }

    with engine.connect() as conn:

        for key, query in queries.items():

            try:
                stats[key] = conn.execute(text(query)).scalar() or 0

            except Exception:
                stats[key] = 0

    return stats
