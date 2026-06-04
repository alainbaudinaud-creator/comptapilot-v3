def charger_controle_interne():
    kpis = {
        "score_controle": 87,
        "risques_identifies": 18,
        "controles_actifs": 34,
        "alertes_critiques": 3,
        "audits_traces": 126,
    }

    risques = [
        ["Séparation des tâches", "Validation et saisie par même utilisateur", "Élevé", "Action corrective requise"],
        ["GED", "Absence de justificatif sur écritures sensibles", "Élevé", "Blocage visa"],
        ["Trésorerie", "Paiements non rapprochés", "Moyen", "Contrôle hebdomadaire"],
        ["Fiscal", "Déclaration TVA sans cadrage validé", "Élevé", "Validation chef obligatoire"],
        ["Accès utilisateurs", "Droits administrateur trop larges", "Moyen", "Revue mensuelle"],
    ]

    controles = [
        ["Permanent", "Contrôle séparation saisie / validation", "Actif", "Mensuel"],
        ["Permanent", "Contrôle pièces GED obligatoires", "Actif", "Quotidien"],
        ["Périodique", "Revue droits utilisateurs", "À planifier", "Mensuel"],
        ["Périodique", "Contrôle cohérence TVA / balance", "Actif", "Trimestriel"],
        ["Audit", "Traçabilité visa expert-comptable", "Actif", "À chaque clôture"],
    ]

    pistes = [
        ["2026-06-04", "Visa EC", "Validation dossier Cabinet Demo", "Expert-comptable"],
        ["2026-06-04", "GED", "Pièce ajoutée sur cycle Banque", "Collaborateur"],
        ["2026-06-03", "Révision", "Contrôle fiscal marqué bloquant", "Chef de mission"],
        ["2026-06-03", "Qualité", "Score conformité recalculé", "Système"],
    ]

    return kpis, risques, controles, pistes
