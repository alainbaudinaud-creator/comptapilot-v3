from services.db_postgres import get_session
from sqlalchemy import text


def get_audit_metrics():

    session = get_session()

    total_actions = session.execute(
        text("SELECT COUNT(*) FROM actions_history_v3")
    ).scalar() or 0

    error_actions = session.execute(
        text("SELECT COUNT(*) FROM actions_history_v3 WHERE statut = 'erreur'")
    ).scalar() or 0

    ok_actions = session.execute(
        text("SELECT COUNT(*) FROM actions_history_v3 WHERE statut = 'ok'")
    ).scalar() or 0

    modules_result = session.execute(
        text(
            """
            SELECT module, COUNT(*)
            FROM actions_history_v3
            GROUP BY module
            ORDER BY COUNT(*) DESC
            """
        )
    ).fetchall()

    status_result = session.execute(
        text(
            """
            SELECT statut, COUNT(*)
            FROM actions_history_v3
            GROUP BY statut
            ORDER BY COUNT(*) DESC
            """
        )
    ).fetchall()

    recent_errors_result = session.execute(
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
                created_at
            FROM actions_history_v3
            WHERE statut = 'erreur'
            ORDER BY created_at DESC
            LIMIT 20
            """
        )
    ).fetchall()

    recent_actions_result = session.execute(
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
                created_at
            FROM actions_history_v3
            ORDER BY created_at DESC
            LIMIT 30
            """
        )
    ).fetchall()

    session.close()

    return {
        "total_actions": total_actions,
        "ok_actions": ok_actions,
        "error_actions": error_actions,
        "modules": [
            {
                "module": row[0],
                "count": row[1]
            }
            for row in modules_result
        ],
        "statuses": [
            {
                "statut": row[0],
                "count": row[1]
            }
            for row in status_result
        ],
        "recent_errors": [
            row_to_action(row)
            for row in recent_errors_result
        ],
        "recent_actions": [
            row_to_action(row)
            for row in recent_actions_result
        ]
    }


def row_to_action(row):

    return {
        "id": row[0],
        "module": row[1],
        "action": row[2],
        "statut": row[3],
        "societe_id": row[4],
        "reference_type": row[5],
        "reference_id": row[6],
        "message": row[7],
        "created_at": str(row[8])
    }


