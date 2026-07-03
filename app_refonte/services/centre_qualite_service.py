from sqlalchemy import text

from database import engine


def _statut_controle(total, anomalies):
    if anomalies > 0:
        return "Bloquant"
    if total == 0:
        return "Attention"
    return "OK"


def _niveau_risque(anomalies):
    if anomalies >= 3:
        return "Élevé"
    if anomalies > 0:
        return "Moyen"
    return "Faible"


def charger_centre_qualite():
    with engine.connect() as conn:
        stats = conn.execute(text("""
            WITH clients AS (
                SELECT COUNT(*) AS total FROM clients_v3
            ),
            taches AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                        AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS bloquantes
                FROM taches_cabinet_v3
            ),
            pieces AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS anomalies
                FROM pieces_v3
            ),
            rappro AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('VALIDE', 'VALIDEE', 'OK', 'RAPPROCHE')
                    ) AS anomalies
                FROM rapprochements_bancaires_v3
            ),
            visas AS (
                SELECT
                    COUNT(DISTINCT societe_id) FILTER (WHERE valide IS TRUE) AS dossiers_avec_visa,
                    COUNT(*) FILTER (WHERE valide IS TRUE) AS visas_valides
                FROM cabinet_visas
            ),
            workflow AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS ouverts
                FROM workflow_cabinet_v3
            )
            SELECT
                clients.total AS dossiers_controles,
                taches.total AS taches_total,
                taches.bloquantes AS taches_bloquantes,
                pieces.total AS pieces_total,
                pieces.anomalies AS pieces_anomalies,
                rappro.total AS rappro_total,
                rappro.anomalies AS rappro_anomalies,
                visas.dossiers_avec_visa AS prets_visa,
                visas.visas_valides AS visas_valides,
                workflow.total AS workflow_total,
                workflow.ouverts AS workflow_ouverts
            FROM clients, taches, pieces, rappro, visas, workflow
        """)).mappings().first()

    dossiers_controles = int(stats["dossiers_controles"] or 0)

    taches_total = int(stats["taches_total"] or 0)
    taches_bloquantes = int(stats["taches_bloquantes"] or 0)

    pieces_total = int(stats["pieces_total"] or 0)
    pieces_anomalies = int(stats["pieces_anomalies"] or 0)

    rappro_total = int(stats["rappro_total"] or 0)
    rappro_anomalies = int(stats["rappro_anomalies"] or 0)

    prets_visa = int(stats["prets_visa"] or 0)
    visas_valides = int(stats["visas_valides"] or 0)

    workflow_total = int(stats["workflow_total"] or 0)
    workflow_ouverts = int(stats["workflow_ouverts"] or 0)

    points_bloquants = taches_bloquantes + pieces_anomalies + rappro_anomalies
    alertes_qualite = points_bloquants + workflow_ouverts

    total_points = taches_total + pieces_total + rappro_total + workflow_total + max(dossiers_controles * 3, 1)
    anomalies = alertes_qualite + max((dossiers_controles * 3) - visas_valides, 0)
    score_global = max(0, min(100, round(((total_points - anomalies) / total_points) * 100))) if total_points else 100

    risques = [
        [
            "GED",
            "Pièces justificatives non validées",
            _niveau_risque(pieces_anomalies),
            f"{pieces_anomalies} pièce(s) à contrôler sur {pieces_total}",
        ],
        [
            "Révision",
            "Tâches critiques non terminées",
            _niveau_risque(taches_bloquantes),
            f"{taches_bloquantes} tâche(s) bloquante(s) sur {taches_total}",
        ],
        [
            "Workflow cabinet",
            "Étapes cabinet encore ouvertes",
            _niveau_risque(workflow_ouverts),
            f"{workflow_ouverts} étape(s) ouverte(s) sur {workflow_total}",
        ],
        [
            "Banque",
            "Rapprochements bancaires non validés",
            _niveau_risque(rappro_anomalies),
            f"{rappro_anomalies} écart(s) sur {rappro_total}",
        ],
        [
            "Visa EC",
            "Dossiers sans chaîne complète de visa",
            _niveau_risque(max((dossiers_controles * 3) - visas_valides, 0)),
            f"{visas_valides} visa(s) validé(s) pour {dossiers_controles} dossier(s)",
        ],
    ]

    controles = [
        [
            "GED Cabinet",
            "Validation documentaire",
            _statut_controle(pieces_total, pieces_anomalies),
            f"{pieces_total - pieces_anomalies} / {pieces_total} pièce(s) validée(s)",
        ],
        [
            "Référentiel révision",
            "Tâches critiques et contrôles ouverts",
            _statut_controle(taches_total, taches_bloquantes),
            f"{taches_bloquantes} point(s) bloquant(s)",
        ],
        [
            "Workflow cabinet",
            "Avancement des étapes de production",
            _statut_controle(workflow_total, workflow_ouverts),
            f"{workflow_total - workflow_ouverts} / {workflow_total} étape(s) terminée(s)",
        ],
        [
            "Banque",
            "Contrôle des rapprochements",
            _statut_controle(rappro_total, rappro_anomalies),
            f"{rappro_total - rappro_anomalies} / {rappro_total} rapprochement(s) validé(s)",
        ],
        [
            "Visa Expert",
            "Autorisation de clôture",
            "OK" if prets_visa > 0 and points_bloquants == 0 else "Bloquant",
            f"{prets_visa} dossier(s) avec visa, {points_bloquants} blocage(s)",
        ],
    ]

    kpis = {
        "score_global": score_global,
        "dossiers_controles": dossiers_controles,
        "points_bloquants": points_bloquants,
        "alertes_qualite": alertes_qualite,
        "prets_visa": prets_visa,
    }

    return kpis, risques, controles
