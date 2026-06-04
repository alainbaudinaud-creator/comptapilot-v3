def charger_referentiel_revision():
    kpis = {
        "cycles": 8,
        "controles_obligatoires": 42,
        "controles_realises": 31,
        "points_bloquants": 4,
        "score_revision": 86,
    }

    cycles = [
        ["Achats", "Risque moyen", 8, 6, "À compléter"],
        ["Ventes", "Risque faible", 7, 7, "Validé"],
        ["Banque", "Risque élevé", 6, 4, "Bloquant"],
        ["Immobilisations", "Risque moyen", 5, 3, "À contrôler"],
        ["Social", "Risque faible", 4, 4, "Validé"],
        ["Fiscal", "Risque élevé", 6, 3, "Bloquant"],
        ["Capitaux propres", "Risque moyen", 3, 2, "À valider"],
        ["Trésorerie", "Risque faible", 3, 2, "À compléter"],
    ]

    controles = [
        ["Achats", "Factures fournisseurs rapprochées avec les écritures", "Réalisé", "Collaborateur"],
        ["Achats", "Contrôle TVA déductible", "Réalisé", "Collaborateur"],
        ["Banque", "Rapprochement bancaire complet", "Bloquant", "Chef de mission"],
        ["Banque", "Justificatifs des mouvements significatifs", "À faire", "Collaborateur"],
        ["Fiscal", "Cadrage TVA comptabilité / déclaration", "Bloquant", "Chef de mission"],
        ["Fiscal", "Contrôle cohérence liasse fiscale", "À faire", "Expert-comptable"],
        ["Immobilisations", "Cadrage tableau amortissements / comptabilité", "À faire", "Collaborateur"],
        ["Ventes", "Contrôle chiffre d'affaires mensuel", "Réalisé", "Chef de mission"],
    ]

    return kpis, cycles, controles
