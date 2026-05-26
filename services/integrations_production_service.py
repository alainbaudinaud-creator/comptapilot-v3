from sqlalchemy import text
from database import engine
from datetime import datetime


def initialiser_integrations_production():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS integrations_production_v3 (
                id SERIAL PRIMARY KEY,
                integration VARCHAR(100),
                statut VARCHAR(50),
                mode_execution VARCHAR(100),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM integrations_production_v3
        """)).scalar() or 0

        if existing == 0:
            integrations = [
                ("OPENAI_API", "READY_CONFIG", "OPTIONNEL", "Clé API à brancher via variable OPENAI_API_KEY"),
                ("TESSERACT_OCR", "READY_CONFIG", "LOCAL", "Moteur OCR prêt à activer"),
                ("CELERY_WORKERS", "READY_CONFIG", "ASYNC", "Workers prêts à connecter à Redis"),
                ("REDIS_QUEUE", "READY_CONFIG", "QUEUE", "Broker prêt via REDIS_URL"),
                ("PDF_ENGINE", "READY_CONFIG", "EXPORT", "Génération PDF métier prête"),
                ("EXCEL_EXPORT", "READY_CONFIG", "EXPORT", "Exports Excel/FEC prêts"),
                ("DSP2_BANKING", "ROADMAP", "CONNECTEUR", "Connecteurs bancaires à brancher"),
                ("PDP_PEPPOL", "ROADMAP", "REGLEMENTAIRE", "Flux facture électronique à brancher"),
            ]

            for integration, statut, mode_execution, message in integrations:
                conn.execute(text("""
                    INSERT INTO integrations_production_v3
                    (integration, statut, mode_execution, message)
                    VALUES
                    (:integration, :statut, :mode_execution, :message)
                """), {
                    "integration": integration,
                    "statut": statut,
                    "mode_execution": mode_execution,
                    "message": message,
                })


def dashboard_integrations_production():

    initialiser_integrations_production()

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, integration, statut, mode_execution, message, created_at
            FROM integrations_production_v3
            ORDER BY id
        """)).mappings().all()

    return {
        "total": len(rows),
        "items": [dict(row) for row in rows],
        "server_time": datetime.utcnow().isoformat(),
    }


