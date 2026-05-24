from services.db_postgres import get_session
from sqlalchemy import text


def get_client_space_data(societe_id):

    session = get_session()

    societe = session.execute(
        text(
            """
            SELECT id, nom, siren, email
            FROM societes
            WHERE id = :societe_id
            """
        ),
        {
            "societe_id": societe_id
        }
    ).fetchone()

    documents_count = session.execute(
        text(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE societe_id = :societe_id
            """
        ),
        {
            "societe_id": societe_id
        }
    ).scalar() or 0

    ocr_pending = session.execute(
        text(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE societe_id = :societe_id
            AND statut_ocr = 'en_attente'
            """
        ),
        {
            "societe_id": societe_id
        }
    ).scalar() or 0

    relances_count = session.execute(
        text(
            """
            SELECT COUNT(*)
            FROM relances_client_v3
            WHERE societe_id = :societe_id
            """
        ),
        {
            "societe_id": societe_id
        }
    ).scalar() or 0

    recent_documents = session.execute(
        text(
            """
            SELECT id, original_filename, statut_ocr, statut_precompta, created_at
            FROM documents
            WHERE societe_id = :societe_id
            ORDER BY created_at DESC
            LIMIT 20
            """
        ),
        {
            "societe_id": societe_id
        }
    ).fetchall()

    session.close()

    if not societe:
        return None

    return {
        "societe": {
            "id": societe[0],
            "nom": societe[1],
            "siren": societe[2],
            "email": societe[3]
        },
        "metrics": {
            "documents_count": documents_count,
            "ocr_pending": ocr_pending,
            "relances_count": relances_count
        },
        "recent_documents": [
            {
                "id": row[0],
                "filename": row[1],
                "statut_ocr": row[2],
                "statut_precompta": row[3],
                "created_at": str(row[4])
            }
            for row in recent_documents
        ]
    }
