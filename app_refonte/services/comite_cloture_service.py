def charger_comite_cloture():
    kpis = {
        "dossiers_comite": 18,
        "go_cloture": 11,
        "no_go": 3,
        "a_arbitrer": 4,
        "score_cloture": 87,
    }

    dossiers = [
        ["Orange SA", "Feuille maîtresse OK", "Chef mission validé", "À viser EC", "GO sous réserve"],
        ["IFG Holding", "Points bloquants qualité", "Non validé", "Bloqué", "NO GO"],
        ["Cabinet Demo", "Cycles validés", "Visa EC validé", "Prêt clôture", "GO"],
        ["SAS Lumière", "Pièces GED manquantes", "Non validé", "Bloqué", "NO GO"],
        ["SCI Patrimoine", "Fiscal à arbitrer", "Chef mission validé", "Arbitrage EC", "À arbitrer"],
    ]

    blocages = [
        ["Qualité", "IFG Holding", "Contrôles bloquants non levés", "Critique"],
        ["GED", "SAS Lumière", "Pièces justificatives absentes", "Critique"],
        ["Fiscal", "SCI Patrimoine", "Cadrage TVA à arbitrer", "Élevé"],
        ["Visa EC", "Orange SA", "Visa final en attente", "Moyen"],
    ]

    decisions = [
        ["GO", "Dossier clôturable immédiatement", 11],
        ["GO sous réserve", "Clôturable après visa final", 2],
        ["À arbitrer", "Décision expert-comptable requise", 4],
        ["NO GO", "Blocage clôture", 3],
    ]

    return kpis, dossiers, blocages, decisions
