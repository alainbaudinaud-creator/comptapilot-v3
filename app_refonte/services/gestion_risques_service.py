from app_refonte.services.orchestration_postgres_service import charger_orchestration_postgres


def charger_gestion_risques():
    data_pg = charger_orchestration_postgres()
    pg = data_pg["kpis"]

    risques_total = pg["taches_critiques"] + pg["notifications_non_lues"]
    risques_critiques = pg["taches_critiques"]
    risques_maitrises = max(0, pg["taches_ouvertes"] - pg["taches_critiques"])
    plans_actions = risques_total

    kpis = {
        "risques_total": risques_total,
        "risques_critiques": risques_critiques,
        "risques_maitrises": risques_maitrises,
        "plans_actions": plans_actions,
        "score_global": pg["score_global"],
    }

    risques = []

    for t in data_pg["taches"]:
        priorite = t.get("priorite") or "NORMALE"
        criticite = "Critique" if priorite == "CRITIQUE" else "Élevé" if priorite == "HAUTE" else "Moyen"
        impact = "Élevé" if priorite in ("CRITIQUE", "HAUTE") else "Moyen"
        responsable = "Chef de mission" if priorite in ("CRITIQUE", "HAUTE") else "Collaborateur"
        risques.append([
            t.get("raison_sociale") or "Cabinet",
            t.get("titre") or "Tâche cabinet",
            criticite,
            impact,
            responsable,
            t.get("statut") or "A_TRAITER",
        ])

    for n in data_pg["notifications"]:
        niveau = n.get("niveau") or "INFO"
        criticite = "Élevé" if niveau in ("WARNING", "CRITIQUE", "ALERTE") else "Moyen"
        risques.append([
            n.get("raison_sociale") or "Cabinet",
            n.get("titre") or "Notification cabinet",
            criticite,
            niveau,
            "Cabinet",
            n.get("statut") or "NON_LUE",
        ])

    plans = []
    for r in risques[:8]:
        priorite = "Critique" if r[2] == "Critique" else "Haute" if r[2] == "Élevé" else "Normale"
        plans.append([
            r[0],
            f"Traiter : {r[1]}",
            r[4],
            priorite,
        ])

    return kpis, risques[:10], plans
