from services.db_postgres import get_session
from sqlalchemy import text


def get_document_for_ocr(document_id):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                societe_id,
                original_filename,
                stored_filename,
                storage_path,
                mime_type,
                file_size
            FROM documents
            WHERE id = :document_id
            """
        ),
        {
            "document_id": document_id
        }
    )

    row = result.fetchone()
    session.close()

    if not row:
        return None

    return {
        "id": row[0],
        "societe_id": row[1],
        "original_filename": row[2],
        "stored_filename": row[3],
        "storage_path": row[4],
        "mime_type": row[5],
        "file_size": row[6]
    }


def update_document_ocr_success(document_id, ocr_text):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE documents
            SET
                statut_ocr = 'termine',
                ocr_text = :ocr_text,
                ocr_error = NULL,
                ocr_processed_at = CURRENT_TIMESTAMP
            WHERE id = :document_id
            """
        ),
        {
            "document_id": document_id,
            "ocr_text": ocr_text
        }
    )

    session.commit()
    session.close()


def update_document_ocr_error(document_id, error_message):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE documents
            SET
                statut_ocr = 'erreur',
                ocr_error = :ocr_error,
                ocr_processed_at = CURRENT_TIMESTAMP
            WHERE id = :document_id
            """
        ),
        {
            "document_id": document_id,
            "ocr_error": error_message
        }
    )

    session.commit()
    session.close()
