from sqlalchemy import text
from database import engine


def charger_workflow_cabinet():
    with engine.connect() as conn:
        k = conn.execute(text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut,'')) IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS termines,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut,'')) NOT IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS ouverts,
                COUNT(DISTINCT client_id) AS dossiers,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut,'')) IN ('BLOQUANT','ERREUR')) AS bloquants
            FROM workflow_cabinet_v3
        """)).mappings().first()

        rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale, 'Client non identifié') AS client,
                COALESCE(w.module, 'Workflow') AS module,
                COALESCE(w.etape, 'Étape cabinet') AS etape,
                COALESCE(w.statut, 'A_FAIRE') AS statut,
                COALESCE(w.responsable, 'Non affecté') AS responsable
            FROM workflow_cabinet_v3 w
            LEFT JOIN clients_v3 c ON c.id = w.client_id
            ORDER BY w.created_at DESC, w.id DESC
            LIMIT 20
        """)).mappings().all()

    total = int(k["total"] or 0)
    termines = int(k["termines"] or 0)
    ouverts = int(k["ouverts"] or 0)
    bloquants = int(k["bloquants"] or 0)
    score = 100 if total == 0 else round((termines / total) * 100)

    kpis = {
        "total": total,
        "termines": termines,
        "ouverts": ouverts,
        "bloquants": bloquants,
        "dossiers": int(k["dossiers"] or 0),
        "score": score,
    }

    workflow = [
        [r["client"], r["module"], r["etape"], r["statut"], r["responsable"]]
        for r in rows
    ]

    return kpis, workflow
