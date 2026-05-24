from services.db_postgres import get_session
from sqlalchemy import text


def get_ecritures_for_export(societe_id=None):

    session = get_session()

    if societe_id:
        result = session.execute(
            text(
                """
                SELECT
                    id,
                    date_ecriture,
                    journal,
                    compte,
                    libelle,
                    debit,
                    credit,
                    source,
                    societe_id,
                    document_id,
                    precompta_id
                FROM ecritures_v3
                WHERE societe_id = :societe_id
                ORDER BY date_ecriture, id
                """
            ),
            {
                "societe_id": societe_id
            }
        )
    else:
        result = session.execute(
            text(
                """
                SELECT
                    id,
                    date_ecriture,
                    journal,
                    compte,
                    libelle,
                    debit,
                    credit,
                    source,
                    societe_id,
                    document_id,
                    precompta_id
                FROM ecritures_v3
                ORDER BY date_ecriture, id
                """
            )
        )

    rows = result.fetchall()
    session.close()

    return [
        {
            "id": row[0],
            "date_ecriture": row[1],
            "journal": row[2],
            "compte": row[3],
            "libelle": row[4],
            "debit": float(row[5]) if row[5] is not None else 0,
            "credit": float(row[6]) if row[6] is not None else 0,
            "source": row[7],
            "societe_id": row[8],
            "document_id": row[9],
            "precompta_id": row[10]
        }
        for row in rows
    ]
