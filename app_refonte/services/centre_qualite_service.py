def charger_centre_qualite():
    kpis = {
        "score_global": 89,
        "dossiers_controles": 14,
        "points_bloquants": 5,
        "alertes_qualite": 11,
        "prets_visa": 8,
    }

    risques = [
        ["GED", "Pièces justificatives manquantes", "Élevé", "3 dossiers concernés"],
        ["Révision", "Contrôles obligatoires incomplets", "Élevé", "Banque et Fiscal"],
        ["Clôture", "Feuille maîtresse non validée", "Moyen", "2 dossiers"],
        ["Fiscal", "Cadrage TVA à confirmer", "Moyen", "1 dossier"],
        ["Visa EC", "Validation chef de mission absente", "Élevé", "4 dossiers"],
    ]

    controles = [
        ["GED Cabinet", "Indexation documentaire", "OK", "184 documents indexés"],
        ["Référentiel révision", "Contrôles obligatoires", "Attention", "31 / 42 réalisés"],
        ["Justification comptes", "Comptes sensibles", "OK", "Justifications présentes"],
        ["Feuille maîtresse", "Synthèse clôture", "Attention", "2 validations manquantes"],
        ["Visa Expert", "Autorisation clôture", "Bloquant", "3 dossiers bloqués"],
    ]

    return kpis, risques, controles
