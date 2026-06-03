from app_refonte.services.visas_cabinet_service import charger_visas_cabinet
from app_refonte.services.controle_ia_service import calculer_controles_ia
from app_refonte.services.revision_cabinet_service import charger_revision_cabinet


def calculer_score_revision():
    visas = charger_visas_cabinet()
    controle_ia = calculer_controles_ia()
    revision = charger_revision_cabinet()

    nb_visas = int(visas.get("nb_visas", 0))
    nb_attendus = int(visas.get("nb_attendus", 3) or 3)

    score_visas = int((nb_visas / nb_attendus) * 40) if nb_attendus else 0

    risque_ia = int(controle_ia.get("score_risque", 0) or 0)
    score_ia = max(0, 30 - int(risque_ia * 0.3))

    points_bloquants = int(revision.get("points_bloquants", 0) or 0)
    score_revision = max(0, 30 - points_bloquants)

    score_global = max(0, min(100, score_visas + score_ia + score_revision))

    if score_global >= 85 and visas.get("cloture_autorisee"):
        niveau = "PRET_CLOTURE"
        libelle = "Dossier prêt pour clôture"
    elif score_global >= 70:
        niveau = "REVISION_AVANCEE"
        libelle = "Révision avancée"
    elif score_global >= 45:
        niveau = "POINTS_A_TRAITER"
        libelle = "Points à traiter"
    else:
        niveau = "DOSSIER_A_RISQUE"
        libelle = "Dossier à risque"

    return {
        "score_global": score_global,
        "niveau": niveau,
        "libelle": libelle,
        "detail": {
            "score_visas": score_visas,
            "score_ia": score_ia,
            "score_revision": score_revision,
            "nb_visas": nb_visas,
            "nb_attendus": nb_attendus,
            "risque_ia": risque_ia,
            "points_bloquants": points_bloquants,
            "cloture_autorisee": bool(visas.get("cloture_autorisee"))
        },
        "sources": {
            "visas": visas,
            "controle_ia": controle_ia,
            "revision": revision
        }
    }
