from app_refonte.services.orchestration_postgres_service import charger_orchestration_postgres


def charger_centre_decision():
    data_pg = charger_orchestration_postgres()
    pg = data_pg["kpis"]

    kpis = {
        "decisions_urgentes": pg["taches_critiques"],
        "arbitrages_ec": pg["clients_revision"],
        "dossiers_prioritaires": pg["taches_critiques"],
        "alertes_globales": pg["notifications_non_lues"],
        "score_cabinet": pg["score_global"],
    }

    decisions = []
    for t in data_pg["taches"]:
        priorite = t.get("priorite") or "NORMALE"
        niveau = "Critique" if priorite == "CRITIQUE" else "Haute" if priorite == "HAUTE" else "Normale"
        responsable = "Chef de mission" if priorite in ("CRITIQUE", "HAUTE") else "Collaborateur"
        decisions.append([
            t.get("raison_sociale") or "Cabinet",
            t.get("titre") or "Décision cabinet",
            responsable,
            niveau,
            "Traiter la tâche prioritaire",
        ])

    alertes = []
    for n in data_pg["notifications"]:
        alertes.append([
            n.get("niveau") or "INFO",
            n.get("titre") or "Notification cabinet",
        ])

    priorites = []
    for index, t in enumerate(data_pg["taches"][:5], start=1):
        priorites.append([
            str(index),
            t.get("titre") or "Tâche prioritaire",
            "Aujourd'hui" if t.get("priorite") in ("CRITIQUE", "HAUTE") else "48h",
        ])

    return kpis, decisions[:10], alertes[:10], priorites
