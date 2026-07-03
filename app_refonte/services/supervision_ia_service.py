from app_refonte.services.taches_ia_service import charger_taches_ia

def charger_supervision_ia():
    kpis, taches = charger_taches_ia()
    return kpis, taches
