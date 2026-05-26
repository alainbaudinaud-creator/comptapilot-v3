from services.db_postgres import get_session
from sqlalchemy import text


def list_ecritures_v3(societe_id=None):

    session = get_session()

    if societe_id:
        result = session.execute(
            text(
                """
                SELECT
                    id,
                    precompta_id,
                    document_id,
                    societe_id,
                    date_ecriture,
                    libelle,
                    compte,
                    debit,
                    credit,
                    journal,
                    source,
                    created_at
                FROM ecritures_v3
                WHERE societe_id = :societe_id
                ORDER BY created_at DESC, id DESC
                LIMIT 500
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
                    precompta_id,
                    document_id,
                    societe_id,
                    date_ecriture,
                    libelle,
                    compte,
                    debit,
                    credit,
                    journal,
                    source,
                    created_at
                FROM ecritures_v3
                ORDER BY created_at DESC, id DESC
                LIMIT 500
                """
            )
        )

    rows = result.fetchall()
    session.close()

    return [
        {
            "id": row[0],
            "precompta_id": row[1],
            "document_id": row[2],
            "societe_id": row[3],
            "date_ecriture": row[4],
            "libelle": row[5],
            "compte": row[6],
            "debit": float(row[7]) if row[7] is not None else 0,
            "credit": float(row[8]) if row[8] is not None else 0,
            "journal": row[9],
            "source": row[10],
            "created_at": str(row[11])
        }
        for row in rows
    ]


