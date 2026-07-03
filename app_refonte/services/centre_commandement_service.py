from app_refonte.services.orchestration_cabinet_service import charger_orchestration_cabinet
from app_refonte.services.orchestration_postgres_service import charger_orchestration_postgres


def charger_centre_commandement():
    
    kpis, synthese = charger_orchestration_cabinet()
    data_pg = charger_orchestration_postgres()
        

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
        
        "alertes_totales": data_pg["kpis"]["notifications_non_lues"],
        
        
        "dossiers_prioritaires": data_pg["kpis"]["taches_critiques"],
        
        "prets_visa": kpis["dossiers_prets_visa"],
        "prets_cloture": kpis["dossiers_prets_cloture"],
    }

    return commandement, synthese
