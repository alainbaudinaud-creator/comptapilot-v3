from app_refonte.services.orchestration_cabinet_service import charger_orchestration_cabinet
from app_refonte.services.orchestration_postgres_service import charger_orchestration_postgres


def charger_cockpit_direction():
    kpis, synthese = charger_orchestration_cabinet()
    data_pg = charger_orchestration_postgres()

    kpis["score_cabinet"] = data_pg["kpis"]["score_global"]
    kpis["alertes_totales"] = data_pg["kpis"]["notifications_non_lues"]
    kpis["dossiers_prioritaires"] = data_pg["kpis"]["taches_critiques"]

    indicateurs = [
        ["Score cabinet réel", f"{data_pg['kpis']['score_global']}%", "Calcul PostgreSQL"],
        ["Clients actifs", data_pg["kpis"]["clients_total"], "clients_v3"],
        ["Clients en révision / validation", data_pg["kpis"]["clients_revision"], "clients_v3"],
        ["Tâches ouvertes", data_pg["kpis"]["taches_ouvertes"], "taches_cabinet_v3"],
        ["Tâches critiques", data_pg["kpis"]["taches_critiques"], "taches_cabinet_v3"],
    ]

    decisions = synthese["decisions"]
    risques = synthese["risques"]
    blocages = synthese["blocages"]
    priorites = synthese["priorites"]

    return kpis, indicateurs, decisions, risques, blocages, priorites
