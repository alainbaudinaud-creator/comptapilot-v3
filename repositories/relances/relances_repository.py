from services.db_postgres import get_session
from sqlalchemy import text


def create_relance(data):

    session = get_session()

    result = session.execute(
        text(
            """
            INSERT INTO relances_client_v3 (
                societe_id,
                type_relance,
                titre,
                message,
                reference_type,
                reference_id,
                statut
            )
            VALUES (
                :societe_id,
                :type_relance,
                :titre,
                :message,
                :reference_type,
                :reference_id,
                'brouillon'
            )
            RETURNING id
            """
        ),
        data
    )

    relance_id = result.fetchone()[0]

    session.commit()
    session.close()

    return relance_id


def list_relances():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                societe_id,
                type_relance,
                titre,
                message,
                reference_type,
                reference_id,
                statut,
                created_at,
                sent_at
            FROM relances_client_v3
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
            "societe_id": row[1],
            "type_relance": row[2],
            "titre": row[3],
            "message": row[4],
            "reference_type": row[5],
            "reference_id": row[6],
            "statut": row[7],
            "created_at": str(row[8]),
            "sent_at": str(row[9]) if row[9] else None
        }
        for row in rows
    ]


def mark_relance_sent(relance_id):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE relances_client_v3
            SET
                statut = 'envoyee',
                sent_at = CURRENT_TIMESTAMP
            WHERE id = :relance_id
            """
        ),
        {
            "relance_id": relance_id
        }
    )

    session.commit()
    session.close()
