import os
from sqlalchemy import create_engine, text


def db_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


def charger_taches_revision():

    engine = create_engine(db_url(), pool_pre_ping=True)

    with engine.connect() as conn:

        rows = conn.execute(text("""
            SELECT
                id,
                titre,
                priorite,
                statut,
                echeance,
                created_at
            FROM taches_cabinet_v3
            ORDER BY id DESC
            LIMIT 50
        """)).mappings().all()

    return {
        "nb_taches": len(rows),
        "taches": [dict(r) for r in rows]
    }
