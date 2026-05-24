import os

from repositories.ocr.ocr_repository import (
    get_document_for_ocr,
    update_document_ocr_success,
    update_document_ocr_error
)

from services_v3.history.history_service import (
    log_action
)


def run_ocr_on_document(document_id):

    document = get_document_for_ocr(document_id)

    if not document:
        log_action(
            module="ocr",
            action="ocr_document",
            statut="erreur",
            reference_type="document",
            reference_id=document_id,
            message="Document introuvable"
        )

        return {
            "success": False,
            "message": "Document introuvable"
        }

    storage_path = document.get("storage_path")

    if not storage_path or not os.path.exists(storage_path):

        update_document_ocr_error(
            document_id,
            "Fichier physique introuvable"
        )

        log_action(
            module="ocr",
            action="ocr_document",
            statut="erreur",
            societe_id=document.get("societe_id"),
            reference_type="document",
            reference_id=document_id,
            message="Fichier physique introuvable"
        )

        return {
            "success": False,
            "message": "Fichier physique introuvable"
        }

    try:
        ocr_text = generate_placeholder_ocr_text(document)

        update_document_ocr_success(
            document_id,
            ocr_text
        )

        log_action(
            module="ocr",
            action="ocr_document",
            statut="ok",
            societe_id=document.get("societe_id"),
            reference_type="document",
            reference_id=document_id,
            message="OCR document terminé",
            metadata={
                "original_filename": document.get("original_filename"),
                "file_size": document.get("file_size")
            }
        )

        return {
            "success": True,
            "document_id": document_id,
            "statut_ocr": "termine",
            "ocr_text_preview": ocr_text[:250],
            "message": "OCR terminé"
        }

    except Exception as exc:

        update_document_ocr_error(
            document_id,
            str(exc)
        )

        log_action(
            module="ocr",
            action="ocr_document",
            statut="erreur",
            societe_id=document.get("societe_id"),
            reference_type="document",
            reference_id=document_id,
            message=str(exc)
        )

        return {
            "success": False,
            "document_id": document_id,
            "message": "Erreur OCR",
            "error": str(exc)
        }


def generate_placeholder_ocr_text(document):

    return f"""
OCR V3 — Extraction simulée

Document : {document.get("original_filename")}
Société ID : {document.get("societe_id")}
Type MIME : {document.get("mime_type")}
Taille : {document.get("file_size")} octets

Texte détecté :
Facture fournisseur simulée.
Montant HT : à détecter.
TVA : à détecter.
Montant TTC : à détecter.
Date facture : à détecter.
Numéro facture : à détecter.

Statut :
Document prêt pour analyse précomptable IA.
""".strip()
