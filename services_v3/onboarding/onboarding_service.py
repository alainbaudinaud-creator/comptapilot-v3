from repositories.onboarding.onboarding_repository import (
    create_client_onboarding
)


def onboard_new_client(data):

    societe_id = create_client_onboarding(
        nom=data.get("nom"),
        siren=data.get("siren"),
        email=data.get("email"),
        telephone=data.get("telephone")
    )

    return {
        "societe_id": societe_id,
        "workflow": "initialisé",
        "imports": "en_attente",
        "ocr": "prêt",
        "precompta_ia": "prête",
        "statut": "client_cree"
    }

