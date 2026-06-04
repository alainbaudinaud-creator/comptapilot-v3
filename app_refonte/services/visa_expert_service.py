def charger_visa_expert():
    kpis = {
        "dossiers_prets": 9,
        "a_valider_chef": 5,
        "a_visa_ec": 4,
        "bloques": 3,
        "score_conformite": 88,
    }

    dossiers = [
        ["Orange SA", "Révision terminée", "Chef de mission", "À viser", "92%"],
        ["IFG Holding", "Contrôles bloquants", "Collaborateur", "Bloqué", "71%"],
        ["Cabinet Demo", "Feuille maîtresse validée", "Expert-comptable", "Visa final", "96%"],
        ["SAS Lumière", "Pièces GED manquantes", "Collaborateur", "Bloqué", "68%"],
        ["SCI Patrimoine", "Référentiel révision OK", "Chef de mission", "À valider", "89%"],
    ]

    validations = [
        ["Collaborateur", "Préparation dossier", "Réalisé", "Justifications et GED contrôlées"],
        ["Chef de mission", "Revue qualité", "En cours", "Contrôles fiscaux à finaliser"],
        ["Expert-comptable", "Visa final", "À faire", "En attente validation chef"],
        ["Système", "Autorisation clôture", "Bloquée", "3 dossiers avec points bloquants"],
    ]

    return kpis, dossiers, validations
