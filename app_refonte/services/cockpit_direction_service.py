from app_refonte.services.orchestration_cabinet_service import charger_orchestration_cabinet


def charger_cockpit_direction():
    kpis, synthese = charger_orchestration_cabinet()

    indicateurs = [
        ["Score cabinet", f"{kpis['score_cabinet']}%", "Pilotage global"],
        ["Score qualité", f"{kpis['score_qualite']}%", "Qualité dossiers"],
        ["Score conformité", f"{kpis['score_conformite']}%", "RGPD / LCB-FT"],
        ["Score risque", f"{kpis['score_risque']}%", "Exposition cabinet"],
        ["Score clôture", f"{kpis['score_cloture']}%", "Préparation clôture"],
    ]

    decisions = synthese["decisions"]
    risques = synthese["risques"]
    blocages = synthese["blocages"]
    priorites = synthese["priorites"]

    return kpis, indicateurs, decisions, risques, blocages, priorites
