from app_refonte.services.controle_ia_service import calculer_controles_ia
from app_refonte.services.score_revision_service import calculer_score_revision


def generer_plan_action_ia():

    controle = calculer_controles_ia()
    score = calculer_score_revision()

    actions = []

    for alerte in controle.get("alertes", []):

        if "471" in alerte or "467" in alerte:
            actions.append({
                "priorite": "HAUTE",
                "action": "Justifier et solder les comptes d'attente 471/467"
            })

        elif "fournisseur" in alerte.lower():
            actions.append({
                "priorite": "HAUTE",
                "action": "Contrôler les fournisseurs débiteurs"
            })

        elif "client" in alerte.lower():
            actions.append({
                "priorite": "MOYENNE",
                "action": "Contrôler les clients créditeurs"
            })

        elif "libellé" in alerte.lower():
            actions.append({
                "priorite": "MOYENNE",
                "action": "Compléter les libellés manquants"
            })

    points = score["detail"]["points_bloquants"]

    if points > 0:
        actions.append({
            "priorite": "HAUTE",
            "action": f"Traiter les {points} points bloquants de révision"
        })

    actions.append({
        "priorite": "NORMALE",
        "action": "Relancer le contrôle IA après correction"
    })

    return {
        "score_global": score["score_global"],
        "niveau": score["niveau"],
        "nb_actions": len(actions),
        "actions": actions
    }
