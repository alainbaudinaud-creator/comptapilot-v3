from services.db_postgres import get_session
from sqlalchemy import text


def get_alerts_raw_data():

    session = get_session()

    data = {}

    data["ocr_errors"] = session.execute(
        text(
            """
            SELECT id, societe_id, original_filename, ocr_error, created_at
            FROM documents
            WHERE statut_ocr = 'erreur'
            ORDER BY created_at DESC
            LIMIT 50
            """
        )
    ).fetchall()

    data["ocr_pending"] = session.execute(
        text(
            """
            SELECT id, societe_id, original_filename, created_at
            FROM documents
            WHERE statut_ocr = 'en_attente'
            ORDER BY created_at DESC
            LIMIT 50
            """
        )
    ).fetchall()

    data["precompta_pending"] = session.execute(
        text(
            """
            SELECT id, document_id, societe_id, fournisseur, montant_ttc, created_at
            FROM precompta_documents
            WHERE statut_validation = 'a_valider'
            ORDER BY created_at DESC
            LIMIT 50
            """
        )
    ).fetchall()

    data["precompta_rejected"] = session.execute(
        text(
            """
            SELECT id, document_id, societe_id, fournisseur, commentaire_validation, created_at
            FROM precompta_documents
            WHERE statut_validation = 'rejetee'
            ORDER BY created_at DESC
            LIMIT 50
            """
        )
    ).fetchall()

    session.close()

    return data

