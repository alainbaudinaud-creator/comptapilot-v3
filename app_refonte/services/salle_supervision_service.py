from app_refonte.services.orchestration_postgres_service import charger_orchestration_postgres


def charger_salle_supervision():
    data_pg = charger_orchestration_postgres()
    pg = data_pg["kpis"]

    kpis = {
        "dossiers_actifs": pg["clients_total"],
        "alertes_bloquantes": pg["notifications_non_lues"],
        "retards": pg["taches_critiques"],
        "prets_visa": pg["clients_revision"],
        "prets_cloture": max(0, pg["clients_total"] - pg["clients_revision"]),
        "score_global": pg["score_global"],
    }

    dossiers = []
    for client in data_pg["clients"]:
        statut = client.get("statut") or "INCONNU"
        risque = "Risque élevé" if statut in ("REVISION", "VALIDATION_EC") else "Risque moyen"
        score = f"{pg['score_global']}%"
        decision = "À superviser" if statut in ("REVISION", "VALIDATION_EC") else "Suivi normal"
        dossiers.append([
            client.get("raison_sociale"),
            statut,
            "Cabinet",
            risque,
            score,
            decision,
        ])

    alertes = []
    for n in data_pg["notifications"]:
        niveau = n.get("niveau") or "INFO"
        dossier = n.get("raison_sociale") or "Cabinet"
        titre = n.get("titre") or "Notification"
        alertes.append([niveau, dossier, titre])

    charge = [
        ["Tâches ouvertes", pg["taches_ouvertes"], pg["taches_critiques"], "Charge réelle PostgreSQL"],
        ["Notifications non lues", pg["notifications_non_lues"], pg["notifications_non_lues"], "À traiter"],
        ["Clients en révision", pg["clients_revision"], pg["clients_revision"], "Prioritaire"],
        ["Clients actifs", pg["clients_total"], pg["clients_total"], "Portefeuille"],
    ]

    return kpis, dossiers, alertes, charge
