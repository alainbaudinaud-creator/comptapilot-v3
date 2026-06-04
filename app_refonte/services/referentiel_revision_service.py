from sqlalchemy import text

from database import engine


def _statut_affiche(statut, bloquants, total, realises):
    statut = (statut or "").upper()
    if bloquants > 0:
        return "Bloquant"
    if total == 0:
        return "À cadrer"
    if realises >= total:
        return "Validé"
    if realises == 0:
        return "À faire"
    return "À compléter"


def _risque_affiche(priorite_haute, bloquants):
    if bloquants > 0 or priorite_haute >= 2:
        return "Risque élevé"
    if priorite_haute == 1:
        return "Risque moyen"
    return "Risque faible"


def charger_referentiel_revision():
    with engine.connect() as conn:
        workflow_rows = conn.execute(text("""
            SELECT
                COALESCE(module, 'REVISION') AS cycle,
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut, '')) IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')) AS realises,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut, '')) IN ('BLOQUANT', 'A_BLOQUER', 'ERREUR')) AS bloquants
            FROM workflow_cabinet_v3
            GROUP BY COALESCE(module, 'REVISION')
            ORDER BY COALESCE(module, 'REVISION')
        """)).mappings().all()

        taches_rows = conn.execute(text("""
            SELECT
                COALESCE(t.titre, 'Contrôle de révision') AS titre,
                COALESCE(t.statut, 'A_FAIRE') AS statut,
                COALESCE(t.priorite, 'NORMALE') AS priorite,
                COALESCE(c.raison_sociale, 'Client non identifié') AS client
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c ON c.id = t.client_id
            ORDER BY
                CASE UPPER(COALESCE(t.priorite, ''))
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'URGENT' THEN 3
                    ELSE 4
                END,
                t.echeance NULLS LAST,
                t.id DESC
            LIMIT 12
        """)).mappings().all()

        taches_stats = conn.execute(text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut, '')) IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')) AS realises,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')) AS prioritaires,
                COUNT(*) FILTER (
                    WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                    AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                ) AS bloquants
            FROM taches_cabinet_v3
        """)).mappings().first()

        pieces_stats = conn.execute(text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE statut_validation = 'VALIDEE') AS validees,
                COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS a_controler
            FROM pieces_v3
        """)).mappings().first()

        rapprochements_stats = conn.execute(text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut, '')) IN ('VALIDE', 'VALIDEE', 'OK', 'RAPPROCHE')) AS valides,
                COUNT(*) FILTER (WHERE UPPER(COALESCE(statut, '')) NOT IN ('VALIDE', 'VALIDEE', 'OK', 'RAPPROCHE')) AS ecarts
            FROM rapprochements_bancaires_v3
        """)).mappings().first()

        visas_stats = conn.execute(text("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE valide IS TRUE) AS valides,
                COUNT(*) FILTER (WHERE valide IS NOT TRUE) AS attente
            FROM cabinet_visas
        """)).mappings().first()

    controles_obligatoires = int(taches_stats["total"] or 0)
    controles_realises = int(taches_stats["realises"] or 0)
    points_bloquants = int(taches_stats["bloquants"] or 0)

    pieces_total = int(pieces_stats["total"] or 0)
    pieces_validees = int(pieces_stats["validees"] or 0)
    pieces_a_controler = int(pieces_stats["a_controler"] or 0)

    rappro_total = int(rapprochements_stats["total"] or 0)
    rappro_valides = int(rapprochements_stats["valides"] or 0)
    rappro_ecarts = int(rapprochements_stats["ecarts"] or 0)

    visas_total = int(visas_stats["total"] or 0)
    visas_valides = int(visas_stats["valides"] or 0)
    visas_attente = int(visas_stats["attente"] or 0)

    total_controles = controles_obligatoires + pieces_total + rappro_total + visas_total
    total_realises = controles_realises + pieces_validees + rappro_valides + visas_valides
    total_bloquants = points_bloquants + pieces_a_controler + rappro_ecarts + visas_attente

    score_revision = 100 if total_controles == 0 else max(0, min(100, round((total_realises / total_controles) * 100)))

    cycles = []
    for row in workflow_rows:
        total = int(row["total"] or 0)
        realises = int(row["realises"] or 0)
        bloquants = int(row["bloquants"] or 0)
        cycles.append([
            row["cycle"],
            _risque_affiche(0, bloquants),
            total,
            realises,
            _statut_affiche(None, bloquants, total, realises),
        ])

    cycles.extend([
        ["GED / pièces justificatives", _risque_affiche(0, pieces_a_controler), pieces_total, pieces_validees, _statut_affiche(None, pieces_a_controler, pieces_total, pieces_validees)],
        ["Banque / rapprochements", _risque_affiche(0, rappro_ecarts), rappro_total, rappro_valides, _statut_affiche(None, rappro_ecarts, rappro_total, rappro_valides)],
        ["Visa expert-comptable", _risque_affiche(0, visas_attente), visas_total, visas_valides, _statut_affiche(None, visas_attente, visas_total, visas_valides)],
    ])

    if not cycles:
        cycles = [["Révision", "Risque moyen", total_controles, total_realises, _statut_affiche(None, total_bloquants, total_controles, total_realises)]]

    controles = []
    for row in taches_rows:
        statut = row["statut"]
        priorite = (row["priorite"] or "").upper()
        statut_controle = "Bloquant" if priorite in ("CRITIQUE", "HAUTE", "URGENT") and str(statut).upper() not in ("TERMINE", "TERMINEE", "VALIDEE", "VALIDÉE", "OK") else statut
        controles.append([
            row["client"],
            row["titre"],
            statut_controle,
            "Chef de mission" if priorite in ("CRITIQUE", "HAUTE", "URGENT") else "Collaborateur",
        ])

    if pieces_a_controler:
        controles.append(["GED", "Pièces justificatives non validées", "Bloquant", "Collaborateur"])
    if rappro_ecarts:
        controles.append(["Banque", "Rapprochements bancaires non validés", "Bloquant", "Chef de mission"])
    if visas_attente:
        controles.append(["Visa EC", "Visas expert-comptable en attente", "À faire", "Expert-comptable"])

    kpis = {
        "cycles": len(cycles),
        "controles_obligatoires": total_controles,
        "controles_realises": total_realises,
        "points_bloquants": total_bloquants,
        "score_revision": score_revision,
    }

    return kpis, cycles, controles
