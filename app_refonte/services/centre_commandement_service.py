from app_refonte.services.orchestration_cabinet_service import charger_orchestration_cabinet


def charger_centre_commandement():
    kpis, synthese = charger_orchestration_cabinet()

    commandement = {
        "score_global": round(
            (
                kpis["score_cabinet"]
                + kpis["score_supervision"]
                + kpis["score_risque"]
                + kpis["score_controle"]
                + kpis["score_conformite"]
                + kpis["score_qualite"]
                + kpis["score_cloture"]
            ) / 7
        ),
        "alertes_totales": kpis["alertes_totales"],
        "dossiers_prioritaires": kpis["dossiers_prioritaires"],
        "prets_visa": kpis["dossiers_prets_visa"],
        "prets_cloture": kpis["dossiers_prets_cloture"],
    }

    return commandement, synthese
