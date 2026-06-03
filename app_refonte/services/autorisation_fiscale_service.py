from app_refonte.services.score_revision_service import calculer_score_revision


def verifier_autorisation_fiscale():
    score = calculer_score_revision()
    detail = score.get("detail", {})

    score_global = int(score.get("score_global", 0) or 0)
    cloture_autorisee = bool(detail.get("cloture_autorisee", False))
    nb_visas = int(detail.get("nb_visas", 0) or 0)
    nb_attendus = int(detail.get("nb_attendus", 3) or 3)

    declarations_autorisees = (
        score_global >= 85
        and cloture_autorisee
        and nb_visas >= nb_attendus
    )

    if declarations_autorisees:
        statut = "DECLARATIONS_AUTORISEES"
        message = "Le dossier est suffisamment révisé. Les déclarations fiscales peuvent être préparées."
    elif not cloture_autorisee or nb_visas < nb_attendus:
        statut = "VISAS_INCOMPLETS"
        message = "Les déclarations fiscales sont bloquées : tous les visas cabinet ne sont pas validés."
    else:
        statut = "SCORE_REVISION_INSUFFISANT"
        message = "Les déclarations fiscales sont bloquées : le score global de révision doit atteindre 85/100."

    return {
        "declarations_autorisees": declarations_autorisees,
        "statut": statut,
        "message": message,
        "score_global": score_global,
        "seuil_score": 85,
        "nb_visas": nb_visas,
        "nb_attendus": nb_attendus,
        "score_revision": score
    }
