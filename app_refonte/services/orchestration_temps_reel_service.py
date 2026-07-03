from app_refonte.services.orchestration_postgres_service import charger_orchestration_postgres
from app_refonte.services.centre_decision_service import charger_centre_decision
from app_refonte.services.salle_supervision_service import charger_salle_supervision
from app_refonte.services.gestion_risques_service import charger_gestion_risques


def charger_orchestration_temps_reel():
    data_pg = charger_orchestration_postgres()
    pg = data_pg["kpis"]

    decision_kpis, decisions, alertes, priorites = charger_centre_decision()
    supervision_kpis, dossiers, alertes_supervision, charge = charger_salle_supervision()
    risques_kpis, risques, plans = charger_gestion_risques()

    cerveau = {
        "score_global": pg["score_global"],
        "alertes_totales": pg["notifications_non_lues"],
        "dossiers_prioritaires": pg["taches_critiques"],
        "dossiers_prets_visa": pg["clients_revision"],
        "dossiers_prets_cloture": max(0, pg["clients_total"] - pg["clients_revision"]),
        "niveau_action": "Prioritaire" if pg["taches_critiques"] >= 10 else "Normal",
    }

    synthese = {
        "decisions": decisions[:5],
        "dossiers_supervision": dossiers[:5],
        "risques": risques[:5],
        "blocages": risques[:5],
        "priorites": priorites[:5],
    }

    actions_du_jour = []
    for index, t in enumerate(data_pg["taches"][:5], start=1):
        actions_du_jour.append([
            str(index),
            t.get("titre") or "Tâche prioritaire",
            "Chef de mission" if t.get("priorite") in ("CRITIQUE", "HAUTE") else "Collaborateur",
            "Aujourd'hui" if t.get("priorite") in ("CRITIQUE", "HAUTE") else "48h",
        ])

    flux = [
        ["PostgreSQL", "Clients actifs", pg["clients_total"]],
        ["PostgreSQL", "Tâches ouvertes", pg["taches_ouvertes"]],
        ["PostgreSQL", "Tâches critiques", pg["taches_critiques"]],
        ["PostgreSQL", "Notifications non lues", pg["notifications_non_lues"]],
        ["PostgreSQL", "Score global réel", f"{pg['score_global']}%"],
    ]

    return cerveau, synthese, actions_du_jour, flux
