from sqlalchemy import text

from database import engine


VISAS_ATTENDUS = ["COLLABORATEUR", "CHEF_MISSION", "EXPERT_COMPTABLE"]


def _score_dossier(nb_visas, nb_attendus, bloque=False):
    if bloque:
        return "45%"
    if nb_attendus == 0:
        return "100%"
    return f"{round((nb_visas / nb_attendus) * 100)}%"


def _decision(nb_visas, bloque=False):
    if bloque:
        return "Bloqué"
    if nb_visas >= 3:
        return "Visa final"
    if nb_visas == 2:
        return "À viser"
    if nb_visas == 1:
        return "À valider"
    return "À préparer"


def _niveau_actuel(nb_visas):
    if nb_visas >= 3:
        return "Expert-comptable"
    if nb_visas == 2:
        return "Expert-comptable"
    if nb_visas == 1:
        return "Chef de mission"
    return "Collaborateur"


def charger_visa_expert():
    with engine.connect() as conn:
        dossiers_rows = conn.execute(text("""
            WITH visas AS (
                SELECT
                    societe_id,
                    exercice,
                    COUNT(DISTINCT type_visa) FILTER (WHERE valide IS TRUE) AS nb_visas,
                    COUNT(*) FILTER (WHERE valide IS TRUE AND type_visa = 'COLLABORATEUR') AS visa_collab,
                    COUNT(*) FILTER (WHERE valide IS TRUE AND type_visa = 'CHEF_MISSION') AS visa_chef,
                    COUNT(*) FILTER (WHERE valide IS TRUE AND type_visa = 'EXPERT_COMPTABLE') AS visa_ec
                FROM cabinet_visas
                GROUP BY societe_id, exercice
            ),
            blocages AS (
                SELECT
                    client_id,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                        AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS points_bloquants
                FROM taches_cabinet_v3
                GROUP BY client_id
            ),
            pieces AS (
                SELECT
                    client_id,
                    COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS pieces_a_valider
                FROM pieces_v3
                GROUP BY client_id
            )
            SELECT
                c.id AS client_id,
                c.raison_sociale AS dossier,
                COALESCE(v.exercice, '2025') AS exercice,
                COALESCE(v.nb_visas, 0) AS nb_visas,
                COALESCE(v.visa_collab, 0) AS visa_collab,
                COALESCE(v.visa_chef, 0) AS visa_chef,
                COALESCE(v.visa_ec, 0) AS visa_ec,
                COALESCE(b.points_bloquants, 0) AS points_bloquants,
                COALESCE(p.pieces_a_valider, 0) AS pieces_a_valider
            FROM clients_v3 c
            LEFT JOIN visas v ON v.societe_id = c.id
            LEFT JOIN blocages b ON b.client_id = c.id
            LEFT JOIN pieces p ON p.client_id = c.id
            ORDER BY
                COALESCE(b.points_bloquants, 0) DESC,
                COALESCE(p.pieces_a_valider, 0) DESC,
                COALESCE(v.nb_visas, 0) ASC,
                c.id ASC
            LIMIT 12
        """)).mappings().all()

        stats = conn.execute(text("""
            WITH par_dossier AS (
                SELECT
                    c.id,
                    COUNT(DISTINCT cv.type_visa) FILTER (WHERE cv.valide IS TRUE) AS nb_visas
                FROM clients_v3 c
                LEFT JOIN cabinet_visas cv ON cv.societe_id = c.id
                GROUP BY c.id
            ),
            blocages AS (
                SELECT
                    client_id,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                        AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS points_bloquants
                FROM taches_cabinet_v3
                GROUP BY client_id
            )
            SELECT
                COUNT(*) FILTER (WHERE COALESCE(pd.nb_visas, 0) >= 2) AS dossiers_prets,
                COUNT(*) FILTER (WHERE COALESCE(pd.nb_visas, 0) = 1) AS a_valider_chef,
                COUNT(*) FILTER (WHERE COALESCE(pd.nb_visas, 0) = 2) AS a_visa_ec,
                COUNT(*) FILTER (WHERE COALESCE(b.points_bloquants, 0) > 0) AS bloques,
                COUNT(*) AS dossiers_total,
                SUM(COALESCE(pd.nb_visas, 0)) AS visas_valides
            FROM par_dossier pd
            LEFT JOIN blocages b ON b.client_id = pd.id
        """)).mappings().first()

    dossiers = []
    for row in dossiers_rows:
        nb_visas = int(row["nb_visas"] or 0)
        points_bloquants = int(row["points_bloquants"] or 0)
        pieces_a_valider = int(row["pieces_a_valider"] or 0)
        bloque = points_bloquants > 0 or pieces_a_valider > 0

        if bloque:
            etat_metier = f"{points_bloquants} point(s) bloquant(s), {pieces_a_valider} pièce(s) à valider"
        elif nb_visas >= 3:
            etat_metier = "Visa expert-comptable complet"
        elif nb_visas == 2:
            etat_metier = "Validation chef terminée"
        elif nb_visas == 1:
            etat_metier = "Préparation collaborateur validée"
        else:
            etat_metier = "Révision à finaliser"

        dossiers.append([
            row["dossier"],
            etat_metier,
            _niveau_actuel(nb_visas),
            _decision(nb_visas, bloque=bloque),
            _score_dossier(nb_visas, len(VISAS_ATTENDUS), bloque=bloque),
        ])

    dossiers_total = int(stats["dossiers_total"] or 0)
    visas_valides = int(stats["visas_valides"] or 0)
    max_visas = dossiers_total * len(VISAS_ATTENDUS)
    score_conformite = 100 if max_visas == 0 else round((visas_valides / max_visas) * 100)

    kpis = {
        "dossiers_prets": int(stats["dossiers_prets"] or 0),
        "a_valider_chef": int(stats["a_valider_chef"] or 0),
        "a_visa_ec": int(stats["a_visa_ec"] or 0),
        "bloques": int(stats["bloques"] or 0),
        "score_conformite": score_conformite,
    }

    validations = [
        ["Collaborateur", "Préparation dossier", "Réalisé" if visas_valides >= 1 else "À faire", "Visa collaborateur lu depuis cabinet_visas"],
        ["Chef de mission", "Revue qualité", "Réalisé" if kpis["a_visa_ec"] > 0 or kpis["dossiers_prets"] > 0 else "À faire", "Contrôle des dossiers avant visa EC"],
        ["Expert-comptable", "Visa final", "Réalisé" if score_conformite == 100 else "À faire", "Visa final issu des données cabinet_visas"],
        ["Système", "Autorisation clôture", "Bloquée" if kpis["bloques"] > 0 else "Autorisée", f"{kpis['bloques']} dossier(s) avec points bloquants"],
    ]

    return kpis, dossiers, validations
