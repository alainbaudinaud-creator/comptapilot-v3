from sqlalchemy import text
from database import engine


def initialiser_plateforme_cabinet():

    statements = [
        """
        CREATE TABLE IF NOT EXISTS collaborateurs_v3 (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            role VARCHAR(100),
            actif BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS societes_v3 (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            siren VARCHAR(20),
            statut VARCHAR(50) DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS permissions_v3 (
            id SERIAL PRIMARY KEY,
            collaborateur_id INTEGER,
            module VARCHAR(100),
            lecture BOOLEAN DEFAULT TRUE,
            ecriture BOOLEAN DEFAULT FALSE,
            administration BOOLEAN DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notifications_v3 (
            id SERIAL PRIMARY KEY,
            type_notification VARCHAR(100),
            message TEXT,
            niveau VARCHAR(50),
            statut VARCHAR(50) DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS historique_actions_v3 (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(255),
            action VARCHAR(255),
            module VARCHAR(100),
            detail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS coffre_fort_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            nom_document VARCHAR(255),
            chemin_document TEXT,
            hash_document TEXT,
            statut VARCHAR(50) DEFAULT 'ARCHIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS api_tokens_v3 (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(255),
            token TEXT,
            actif BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS supervision_dossiers_v3 (
            id SERIAL PRIMARY KEY,
            client_id INTEGER,
            module VARCHAR(100),
            statut VARCHAR(50),
            progression INTEGER DEFAULT 0,
            commentaire TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS connecteurs_externes_v3 (
            id SERIAL PRIMARY KEY,
            type_connecteur VARCHAR(100),
            statut VARCHAR(50),
            configuration TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS exports_reglementaires_v3 (
            id SERIAL PRIMARY KEY,
            type_export VARCHAR(100),
            chemin_export TEXT,
            statut VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    with engine.begin() as conn:

        for statement in statements:
            conn.execute(text(statement))

        existing = conn.execute(text("SELECT COUNT(*) FROM collaborateurs_v3")).scalar() or 0

        if existing == 0:
            conn.execute(text("""
                INSERT INTO collaborateurs_v3 (nom, email, role)
                VALUES ('Admin Cabinet', 'admin@comptapilot.local', 'EXPERT_COMPTABLE')
            """))

            conn.execute(text("""
                INSERT INTO societes_v3 (nom, siren)
                VALUES ('CLIENT DEMO COMPTAPILOT', '000000000')
            """))

            conn.execute(text("""
                INSERT INTO notifications_v3 (type_notification, message, niveau)
                VALUES ('PRODUCTION', 'Clôture exercice à contrôler', 'IMPORTANT')
            """))

            conn.execute(text("""
                INSERT INTO historique_actions_v3 (utilisateur, action, module, detail)
                VALUES ('SYSTEM', 'INITIALISATION', 'PLATEFORME_CABINET', 'Initialisation plateforme industrielle V3')
            """))

            for connecteur in ["PEPPOL", "CHORUS_PRO", "PDP"]:
                conn.execute(text("""
                    INSERT INTO connecteurs_externes_v3 (type_connecteur, statut, configuration)
                    VALUES (:connecteur, 'PREPARATION', 'Configuration V3')
                """), {"connecteur": connecteur})


def dashboard_plateforme():

    stats = {}

    queries = {
        "collaborateurs": "SELECT COUNT(*) FROM collaborateurs_v3",
        "societes": "SELECT COUNT(*) FROM societes_v3",
        "notifications": "SELECT COUNT(*) FROM notifications_v3",
        "historique": "SELECT COUNT(*) FROM historique_actions_v3",
        "coffre_fort": "SELECT COUNT(*) FROM coffre_fort_v3",
        "tokens_api": "SELECT COUNT(*) FROM api_tokens_v3",
        "supervision": "SELECT COUNT(*) FROM supervision_dossiers_v3",
        "connecteurs": "SELECT COUNT(*) FROM connecteurs_externes_v3",
        "exports": "SELECT COUNT(*) FROM exports_reglementaires_v3",
    }

    with engine.connect() as conn:
        for key, query in queries.items():
            try:
                stats[key] = conn.execute(text(query)).scalar() or 0
            except Exception:
                stats[key] = 0

    return stats


