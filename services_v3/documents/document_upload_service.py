import os
import uuid
from werkzeug.utils import secure_filename

from repositories.documents.document_repository import (
    create_document_record
)


UPLOAD_ROOT = "/app/uploads/client_portal"

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def is_allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


def upload_client_document(file, societe_id):

    if not file:
        return {
            "success": False,
            "message": "Aucun fichier reçu"
        }

    if not is_allowed_file(file.filename):
        return {
            "success": False,
            "message": "Format de fichier non autorisé"
        }

    os.makedirs(UPLOAD_ROOT, exist_ok=True)

    safe_name = secure_filename(file.filename)
    extension = safe_name.rsplit(".", 1)[1].lower()

    stored_filename = f"{uuid.uuid4()}.{extension}"
    storage_path = os.path.join(UPLOAD_ROOT, stored_filename)

    file.save(storage_path)

    file_size = os.path.getsize(storage_path)

    document_id = create_document_record(
        societe_id=societe_id,
        original_filename=safe_name,
        stored_filename=stored_filename,
        storage_path=storage_path,
        mime_type=file.mimetype,
        file_size=file_size
    )

    return {
        "success": True,
        "document_id": document_id,
        "original_filename": safe_name,
        "stored_filename": stored_filename,
        "file_size": file_size,
        "statut_ocr": "en_attente",
        "statut_precompta": "en_attente",
        "message": "Document reçu et prêt pour OCR"
    }

