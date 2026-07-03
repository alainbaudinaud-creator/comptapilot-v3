from collections import Counter

from sqlalchemy import text

from database import engine


def _decision(points_bloquants, pieces_a_valider, workflow_ouverts, nb_visas):
    if points_bloquants >= 2 or pieces_a_valider > 0:
        return "NO GO"
    if points_bloquants == 1 or workflow_ouverts >= 2:
        return "À arbitrer"
    if nb_visas >= 3:
        return "GO"
    if nb_visas >= 1:
        return "GO sous réserve"
    return "À arbitrer"


def _etat(decision):
    if decision == "GO":
        return "Prêt clôture"
    if decision == "GO sous réserve":
        return "Visa final à compléter"
    if decision == "À arbitrer":
        return "Arbitrage EC"
    return "Bloqué"


def charger_comite_cloture():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            WITH taches AS (
                SELECT
                    client_id,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                        AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS points_bloquants,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS taches_ouvertes
                FROM taches_cabinet_v3
                GROUP BY client_id
            ),
            pieces AS (
                SELECT
                    client_id,
                    COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS pieces_a_valider
                FROM pieces_v3
                GROUP BY client_id
            ),
            workflow AS (
                SELECT
                    client_id,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS workflow_ouverts,
                    COUNT(*) AS workflow_total
                FROM workflow_cabinet_v3
                GROUP BY client_id
            ),
            visas AS (
                SELECT
                    societe_id,
                    COUNT(DISTINCT type_visa) FILTER (WHERE valide IS TRUE) AS nb_visas
                FROM cabinet_visas
                GROUP BY societe_id
            )
            SELECT
                c.id,
                c.raison_sociale AS dossier,
                COALESCE(t.points_bloquants, 0) AS points_bloquants,
                COALESCE(t.taches_ouvertes, 0) AS taches_ouvertes,
                COALESCE(p.pieces_a_valider, 0) AS pieces_a_valider,
                COALESCE(w.workflow_ouverts, 0) AS workflow_ouverts,
                COALESCE(w.workflow_total, 0) AS workflow_total,
                COALESCE(v.nb_visas, 0) AS nb_visas
            FROM clients_v3 c
            LEFT JOIN taches t ON t.client_id = c.id
            LEFT JOIN pieces p ON p.client_id = c.id
            LEFT JOIN workflow w ON w.client_id = c.id
            LEFT JOIN visas v ON v.societe_id = c.id
            ORDER BY c.id ASC
        """)).mappings().all()

    dossiers = []
    blocages = []
    decisions_counter = Counter()

    for row in rows:
        points_bloquants = int(row["points_bloquants"] or 0)
        pieces_a_valider = int(row["pieces_a_valider"] or 0)
        workflow_ouverts = int(row["workflow_ouverts"] or 0)
        workflow_total = int(row["workflow_total"] or 0)
        nb_visas = int(row["nb_visas"] or 0)

        decision = _decision(points_bloquants, pieces_a_valider, workflow_ouverts, nb_visas)
        decisions_counter[decision] += 1

        preparation = (
            "Feuille maîtresse OK"
            if workflow_total > 0 and workflow_ouverts == 0
            else f"{workflow_ouverts} étape(s) workflow ouverte(s)"
        )

        validation = (
            "Visa EC validé"
            if nb_visas >= 3
            else "Chef mission validé" if nb_visas >= 2
            else "Validation incomplète"
        )

        dossiers.append([
            row["dossier"],
            preparation,
            validation,
            _etat(decision),
            decision,
        ])

        if points_bloquants:
            blocages.append([
                "Révision / Qualité",
                row["dossier"],
                f"{points_bloquants} tâche(s) critique(s) non terminée(s)",
                "Critique" if points_bloquants >= 2 else "Élevé",
            ])

        if pieces_a_valider:
            blocages.append([
                "GED",
                row["dossier"],
                f"{pieces_a_valider} pièce(s) justificative(s) à valider",
                "Critique",
            ])

        if workflow_ouverts:
            blocages.append([
                "Workflow",
                row["dossier"],
                f"{workflow_ouverts} étape(s) de clôture/production ouverte(s)",
                "Élevé" if workflow_ouverts >= 2 else "Moyen",
            ])

        if nb_visas < 3:
            blocages.append([
                "Visa EC",
                row["dossier"],
                f"{3 - nb_visas} visa(s) restant(s)",
                "Moyen",
            ])

    dossiers_comite = len(rows)
    go_cloture = decisions_counter["GO"]
    no_go = decisions_counter["NO GO"]
    a_arbitrer = decisions_counter["À arbitrer"]
    go_sous_reserve = decisions_counter["GO sous réserve"]

    score_cloture = 100 if dossiers_comite == 0 else max(
        0,
        min(100, round(((go_cloture + go_sous_reserve * 0.6 + a_arbitrer * 0.3) / dossiers_comite) * 100))
    )

    decisions = [
        ["GO", "Dossier clôturable immédiatement", go_cloture],
        ["GO sous réserve", "Clôturable après visa final ou contrôle complémentaire", go_sous_reserve],
        ["À arbitrer", "Décision expert-comptable requise", a_arbitrer],
        ["NO GO", "Blocage clôture", no_go],
    ]

    kpis = {
        "dossiers_comite": dossiers_comite,
        "go_cloture": go_cloture,
        "no_go": no_go,
        "a_arbitrer": a_arbitrer,
        "score_cloture": score_cloture,
    }

    return kpis, dossiers, blocages, decisions
