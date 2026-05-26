from services.db_postgres import get_session
from sqlalchemy import text


def get_precompta_for_ecriture(precompta_id):

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
                compte_fournisseur,
                statut_validation
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
        "compte_fournisseur": row[10],
        "statut_validation": row[11]
    }


def create_ecriture_lines(precompta, lines):

    session = get_session()

    for line in lines:
        session.execute(
            text(
                """
                INSERT INTO ecritures_v3 (
                    precompta_id,
                    document_id,
                    societe_id,
                    date_ecriture,
                    libelle,
                    compte,
                    debit,
                    credit,
                    journal,
                    source
                )
                VALUES (
                    :precompta_id,
                    :document_id,
                    :societe_id,
                    :date_ecriture,
                    :libelle,
                    :compte,
                    :debit,
                    :credit,
                    'ACH',
                    'precompta_v3'
                )
                """
            ),
            {
                "precompta_id": precompta.get("id"),
                "document_id": precompta.get("document_id"),
                "societe_id": precompta.get("societe_id"),
                "date_ecriture": precompta.get("date_document"),
                "libelle": line.get("libelle"),
                "compte": line.get("compte"),
                "debit": line.get("debit"),
                "credit": line.get("credit")
            }
        )

    session.execute(
        text(
            """
            UPDATE precompta_documents
            SET statut_validation = 'transformee_ecriture'
            WHERE id = :precompta_id
            """
        ),
        {
            "precompta_id": precompta.get("id")
        }
    )

    session.commit()

    session.close()


