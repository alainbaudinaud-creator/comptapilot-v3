from services.db_postgres import get_session
from sqlalchemy import text


def list_precompta_to_validate():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
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
                statut_validation,
                created_at
            FROM precompta_documents
            ORDER BY created_at DESC
            LIMIT 100
            """
        )
    )

    rows = result.fetchall()

    session.close()

    return [
        {
            "id": row[0],
            "document_id": row[1],
            "societe_id": row[2],
            "fournisseur": row[3],
            "type_document": row[4],
            "date_document": row[5],
            "montant_ht": float(row[6]) if row[6] else None,
            "montant_tva": float(row[7]) if row[7] else None,
            "montant_ttc": float(row[8]) if row[8] else None,
            "compte_charge": row[9],
            "compte_tva": row[10],
            "compte_fournisseur": row[11],
            "confiance": float(row[12]) if row[12] else 0,
            "statut_validation": row[13],
            "created_at": str(row[14])
        }
        for row in rows
    ]


def update_precompta_status(
    precompta_id,
    statut_validation,
    commentaire_validation=None,
    validated_by=None
):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE precompta_documents
            SET
                statut_validation = :statut_validation,
                commentaire_validation = :commentaire_validation,
                validated_by = :validated_by,
                validated_at = CURRENT_TIMESTAMP
            WHERE id = :precompta_id
            """
        ),
        {
            "precompta_id": precompta_id,
            "statut_validation": statut_validation,
            "commentaire_validation": commentaire_validation,
            "validated_by": validated_by
        }
    )

    session.commit()

    session.close()


def get_precompta(precompta_id):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                document_id,
                societe_id,
                fournisseur,
                date_document,
                montant_ht,
                montant_tva,
                montant_ttc,
                compte_charge,
                compte_tva,
                compte_fournisseur
            FROM precompta_documents
            WHERE id = :precompta_id
            """
        ),
        {
            "precompta_id": precompta_id
        }
    )

    row = result.fetchone()

    session.close()

    if not row:
        return None

    return {
        "id": row[0],
        "document_id": row[1],
        "societe_id": row[2],
        "fournisseur": row[3],
        "date_document": row[4],
        "montant_ht": row[5],
        "montant_tva": row[6],
        "montant_ttc": row[7],
        "compte_charge": row[8],
        "compte_tva": row[9],
        "compte_fournisseur": row[10]
    }
