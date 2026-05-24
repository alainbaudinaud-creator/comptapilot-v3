from services.db_postgres import get_session
from sqlalchemy import text


def list_societes_summary():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                nom,
                siren,
                email
            FROM societes
            ORDER BY id
            LIMIT 200
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "societe_id": row[0],
            "nom": row[1],
            "siren": row[2],
            "email": row[3]
        }
        for row in rows
    ]


def get_societe_object_counts():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                s.id,
                s.nom,
                COALESCE(d.documents_count, 0) AS documents_count,
                COALESCE(p.precompta_count, 0) AS precompta_count,
                COALESCE(e.ecritures_count, 0) AS ecritures_count,
                COALESCE(r.relances_count, 0) AS relances_count
            FROM societes s
            LEFT JOIN (
                SELECT societe_id, COUNT(*) AS documents_count
                FROM documents
                GROUP BY societe_id
            ) d ON d.societe_id = s.id
            LEFT JOIN (
                SELECT societe_id, COUNT(*) AS precompta_count
                FROM precompta_documents
                GROUP BY societe_id
            ) p ON p.societe_id = s.id
            LEFT JOIN (
                SELECT societe_id, COUNT(*) AS ecritures_count
                FROM ecritures_v3
                GROUP BY societe_id
            ) e ON e.societe_id = s.id
            LEFT JOIN (
                SELECT societe_id, COUNT(*) AS relances_count
                FROM relances_client_v3
                GROUP BY societe_id
            ) r ON r.societe_id = s.id
            ORDER BY s.id
            LIMIT 200
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "societe_id": row[0],
            "nom": row[1],
            "documents_count": row[2],
            "precompta_count": row[3],
            "ecritures_count": row[4],
            "relances_count": row[5]
        }
        for row in rows
    ]


def list_user_societe_access():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                user_id,
                user_email,
                societe_id,
                role_code,
                created_at
            FROM user_societe_access_v3
            ORDER BY created_at DESC
            LIMIT 200
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "id": row[0],
            "user_id": row[1],
            "user_email": row[2],
            "societe_id": row[3],
            "role_code": row[4],
            "created_at": str(row[5])
        }
        for row in rows
    ]
