from sqlalchemy import text

from database import engine


def charger_orchestration_postgres():
    with engine.connect() as conn:
        clients_total = conn.execute(text("""
            SELECT COUNT(*) FROM clients_v3
        """)).scalar() or 0

        clients_revision = conn.execute(text("""
            SELECT COUNT(*) FROM clients_v3
            WHERE statut IN ('REVISION', 'VALIDATION_EC')
        """)).scalar() or 0

        taches_ouvertes = conn.execute(text("""
            SELECT COUNT(*) FROM taches_cabinet_v3
            WHERE statut <> 'TERMINE'
        """)).scalar() or 0

        taches_critiques = conn.execute(text("""
            SELECT COUNT(*) FROM taches_cabinet_v3
            WHERE statut <> 'TERMINE'
              AND priorite IN ('HAUTE', 'CRITIQUE')
        """)).scalar() or 0

        notifications_non_lues = conn.execute(text("""
            SELECT COUNT(*) FROM notifications_cabinet_v3
            WHERE statut = 'NON_LUE'
        """)).scalar() or 0

        clients = conn.execute(text("""
            SELECT id, raison_sociale, statut
            FROM clients_v3
            ORDER BY id
            LIMIT 10
        """)).mappings().all()

        taches = conn.execute(text("""
            SELECT
                t.id,
                t.titre,
                t.priorite,
                t.statut,
                t.echeance,
                c.raison_sociale
            FROM taches_cabinet_v3 t
            JOIN clients_v3 c ON c.id = t.client_id
            WHERE t.statut <> 'TERMINE'
            ORDER BY
                CASE t.priorite
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'WARNING' THEN 3
                    ELSE 4
                END,
                t.id
            LIMIT 10
        """)).mappings().all()

        notifications = conn.execute(text("""
            SELECT
                n.id,
                n.titre,
                n.niveau,
                n.statut,
                c.raison_sociale
            FROM notifications_cabinet_v3 n
            LEFT JOIN clients_v3 c ON c.id = n.client_id
            WHERE n.statut = 'NON_LUE'
            ORDER BY n.id DESC
            LIMIT 10
        """)).mappings().all()

    score_global = max(0, min(100, 100 - taches_critiques * 3 - notifications_non_lues * 2))

    kpis = {
        "clients_total": clients_total,
        "clients_revision": clients_revision,
        "taches_ouvertes": taches_ouvertes,
        "taches_critiques": taches_critiques,
        "notifications_non_lues": notifications_non_lues,
        "score_global": score_global,
    }

    return {
        "kpis": kpis,
        "clients": [dict(x) for x in clients],
        "taches": [dict(x) for x in taches],
        "notifications": [dict(x) for x in notifications],
    }
