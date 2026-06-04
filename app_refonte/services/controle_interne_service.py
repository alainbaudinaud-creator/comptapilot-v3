from sqlalchemy import text

from database import engine


def _niveau(nb):
    if nb >= 3:
        return "Élevé"
    if nb > 0:
        return "Moyen"
    return "Faible"


def _statut_actif(total, anomalies):
    if total == 0:
        return "À planifier"
    if anomalies > 0:
        return "Actif"
    return "Actif"


def charger_controle_interne():
    with engine.connect() as conn:
        stats = conn.execute(text("""
            WITH taches AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                        AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS critiques
                FROM taches_cabinet_v3
            ),
            pieces AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS non_validees
                FROM pieces_v3
            ),
            rappro AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('VALIDE', 'VALIDEE', 'OK', 'RAPPROCHE')
                    ) AS ecarts
                FROM rapprochements_bancaires_v3
            ),
            visas AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE valide IS TRUE) AS valides
                FROM cabinet_visas
            ),
            workflow AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS ouverts
                FROM workflow_cabinet_v3
            ),
            notifications AS (
                SELECT
                    COUNT(*) AS total
                FROM notifications_cabinet_v3
            )
            SELECT
                taches.total AS taches_total,
                taches.critiques AS taches_critiques,
                pieces.total AS pieces_total,
                pieces.non_validees AS pieces_non_validees,
                rappro.total AS rappro_total,
                rappro.ecarts AS rappro_ecarts,
                visas.total AS visas_total,
                visas.valides AS visas_valides,
                workflow.total AS workflow_total,
                workflow.ouverts AS workflow_ouverts,
                notifications.total AS audits_traces
            FROM taches, pieces, rappro, visas, workflow, notifications
        """)).mappings().first()

        pistes_rows = conn.execute(text("""
            SELECT
                created_at::date AS date_action,
                COALESCE(module, 'Workflow') AS module,
                COALESCE(etape, commentaire, 'Action cabinet') AS action,
                COALESCE(responsable, 'Système') AS utilisateur
            FROM workflow_cabinet_v3
            ORDER BY created_at DESC, id DESC
            LIMIT 8
        """)).mappings().all()

    taches_total = int(stats["taches_total"] or 0)
    taches_critiques = int(stats["taches_critiques"] or 0)
    pieces_total = int(stats["pieces_total"] or 0)
    pieces_non_validees = int(stats["pieces_non_validees"] or 0)
    rappro_total = int(stats["rappro_total"] or 0)
    rappro_ecarts = int(stats["rappro_ecarts"] or 0)
    visas_total = int(stats["visas_total"] or 0)
    visas_valides = int(stats["visas_valides"] or 0)
    workflow_total = int(stats["workflow_total"] or 0)
    workflow_ouverts = int(stats["workflow_ouverts"] or 0)
    audits_traces = int(stats["audits_traces"] or 0) + workflow_total + visas_total

    risques_identifies = taches_critiques + pieces_non_validees + rappro_ecarts + workflow_ouverts
    controles_actifs = taches_total + pieces_total + rappro_total + visas_total + workflow_total
    alertes_critiques = taches_critiques + pieces_non_validees + rappro_ecarts

    score_controle = 100 if controles_actifs == 0 else max(
        0,
        min(100, round(((controles_actifs - risques_identifies) / controles_actifs) * 100))
    )

    risques = [
        [
            "Séparation des tâches",
            "Workflow cabinet non finalisé",
            _niveau(workflow_ouverts),
            f"{workflow_ouverts} étape(s) ouverte(s) sur {workflow_total}",
        ],
        [
            "GED",
            "Pièces justificatives non validées",
            _niveau(pieces_non_validees),
            f"{pieces_non_validees} pièce(s) à valider sur {pieces_total}",
        ],
        [
            "Trésorerie",
            "Rapprochements bancaires non validés",
            _niveau(rappro_ecarts),
            f"{rappro_ecarts} écart(s) sur {rappro_total}",
        ],
        [
            "Révision",
            "Tâches critiques non terminées",
            _niveau(taches_critiques),
            f"{taches_critiques} tâche(s) critique(s) ouverte(s)",
        ],
        [
            "Visa expert-comptable",
            "Chaîne de visa incomplète",
            _niveau(max(visas_total - visas_valides, 0)),
            f"{visas_valides} visa(s) validé(s) sur {visas_total}",
        ],
    ]

    controles = [
        ["Permanent", "Contrôle workflow cabinet", _statut_actif(workflow_total, workflow_ouverts), "Quotidien"],
        ["Permanent", "Contrôle pièces GED obligatoires", _statut_actif(pieces_total, pieces_non_validees), "Quotidien"],
        ["Permanent", "Contrôle tâches critiques de révision", _statut_actif(taches_total, taches_critiques), "Quotidien"],
        ["Périodique", "Contrôle rapprochements bancaires", _statut_actif(rappro_total, rappro_ecarts), "Hebdomadaire"],
        ["Audit", "Traçabilité visa expert-comptable", _statut_actif(visas_total, max(visas_total - visas_valides, 0)), "À chaque clôture"],
    ]

    pistes = []
    for row in pistes_rows:
        pistes.append([
            str(row["date_action"]),
            row["module"],
            row["action"],
            row["utilisateur"],
        ])

    if not pistes:
        pistes = [["-", "Système", "Aucune piste d'audit workflow disponible", "Système"]]

    kpis = {
        "score_controle": score_controle,
        "risques_identifies": risques_identifies,
        "controles_actifs": controles_actifs,
        "alertes_critiques": alertes_critiques,
        "audits_traces": audits_traces,
    }

    return kpis, risques, controles, pistes
