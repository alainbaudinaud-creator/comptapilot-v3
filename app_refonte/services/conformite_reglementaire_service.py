def charger_conformite_reglementaire():
    kpis = {
        "score_conformite": 84,
        "dossiers_rgpd": 12,
        "alertes_lcbft": 4,
        "lettres_mission": 9,
        "revues_annuelles": 6,
    }

    obligations = [
        ["RGPD", "Registre traitements clients", "À jour", "Revue annuelle"],
        ["LCB-FT", "Identification bénéficiaire effectif", "Attention", "4 dossiers incomplets"],
        ["Acceptation client", "Contrôle entrée en relation", "OK", "Dossier validé"],
        ["Lettre de mission", "Lettre signée et archivée GED", "Attention", "3 lettres manquantes"],
        ["Indépendance", "Contrôle conflits d'intérêts", "OK", "Aucun conflit détecté"],
        ["Ordre EC", "Dossier qualité cabinet", "À compléter", "Pièces à centraliser"],
    ]

    risques = [
        ["LCB-FT", "Bénéficiaire effectif non documenté", "Élevé", "Blocage acceptation client"],
        ["RGPD", "Durée conservation non renseignée", "Moyen", "Revue registre"],
        ["Mission", "Lettre de mission absente", "Élevé", "Blocage visa EC"],
        ["Indépendance", "Mission sensible à revoir", "Moyen", "Validation expert-comptable"],
    ]

    actions = [
        ["Mettre à jour registre RGPD", "Chef de mission", "En cours"],
        ["Compléter questionnaires LCB-FT", "Collaborateur", "À faire"],
        ["Archiver lettres de mission GED", "Administration", "À faire"],
        ["Revue annuelle conformité client", "Expert-comptable", "Planifiée"],
    ]

    return kpis, obligations, risques, actions
