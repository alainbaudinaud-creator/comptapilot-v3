from sqlalchemy import text
from database import engine

def charger_taches_revision():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                id,
                COALESCE(titre, 'Tâche') AS titre,
                COALESCE(priorite, 'NORMALE') AS priorite,
                COALESCE(statut, 'A_FAIRE') AS statut,
                COALESCE(client_id, 0) AS client_id
            FROM taches_cabinet_v3
            ORDER BY id DESC
            LIMIT 20
        """)).mappings().all()

    taches = [[r["client_id"], r["titre"], r["priorite"], r["statut"]] for r in rows]

    kpis = {
        "total": len(taches),
        "terminees": sum(1 for t in taches if str(t[3]).upper() in ("TERMINE","TERMINEE","VALIDEE","VALIDÉE","OK")),
        "ouvertes": sum(1 for t in taches if str(t[3]).upper() not in ("TERMINE","TERMINEE","VALIDEE","VALIDÉE","OK")),
        "critiques": sum(1 for t in taches if str(t[2]).upper() in ("CRITIQUE","HAUTE","URGENT"))
    }

    return kpis, taches

def modifier_statut_tache_revision(tache_id, nouveau_statut):
    """
    Modifie le statut d'une tâche de révision dans taches_cabinet_v3.
    """
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE taches_cabinet_v3
            SET statut = :nouveau_statut
            WHERE id = :tache_id
        """), {
            "nouveau_statut": nouveau_statut,
            "tache_id": tache_id
        })

    return {"success": True, "tache_id": tache_id, "nouveau_statut": nouveau_statut}
