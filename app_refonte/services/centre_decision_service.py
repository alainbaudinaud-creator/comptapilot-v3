def charger_centre_decision():
    kpis = {
        "decisions_urgentes": 8,
        "arbitrages_ec": 5,
        "dossiers_prioritaires": 12,
        "alertes_globales": 21,
        "score_cabinet": 86,
    }

    decisions = [
        ["IFG Holding", "NO GO clôture", "Expert-comptable", "Critique", "Arbitrer blocage LCB-FT"],
        ["SAS Lumière", "Pièces GED manquantes", "Chef mission", "Critique", "Demander justificatifs client"],
        ["Orange SA", "Visa EC final", "Expert-comptable", "Haute", "Valider clôture sous réserve"],
        ["SCI Patrimoine", "Cadrage fiscal", "Chef mission", "Haute", "Arbitrer TVA avant comité"],
        ["Cabinet Demo", "Clôture prête", "Expert-comptable", "Normale", "Autoriser clôture"],
    ]

    alertes = [
        ["Qualité", "5 points bloquants cabinet"],
        ["Conformité", "4 alertes LCB-FT"],
        ["Révision", "11 contrôles obligatoires non finalisés"],
        ["GED", "7 pièces manquantes avant clôture"],
        ["Visa", "4 dossiers en attente expert-comptable"],
    ]

    priorites = [
        ["1", "Lever les blocages critiques", "Aujourd'hui"],
        ["2", "Valider les dossiers prêts au visa", "Aujourd'hui"],
        ["3", "Arbitrer les dossiers fiscaux sensibles", "48h"],
        ["4", "Relancer les pièces GED manquantes", "48h"],
    ]

    return kpis, decisions, alertes, priorites
