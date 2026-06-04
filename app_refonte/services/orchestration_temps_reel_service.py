from app_refonte.services.orchestration_cabinet_service import charger_orchestration_cabinet


def charger_orchestration_temps_reel():
    kpis, synthese = charger_orchestration_cabinet()

    score_global = round(
        (
            kpis["score_cabinet"]
            + kpis["score_supervision"]
            + kpis["score_risque"]
            + kpis["score_controle"]
            + kpis["score_conformite"]
            + kpis["score_qualite"]
            + kpis["score_cloture"]
        ) / 7
    )

    cerveau = {
        "score_global": score_global,
        "alertes_totales": kpis["alertes_totales"],
        "dossiers_prioritaires": kpis["dossiers_prioritaires"],
        "dossiers_prets_visa": kpis["dossiers_prets_visa"],
        "dossiers_prets_cloture": kpis["dossiers_prets_cloture"],
        "niveau_action": "Prioritaire" if kpis["alertes_totales"] > 30 else "Normal",
    }

    actions_du_jour = [
        ["1", "Traiter les blocages critiques", "Expert-comptable", "Immédiat"],
        ["2", "Valider les dossiers prêts au visa", "Expert-comptable", "Aujourd'hui"],
        ["3", "Relancer les pièces GED manquantes", "Collaborateur", "48h"],
        ["4", "Arbitrer les risques fiscaux sensibles", "Chef de mission", "48h"],
    ]

    flux = [
        ["Centre décision", "Décisions prioritaires", len(synthese["decisions"])],
        ["Salle supervision", "Dossiers suivis", len(synthese["dossiers_supervision"])],
        ["Gestion risques", "Risques majeurs", len(synthese["risques"])],
        ["Comité clôture", "Blocages restants", len(synthese["blocages"])],
        ["Priorités", "Actions actives", len(synthese["priorites"])],
    ]

    return cerveau, synthese, actions_du_jour, flux
