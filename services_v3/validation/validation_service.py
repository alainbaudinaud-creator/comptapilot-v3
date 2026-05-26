from repositories.validation.validation_repository import (
    list_precompta_to_validate,
    update_precompta_status,
    get_precompta
)

from services_v3.history.history_service import (
    log_action
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
        log_action(
            module="validation",
            action="validation_precompta",
            statut="erreur",
            reference_type="precompta",
            reference_id=precompta_id,
            message="Précompta introuvable"
        )

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

    log_action(
        module="validation",
        action="validation_precompta",
        statut="ok",
        societe_id=precompta.get("societe_id"),
        reference_type="precompta",
        reference_id=precompta_id,
        message="Précompta validée",
        metadata={
            "validated_by": data.get("validated_by", "collaborateur"),
            "commentaire": data.get("commentaire")
        }
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
        log_action(
            module="validation",
            action="rejet_precompta",
            statut="erreur",
            reference_type="precompta",
            reference_id=precompta_id,
            message="Précompta introuvable"
        )

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

    log_action(
        module="validation",
        action="rejet_precompta",
        statut="ok",
        societe_id=precompta.get("societe_id"),
        reference_type="precompta",
        reference_id=precompta_id,
        message="Précompta rejetée",
        metadata={
            "validated_by": data.get("validated_by", "collaborateur"),
            "commentaire": data.get("commentaire")
        }
    )

    return {
        "success": True,
        "precompta_id": precompta_id,
        "statut_validation": "rejetee",
        "message": "Précompta rejetée"
    }


