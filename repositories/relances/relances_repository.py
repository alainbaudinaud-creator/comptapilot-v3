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
                sent_at,
                email_to,
                email_subject,
                email_body,
                email_status
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
            "sent_at": str(row[9]) if row[9] else None,
            "email_to": row[10],
            "email_subject": row[11],
            "email_body": row[12],
            "email_status": row[13]
        }
        for row in rows
    ]


def get_relance(relance_id):

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
                email_to,
                email_subject,
                email_body,
                email_status
            FROM relances_client_v3
            WHERE id = :relance_id
            """
        ),
        {
            "relance_id": relance_id
        }
    )

    row = result.fetchone()
    session.close()

    if not row:
        return None

    return {
        "id": row[0],
        "societe_id": row[1],
        "type_relance": row[2],
        "titre": row[3],
        "message": row[4],
        "reference_type": row[5],
        "reference_id": row[6],
        "statut": row[7],
        "email_to": row[8],
        "email_subject": row[9],
        "email_body": row[10],
        "email_status": row[11]
    }


def get_societe_email(societe_id):

    if not societe_id:
        return None

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT email
            FROM societes
            WHERE id = :societe_id
            """
        ),
        {
            "societe_id": societe_id
        }
    )

    row = result.fetchone()
    session.close()

    if not row:
        return None

    return row[0]


def prepare_relance_email(
    relance_id,
    email_to,
    email_subject,
    email_body
):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE relances_client_v3
            SET
                email_to = :email_to,
                email_subject = :email_subject,
                email_body = :email_body,
                email_status = 'pret',
                statut = 'email_prepare'
            WHERE id = :relance_id
            """
        ),
        {
            "relance_id": relance_id,
            "email_to": email_to,
            "email_subject": email_subject,
            "email_body": email_body
        }
    )

    session.commit()
    session.close()


def mark_relance_sent(relance_id):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE relances_client_v3
            SET
                statut = 'envoyee',
                email_status = 'envoye',
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

