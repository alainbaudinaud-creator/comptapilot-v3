from repositories.validation.validation_repository import (
    list_precompta_to_validate,
    update_precompta_status,
    get_precompta
)


def get_validation_queue():

    items = list_precompta_to_validate()

    return {
        "count": len(items),
        "items": items
    }


def validate_precompta(precompta_id, data):

    precompta = get_precompta(precompta_id)

    if not precompta:
        return {
            "success": False,
            "message": "Précompta introuvable"
        }

    update_precompta_status(
        precompta_id=precompta_id,
        statut_validation="validee",
        commentaire_validation=data.get("commentaire"),
        validated_by=data.get("validated_by", "collaborateur")
    )

    return {
        "success": True,
        "precompta_id": precompta_id,
        "statut_validation": "validee",
        "message": "Précompta validée"
    }


def reject_precompta(precompta_id, data):

    precompta = get_precompta(precompta_id)

    if not precompta:
        return {
            "success": False,
            "message": "Précompta introuvable"
        }

    update_precompta_status(
        precompta_id=precompta_id,
        statut_validation="rejetee",
        commentaire_validation=data.get("commentaire"),
        validated_by=data.get("validated_by", "collaborateur")
    )

    return {
        "success": True,
        "precompta_id": precompta_id,
        "statut_validation": "rejetee",
        "message": "Précompta rejetée"
    }
