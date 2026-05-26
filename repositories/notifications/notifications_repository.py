from services.db_postgres import get_session
from sqlalchemy import text


def create_notification(data):

    session = get_session()

    result = session.execute(
        text(
            """
            INSERT INTO notifications_v3 (
                societe_id,
                type_notification,
                niveau,
                titre,
                message,
                reference_type,
                reference_id,
                statut
            )
            VALUES (
                :societe_id,
                :type_notification,
                :niveau,
                :titre,
                :message,
                :reference_type,
                :reference_id,
                'non_lue'
            )
            RETURNING id
            """
        ),
        data
    )

    notification_id = result.fetchone()[0]

    session.commit()
    session.close()

    return notification_id


def list_notifications(limit=100):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                societe_id,
                type_notification,
                niveau,
                titre,
                message,
                reference_type,
                reference_id,
                statut,
                created_at,
                read_at
            FROM notifications_v3
            ORDER BY created_at DESC
            LIMIT :limit
            """
        ),
        {
            "limit": limit
        }
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "id": row[0],
            "societe_id": row[1],
            "type_notification": row[2],
            "niveau": row[3],
            "titre": row[4],
            "message": row[5],
            "reference_type": row[6],
            "reference_id": row[7],
            "statut": row[8],
            "created_at": str(row[9]),
            "read_at": str(row[10]) if row[10] else None
        }
        for row in rows
    ]


def mark_notification_as_read(notification_id):

    session = get_session()

    session.execute(
        text(
            """
            UPDATE notifications_v3
            SET
                statut = 'lue',
                read_at = CURRENT_TIMESTAMP
            WHERE id = :notification_id
            """
        ),
        {
            "notification_id": notification_id
        }
    )

    session.commit()
    session.close()


def count_unread_notifications():

    session = get_session()

    count = session.execute(
        text(
            """
            SELECT COUNT(*)
            FROM notifications_v3
            WHERE statut = 'non_lue'
            """
        )
    ).scalar() or 0

    session.close()

    return count

