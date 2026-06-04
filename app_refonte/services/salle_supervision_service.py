from sqlalchemy import text
from database import engine


def charger_salle_supervision():
    with engine.connect() as conn:

        stats = conn.execute(text("""
            WITH clients AS (
                SELECT COUNT(*) AS total
                FROM clients_v3
            ),
            taches AS (
                SELECT COUNT(*) AS ouvertes
                FROM taches_cabinet_v3
                WHERE UPPER(COALESCE(statut,'')) NOT IN
                ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')
            ),
            workflow AS (
                SELECT COUNT(*) AS ouvertes
                FROM workflow_cabinet_v3
                WHERE UPPER(COALESCE(statut,'')) NOT IN
                ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')
            ),
            pieces AS (
                SELECT COUNT(*) AS a_valider
                FROM pieces_v3
                WHERE COALESCE(statut_validation,'') <> 'VALIDEE'
            )
            SELECT
                clients.total AS clients,
                taches.ouvertes AS taches,
                workflow.ouvertes AS workflow,
                pieces.a_valider AS pieces
            FROM clients,taches,workflow,pieces
        """)).mappings().first()

        workflow_rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale,'Client non identifié') AS client,
                COALESCE(w.etape,'Étape cabinet') AS etape,
                COALESCE(w.responsable,'Non affecté') AS responsable,
                CASE
                    WHEN UPPER(COALESCE(w.statut,'')) IN ('BLOQUANT','ERREUR')
                    THEN 'Élevé'
                    ELSE 'Moyen'
                END AS risque,
                '80%' AS score,
                COALESCE(w.statut,'A_FAIRE') AS statut
            FROM workflow_cabinet_v3 w
            LEFT JOIN clients_v3 c
                ON c.id = w.client_id
            ORDER BY w.id DESC
            LIMIT 20
        """)).mappings().all()

        taches_rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale,'Client non identifié') AS client,
                COALESCE(t.titre,'Tâche cabinet') AS titre
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c
                ON c.id = t.client_id
            WHERE UPPER(COALESCE(t.priorite,'')) IN
            ('CRITIQUE','HAUTE','URGENT')
            ORDER BY t.id DESC
            LIMIT 10
        """)).mappings().all()

    clients = int(stats["clients"] or 0)
    taches = int(stats["taches"] or 0)
    workflow = int(stats["workflow"] or 0)
    pieces = int(stats["pieces"] or 0)

    score = max(0, 100 - (taches * 2) - (workflow))

    kpis = {
        "dossiers_actifs": clients,
        "alertes_bloquantes": taches,
        "retards": workflow,
        "prets_visa": max(0, clients - pieces),
        "prets_cloture": max(0, clients - taches),
        "score_global": score
    }

    dossiers = [
        [
            r["client"],
            r["etape"],
            r["responsable"],
            r["risque"],
            r["score"],
            r["statut"]
        ]
        for r in workflow_rows
    ]

    alertes = [
        [
            "Bloquant",
            r["client"],
            r["titre"]
        ]
        for r in taches_rows
    ]

    charge = [
        [
            "Collaborateurs",
            clients,
            taches,
            "En charge"
        ],
        [
            "Chefs de mission",
            clients,
            workflow,
            "Supervision"
        ],
        [
            "Expert-comptable",
            max(1, clients),
            pieces,
            "Visa"
        ]
    ]

    return kpis, dossiers, alertes, charge
