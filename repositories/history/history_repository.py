from services.db_postgres import get_session
from sqlalchemy import text


def create_history_entry(data):

    session = get_session()

    result = session.execute(
        text(
            """
            INSERT INTO actions_history_v3 (
                module,
                action,
                statut,
                societe_id,
                reference_type,
                reference_id,
                message,
                metadata,
                created_by
            )
            VALUES (
                :module,
                :action,
                :statut,
                :societe_id,
                :reference_type,
                :reference_id,
                :message,
                :metadata,
                :created_by
            )
            RETURNING id
            """
        ),
        data
    )

    history_id = result.fetchone()[0]

    session.commit()
    session.close()

    return history_id


def list_history(limit=200):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                module,
                action,
                statut,
                societe_id,
                reference_type,
                reference_id,
                message,
                metadata,
                created_by,
                created_at
            FROM actions_history_v3
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
            "module": row[1],
            "action": row[2],
            "statut": row[3],
            "societe_id": row[4],
            "reference_type": row[5],
            "reference_id": row[6],
            "message": row[7],
            "metadata": row[8],
            "created_by": row[9],
            "created_at": str(row[10])
        }
        for row in rows
    ]

