from sqlalchemy import text
from database import engine


def initialiser_produit_final():

    statements = [
        """
        CREATE TABLE IF NOT EXISTS portail_client_final_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            email VARCHAR(255),
            statut VARCHAR(50),
            dernier_acces TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ged_probatoire_final_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            nom_document VARCHAR(255),
            type_document VARCHAR(100),
            chemin_document TEXT,
            hash_sha256 TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS signature_electronique_final_v3 (
            id SERIAL PRIMARY KEY,
            document_id INTEGER,
            signataire VARCHAR(255),
            statut VARCHAR(50),
            preuve_signature TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pdp_facture_electronique_v3 (
            id SERIAL PRIMARY KEY,
            facture_numero VARCHAR(100),
            sens VARCHAR(20),
            statut_pdp VARCHAR(100),
            format_facture VARCHAR(50),
            flux TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notifications_temps_reel_v3 (
            id SERIAL PRIMARY KEY,
            canal VARCHAR(100),
            message TEXT,
            niveau VARCHAR(50),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS emails_automatiques_v3 (
            id SERIAL PRIMARY KEY,
            destinataire VARCHAR(255),
            sujet VARCHAR(255),
            contenu TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS facturation_saas_final_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            plan VARCHAR(100),
            montant_ht NUMERIC(14,2),
            montant_tva NUMERIC(14,2),
            montant_ttc NUMERIC(14,2),
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS api_produit_final_v3 (
            id SERIAL PRIMARY KEY,
            endpoint VARCHAR(255),
            methode VARCHAR(20),
            statut VARCHAR(50),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))

        existing = conn.execute(text("SELECT COUNT(*) FROM api_produit_final_v3")).scalar() or 0

        if existing == 0:
            endpoints = [
                ("/api/v3/portail-client", "GET", "Portail client"),
                ("/api/v3/ged", "GET", "GED probatoire"),
                ("/api/v3/signature", "POST", "Signature électronique"),
                ("/api/v3/pdp/facture", "POST", "Facture électronique PDP"),
                ("/api/v3/notifications", "GET", "Notifications temps réel"),
                ("/api/v3/emails", "POST", "Emails automatiques"),
                ("/api/v3/facturation", "GET", "Facturation SaaS"),
            ]

            for endpoint, methode, description in endpoints:
                conn.execute(text("""
                    INSERT INTO api_produit_final_v3 (endpoint, methode, statut, description)
                    VALUES (:endpoint, :methode, 'PRET', :description)
                """), {
                    "endpoint": endpoint,
                    "methode": methode,
                    "description": description,
                })

            conn.execute(text("""
                INSERT INTO portail_client_final_v3 (client_id, email, statut, dernier_acces)
                VALUES (1, 'client.demo@comptapilot.local', 'ACTIF', NOW())
            """))

            conn.execute(text("""
                INSERT INTO notifications_temps_reel_v3 (canal, message, niveau, statut)
                VALUES ('DASHBOARD', 'Nouveau document disponible', 'INFO', 'ACTIVE')
            """))

            conn.execute(text("""
                INSERT INTO emails_automatiques_v3 (destinataire, sujet, contenu, statut)
                VALUES ('client.demo@comptapilot.local', 'Documents comptables disponibles', 'Vos documents sont prêts dans le portail.', 'PRET')
            """))

            conn.execute(text("""
                INSERT INTO pdp_facture_electronique_v3 (facture_numero, sens, statut_pdp, format_facture, flux)
                VALUES ('F-PDP-0001', 'EMISSION', 'PREPARATION', 'FACTUR-X', 'Flux PDP demo V3')
            """))

            conn.execute(text("""
                INSERT INTO facturation_saas_final_v3 (client_id, plan, montant_ht, montant_tva, montant_ttc, statut)
                VALUES (1, 'PRO_CABINET', 149.00, 29.80, 178.80, 'ACTIVE')
            """))


def dashboard_produit_final():

    stats = {}
    queries = {
        "portail_client": "SELECT COUNT(*) FROM portail_client_final_v3",
        "ged_probatoire": "SELECT COUNT(*) FROM ged_probatoire_final_v3",
        "signatures": "SELECT COUNT(*) FROM signature_electronique_final_v3",
        "pdp": "SELECT COUNT(*) FROM pdp_facture_electronique_v3",
        "notifications": "SELECT COUNT(*) FROM notifications_temps_reel_v3",
        "emails": "SELECT COUNT(*) FROM emails_automatiques_v3",
        "facturation": "SELECT COUNT(*) FROM facturation_saas_final_v3",
        "api": "SELECT COUNT(*) FROM api_produit_final_v3",
    }

    with engine.connect() as conn:
        for key, query in queries.items():
            try:
                stats[key] = conn.execute(text(query)).scalar() or 0
            except Exception:
                stats[key] = 0

    return stats

