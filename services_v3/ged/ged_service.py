from repositories.ged.ged_repository import (
    list_ged_documents,
    update_document_ged,
    archive_document
)

from services_v3.history.history_service import (
    log_action
)


def get_ged_dashboard():

    documents = list_ged_documents()

    active = [
        item for item in documents
        if item.get("ged_status") != "archive"
    ]

    archived = [
        item for item in documents
        if item.get("ged_status") == "archive"
    ]

    return {
        "count": len(documents),
        "active_count": len(active),
        "archived_count": len(archived),
        "items": documents
    }


def classify_document(document_id, data):

    category = data.get("category", "non_classe")
    tags = data.get("tags", "")

    update_document_ged(
        document_id=document_id,
        category=category,
        tags=tags
    )

    log_action(
        module="ged",
        action="classification_document",
        statut="ok",
        reference_type="document",
        reference_id=document_id,
        message="Document classé dans la GED",
        metadata={
            "category": category,
            "tags": tags
        }
    )

    return {
        "success": True,
        "document_id": document_id,
        "category": category,
        "tags": tags,
        "message": "Document classé"
    }


def archive_ged_document(document_id):

    archive_document(document_id)

    log_action(
        module="ged",
        action="archivage_document",
        statut="ok",
        reference_type="document",
        reference_id=document_id,
        message="Document archivé dans la GED"
    )

    return {
        "success": True,
        "document_id": document_id,
        "message": "Document archivé"
    }

