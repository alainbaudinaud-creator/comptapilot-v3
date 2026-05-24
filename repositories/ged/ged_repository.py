from services.db_postgres import get_session
from sqlalchemy import text


def list_ged_documents():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                societe_id,
                original_filename,
                mime_type,
                file_size,
                statut_ocr,
                statut_precompta,
                ged_category,
                ged_status,
                ged_tags,
                created_at,
                archived_at
            FROM documents
            ORDER BY created_at DESC
            LIMIT 300
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "id": row[0],
            "societe_id": row[1],
            "filename": row[2],
            "mime_type": row[3],
            "file_size": row[4],
            "statut_ocr": row[5],
            "statut_precompta": row[6],
            "ged_category": row[7],
            "ged_status": row[8],
            "ged_tags": row[9],
            "created_at": str(row[10]),
            "archived_at": str(row[11]) if row[11] else None
        }
        for row in rows
    ]


def update_document_ged(document_id, category, tags):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE documents
            SET
                ged_category = :category,
                ged_tags = :tags
            WHERE id = :document_id
            """
        ),
        {
            "document_id": document_id,
            "category": category,
            "tags": tags
        }
    )

    session.commit()
    session.close()


def archive_document(document_id):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE documents
            SET
                ged_status = 'archive',
                archived_at = CURRENT_TIMESTAMP
            WHERE id = :document_id
            """
        ),
        {
            "document_id": document_id
        }
    )

    session.commit()
    session.close()
