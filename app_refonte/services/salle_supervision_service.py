def charger_salle_supervision():
    kpis = {
        "dossiers_actifs": 32,
        "alertes_bloquantes": 7,
        "retards": 5,
        "prets_visa": 9,
        "prets_cloture": 6,
        "score_global": 88,
    }

    dossiers = [
        ["Orange SA", "Révision", "Chef mission", "Risque moyen", "92%", "À viser"],
        ["IFG Holding", "Conformité", "Responsable conformité", "Risque élevé", "71%", "Bloqué"],
        ["Cabinet Demo", "Clôture", "Expert-comptable", "Risque faible", "96%", "Prêt clôture"],
        ["SAS Lumière", "GED", "Collaborateur", "Risque élevé", "68%", "Pièces manquantes"],
        ["SCI Patrimoine", "Fiscal", "Chef mission", "Risque moyen", "89%", "À contrôler"],
    ]

    alertes = [
        ["Bloquant", "IFG Holding", "LCB-FT incomplet"],
        ["Bloquant", "SAS Lumière", "Pièces GED manquantes"],
        ["Haute", "Orange SA", "Visa EC en attente"],
        ["Haute", "SCI Patrimoine", "Cadrage fiscal à revoir"],
    ]

    charge = [
        ["Collaborateur A", 8, 3, "Charge normale"],
        ["Collaborateur B", 11, 5, "Surcharge"],
        ["Chef mission", 14, 6, "Prioritaire"],
        ["Expert-comptable", 9, 4, "Visa en attente"],
    ]

    return kpis, dossiers, alertes, charge
