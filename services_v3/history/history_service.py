import json

from repositories.history.history_repository import (
    create_history_entry,
    list_history
)


def log_action(
    module,
    action,
    statut="ok",
    societe_id=None,
    reference_type=None,
    reference_id=None,
    message=None,
    metadata=None,
    created_by="system"
):

    if metadata is not None:
        metadata_value = json.dumps(
            metadata,
            ensure_ascii=False
        )
    else:
        metadata_value = None

    history_id = create_history_entry(
        {
            "module": module,
            "action": action,
            "statut": statut,
            "societe_id": societe_id,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "message": message,
            "metadata": metadata_value,
            "created_by": created_by
        }
    )

    return history_id


def get_history_dashboard():

    items = list_history()

    return {
        "count": len(items),
        "items": items
    }

