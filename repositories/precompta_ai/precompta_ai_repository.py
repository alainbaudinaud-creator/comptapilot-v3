from services.db_postgres import get_session
from sqlalchemy import text


def get_document_ocr_data(document_id):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                societe_id,
                original_filename,
                ocr_text
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
        "document_id": row[0],
        "societe_id": row[1],
        "original_filename": row[2],
        "ocr_text": row[3]
    }


def create_precompta_document(data):

    session = get_session()

    result = session.execute(
        text(
            """
            INSERT INTO precompta_documents (
                document_id,
                societe_id,
                fournisseur,
                type_document,
                date_document,
                montant_ht,
                montant_tva,
                montant_ttc,
                compte_charge,
                compte_tva,
                compte_fournisseur,
                confiance,
                statut_validation
            )
            VALUES (
                :document_id,
                :societe_id,
                :fournisseur,
                :type_document,
                :date_document,
                :montant_ht,
                :montant_tva,
                :montant_ttc,
                :compte_charge,
                :compte_tva,
                :compte_fournisseur,
                :confiance,
                'a_valider'
            )
            RETURNING id
            """
        ),
        data
    )

    precompta_id = result.fetchone()[0]

    session.execute(
        text(
            """
            UPDATE documents
            SET statut_precompta = 'generee'
            WHERE id = :document_id
            """
        ),
        {
            "document_id": data.get("document_id")
        }
    )

    session.commit()
    session.close()

    return precompta_id
