from repositories.client_space.client_space_repository import (
    get_client_space_data
)


def get_client_space_dashboard(societe_id=1):

    data = get_client_space_data(societe_id)

    if not data:
        return {
            "success": False,
            "message": "Société introuvable"
        }

    return {
        "success": True,
        "societe": data.get("societe"),
        "metrics": data.get("metrics"),
        "recent_documents": data.get("recent_documents")
    }

