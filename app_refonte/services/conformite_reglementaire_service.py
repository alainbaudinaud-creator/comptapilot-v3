from sqlalchemy import text

from database import engine


def _niveau(nb):
    if nb >= 3:
        return "Élevé"
    if nb > 0:
        return "Moyen"
    return "Faible"


def _statut_attention(anomalies):
    return "OK" if anomalies == 0 else "Attention"


def charger_conformite_reglementaire():
    with engine.connect() as conn:
        stats = conn.execute(text("""
            WITH clients AS (
                SELECT COUNT(*) AS total FROM clients_v3
            ),
            pieces AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE statut_validation = 'VALIDEE') AS validees,
                    COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS anomalies
                FROM pieces_v3
            ),
            taches AS (
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(priorite, '')) IN ('CRITIQUE', 'HAUTE', 'URGENT')
                        AND UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS critiques,
                    COUNT(*) FILTER (
                        WHERE UPPER(COALESCE(statut, '')) NOT IN ('TERMINE', 'TERMINEE', 'VALIDEE', 'VALIDÉE', 'OK')
                    ) AS ouvertes
                FROM taches_cabinet_v3
            ),
            visas AS (
                SELECT
                    COUNT(*) FILTER (WHERE valide IS TRUE) AS valides,
                    COUNT(DISTINCT societe_id) FILTER (WHERE valide IS TRUE) AS dossiers_avec_visa
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
            tele AS (
                SELECT COUNT(*) AS total FROM teletransmissions_fiscales_v3
            )
            SELECT
                clients.total AS clients_total,
                pieces.total AS pieces_total,
                pieces.validees AS pieces_validees,
                pieces.anomalies AS pieces_anomalies,
                taches.total AS taches_total,
                taches.critiques AS taches_critiques,
                taches.ouvertes AS taches_ouvertes,
                visas.valides AS visas_valides,
                visas.dossiers_avec_visa AS dossiers_avec_visa,
                workflow.total AS workflow_total,
                workflow.ouverts AS workflow_ouverts,
                tele.total AS tele_total
            FROM clients, pieces, taches, visas, workflow, tele
        """)).mappings().first()

    clients_total = int(stats["clients_total"] or 0)
    pieces_total = int(stats["pieces_total"] or 0)
    pieces_validees = int(stats["pieces_validees"] or 0)
    pieces_anomalies = int(stats["pieces_anomalies"] or 0)
    taches_total = int(stats["taches_total"] or 0)
    taches_critiques = int(stats["taches_critiques"] or 0)
    taches_ouvertes = int(stats["taches_ouvertes"] or 0)
    visas_valides = int(stats["visas_valides"] or 0)
    dossiers_avec_visa = int(stats["dossiers_avec_visa"] or 0)
    workflow_total = int(stats["workflow_total"] or 0)
    workflow_ouverts = int(stats["workflow_ouverts"] or 0)
    tele_total = int(stats["tele_total"] or 0)

    lettres_mission = pieces_validees
    dossiers_rgpd = clients_total
    alertes_lcbft = taches_critiques + pieces_anomalies
    revues_annuelles = max(0, clients_total - workflow_ouverts)

    points_total = max(1, clients_total + pieces_total + taches_total + workflow_total + max(clients_total * 3, 1))
    anomalies = pieces_anomalies + taches_critiques + workflow_ouverts + max((clients_total * 3) - visas_valides, 0)
    score_conformite = max(0, min(100, round(((points_total - anomalies) / points_total) * 100)))

    obligations = [
        ["RGPD", "Registre traitements clients", "À jour" if clients_total > 0 else "À compléter", f"{clients_total} dossier(s) client(s) référencé(s)"],
        ["LCB-FT", "Contrôle entrée en relation et risques clients", _statut_attention(alertes_lcbft), f"{alertes_lcbft} alerte(s) issue(s) tâches/GED"],
        ["Acceptation client", "Workflow d'acceptation et production cabinet", _statut_attention(workflow_ouverts), f"{workflow_total - workflow_ouverts} / {workflow_total} étape(s) terminée(s)"],
        ["Lettre de mission", "Lettre ou justificatif archivé GED", _statut_attention(max(pieces_total - lettres_mission, 0)), f"{lettres_mission} pièce(s) validée(s) sur {pieces_total}"],
        ["Indépendance", "Visa et revue expert-comptable", _statut_attention(max((clients_total * 3) - visas_valides, 0)), f"{visas_valides} visa(s) validé(s)"],
        ["Ordre EC", "Dossier qualité cabinet et télétransmissions", "OK" if tele_total >= 0 else "À compléter", f"{tele_total} télétransmission(s) suivie(s)"],
    ]

    risques = [
        ["LCB-FT", "Tâches critiques ou dossiers incomplets", _niveau(alertes_lcbft), f"{alertes_lcbft} alerte(s) conformité"],
        ["RGPD", "Dossiers client sans revue annuelle complète", _niveau(max(clients_total - revues_annuelles, 0)), f"{revues_annuelles} revue(s) annuelle(s) estimée(s)"],
        ["Mission", "Pièces ou lettres de mission non validées", _niveau(pieces_anomalies), f"{pieces_anomalies} pièce(s) à valider"],
        ["Indépendance", "Chaîne de visa expert-comptable incomplète", _niveau(max((clients_total * 3) - visas_valides, 0)), f"{dossiers_avec_visa} dossier(s) avec visa"],
    ]

    actions = [
        ["Traiter les tâches critiques conformité", "Chef de mission", "À faire" if taches_critiques else "OK"],
        ["Valider les pièces GED restantes", "Collaborateur", "À faire" if pieces_anomalies else "OK"],
        ["Finaliser les visas expert-comptable", "Expert-comptable", "À faire" if visas_valides < clients_total * 3 else "OK"],
        ["Clôturer les étapes workflow ouvertes", "Responsables dossiers", "En cours" if workflow_ouverts else "OK"],
    ]

    kpis = {
        "score_conformite": score_conformite,
        "dossiers_rgpd": dossiers_rgpd,
        "alertes_lcbft": alertes_lcbft,
        "lettres_mission": lettres_mission,
        "revues_annuelles": revues_annuelles,
    }

    return kpis, obligations, risques, actions
