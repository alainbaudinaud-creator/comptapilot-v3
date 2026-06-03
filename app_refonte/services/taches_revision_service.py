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


def modifier_statut_tache_revision(tache_id, statut):
    statuts_autorises = ["A_FAIRE", "EN_COURS", "TERMINE"]
    statut = (statut or "").upper().strip()

    if statut not in statuts_autorises:
        return {
            "success": False,
            "message": "Statut invalide",
            "statuts_autorises": statuts_autorises
        }

    engine = create_engine(db_url(), pool_pre_ping=True)

    with engine.begin() as conn:
        row = conn.execute(text("""
            UPDATE taches_cabinet_v3
            SET statut = :statut
            WHERE id = :tache_id
            RETURNING id, titre, priorite, statut, echeance, created_at
        """), {
            "statut": statut,
            "tache_id": tache_id
        }).mappings().first()

    if not row:
        return {
            "success": False,
            "message": "Tâche introuvable",
            "tache_id": tache_id
        }

    return {
        "success": True,
        "message": "Statut mis à jour",
        "tache": dict(row)
    }
