from sqlalchemy import text
from database import engine


def charger_taches_revision():
    with engine.connect() as conn:
        k = conn.execute(text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut,'')) IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS terminees,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut,'')) NOT IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS ouvertes,
                COUNT(*) FILTER (
                    WHERE UPPER(COALESCE(priorite,'')) IN ('CRITIQUE','HAUTE','URGENT')
                    AND UPPER(COALESCE(statut,'')) NOT IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')
                ) AS critiques
            FROM taches_cabinet_v3
        """)).mappings().first()

        rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale, 'Client non identifié') AS client,
                COALESCE(t.titre, 'Tâche cabinet') AS titre,
                COALESCE(t.priorite, 'NORMALE') AS priorite,
                COALESCE(t.statut, 'A_FAIRE') AS statut,
                COALESCE(t.echeance::text, '-') AS echeance
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c ON c.id = t.client_id
            ORDER BY
                CASE UPPER(COALESCE(t.priorite,''))
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'URGENT' THEN 3
                    ELSE 4
                END,
                t.echeance NULLS LAST,
                t.id DESC
            LIMIT 20
        """)).mappings().all()

    total = int(k["total"] or 0)
    terminees = int(k["terminees"] or 0)

    kpis = {
        "total": total,
        "terminees": terminees,
        "ouvertes": int(k["ouvertes"] or 0),
        "critiques": int(k["critiques"] or 0),
        "score": 100 if total == 0 else round((terminees / total) * 100),
    }

    taches = [
        [r["client"], r["titre"], r["priorite"], r["statut"], r["echeance"]]
        for r in rows
    ]

    return kpis, taches
