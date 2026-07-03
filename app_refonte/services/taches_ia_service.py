from sqlalchemy import text
from database import engine


def charger_taches_ia():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale, 'Client non identifié') AS client,
                COALESCE(t.titre, 'Contrôle IA') AS titre,
                COALESCE(t.priorite, 'NORMALE') AS priorite,
                COALESCE(t.statut, 'A_FAIRE') AS statut
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c ON c.id = t.client_id
            WHERE
                t.titre ILIKE '%IA%'
                OR t.titre ILIKE '%contrô%'
                OR t.titre ILIKE '%controle%'
                OR UPPER(COALESCE(t.priorite,'')) IN ('CRITIQUE','HAUTE','URGENT')
            ORDER BY t.id DESC
            LIMIT 20
        """)).mappings().all()

    taches = [[r["client"], r["titre"], r["priorite"], r["statut"]] for r in rows]

    kpis = {
        "taches_ia": len(taches),
        "critiques": sum(1 for t in taches if str(t[2]).upper() in ("CRITIQUE", "HAUTE", "URGENT")),
        "a_traiter": sum(1 for t in taches if str(t[3]).upper() not in ("TERMINE", "TERMINEE", "VALIDEE", "VALIDÉE", "OK")),
    }

    return kpis, taches


def generer_taches_depuis_plan_ia(plan=None, client_id=None):
    """
    Compatibilité avec app_refonte.py.
    Génère une liste de tâches IA à partir des données PostgreSQL actuelles.
    """
    kpis, taches = charger_taches_ia()

    suggestions = []
    for t in taches[:10]:
        suggestions.append({
            "client": t[0],
            "titre": t[1],
            "priorite": t[2],
            "statut": t[3],
            "source": "PostgreSQL",
        })

    return {
        "success": True,
        "kpis": kpis,
        "taches": suggestions,
        "client_id": client_id,
        "plan": plan or "plan_ia_cabinet",
    }
