def charger_gestion_risques():
    kpis = {
        "risques_total": 24,
        "risques_critiques": 5,
        "risques_maitrises": 14,
        "plans_actions": 11,
        "score_global": 82,
    }

    risques = [
        ["Fiscal", "TVA incohérente", "Critique", "Élevé", "Chef de mission", "Ouvert"],
        ["LCB-FT", "Bénéficiaire effectif absent", "Critique", "Élevé", "Responsable conformité", "Ouvert"],
        ["GED", "Pièces justificatives manquantes", "Élevé", "Moyen", "Collaborateur", "En cours"],
        ["Révision", "Contrôles obligatoires incomplets", "Élevé", "Moyen", "Chef de mission", "En cours"],
        ["Visa EC", "Validation finale absente", "Moyen", "Faible", "Expert-comptable", "À traiter"],
        ["Qualité", "Dossier hors procédure", "Moyen", "Faible", "Responsable qualité", "Surveillé"],
    ]

    plans = [
        ["TVA", "Revue complète du cadrage TVA", "Chef de mission", "Haute"],
        ["LCB-FT", "Collecte documents bénéficiaires", "Conformité", "Critique"],
        ["GED", "Compléter pièces manquantes", "Collaborateur", "Haute"],
        ["Qualité", "Audit interne ciblé", "Responsable qualité", "Normale"],
    ]

    return kpis, risques, plans
