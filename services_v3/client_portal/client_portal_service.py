from repositories.client_portal.client_portal_repository import (
    get_client_portal_summary
)


def get_client_portal_dashboard(societe_id):

    client = get_client_portal_summary(societe_id)

    if not client:
        return {
            "found": False,
            "message": "Client introuvable"
        }

    return {
        "found": True,
        "client": client,
        "onboarding": {
            "statut": "actif",
            "progression": 35,
            "etape_courante": "Dépôt des pièces"
        },
        "documents": {
            "pieces_deposees": 0,
            "pieces_en_attente": 5,
            "ocr_statut": "prêt"
        },
        "precompta": {
            "statut": "en_attente_documents",
            "ia": "prête"
        },
        "cabinet": {
            "message": "Votre cabinet suit votre dossier en temps réel."
        }
    }

