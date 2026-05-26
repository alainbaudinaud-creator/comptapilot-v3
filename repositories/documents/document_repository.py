from services.db_postgres import get_session
from sqlalchemy import text


def create_document_record(
    societe_id,
    original_filename,
    stored_filename,
    storage_path,
    mime_type,
    file_size
):

    session = get_session()

    result = session.execute(
        text(
            """
            INSERT INTO documents (
                societe_id,
                original_filename,
                stored_filename,
                storage_path,
                mime_type,
                file_size,
                statut_ocr,
                statut_precompta
            )
            VALUES (
                :societe_id,
                :original_filename,
                :stored_filename,
                :storage_path,
                :mime_type,
                :file_size,
                'en_attente',
                'en_attente'
            )
            RETURNING id
            """
        ),
        {
            "societe_id": societe_id,
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "storage_path": storage_path,
            "mime_type": mime_type,
            "file_size": file_size
        }
    )

    document_id = result.fetchone()[0]

    session.commit()
    session.close()

    return document_id

