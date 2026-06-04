from sqlalchemy import text
from database import engine


def charger_salle_supervision():
    with engine.connect() as conn:
        k = conn.execute(text("""
            SELECT
                (SELECT COUNT(*) FROM clients_v3) AS clients,
                (SELECT COUNT(*) FROM taches_cabinet_v3 WHERE UPPER(COALESCE(statut,'')) NOT IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS taches_ouvertes,
                (SELECT COUNT(*) FROM workflow_cabinet_v3 WHERE UPPER(COALESCE(statut,'')) NOT IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS workflow_ouverts,
                (SELECT COUNT(*) FROM pieces_v3 WHERE statut_validation <> 'VALIDEE') AS pieces_a_valider,
                (SELECT COUNT(*) FROM notifications_cabinet_v3) AS notifications
        """)).mappings().first()

        rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale, 'Client non identifié') AS client,
                COALESCE(w.module, 'Supervision') AS module,
                COALESCE(w.etape, 'Contrôle cabinet') AS etape,
                COALESCE(w.statut, 'A_FAIRE') AS statut,
                COALESCE(w.responsable, 'Système') AS responsable
            FROM workflow_cabinet_v3 w
            LEFT JOIN clients_v3 c ON c.id = w.client_id
            ORDER BY w.created_at DESC, w.id DESC
            LIMIT 20
        """)).mappings().all()

    alertes = int(k["taches_ouvertes"] or 0) + int(k["workflow_ouverts"] or 0) + int(k["pieces_a_valider"] or 0)
    score = max(0, min(100, 100 - alertes * 2))

    kpis = {
        "clients": int(k["clients"] or 0),
        "taches_ouvertes": int(k["taches_ouvertes"] or 0),
        "workflow_ouverts": int(k["workflow_ouverts"] or 0),
        "pieces_a_valider": int(k["pieces_a_valider"] or 0),
        "notifications": int(k["notifications"] or 0),
        "score": score,
    }

    supervision = [
        [r["client"], r["module"], r["etape"], r["statut"], r["responsable"]]
        for r in rows
    ]

    return kpis, supervision
