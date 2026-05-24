from services.db_postgres import get_session
from sqlalchemy import text


def list_roles():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT code, label, description
            FROM roles_v3
            ORDER BY code
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "code": row[0],
            "label": row[1],
            "description": row[2]
        }
        for row in rows
    ]


def list_permissions():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT code, label, module
            FROM permissions_v3
            ORDER BY module, code
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "code": row[0],
            "label": row[1],
            "module": row[2]
        }
        for row in rows
    ]


def list_role_permissions():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT role_code, permission_code
            FROM role_permissions_v3
            ORDER BY role_code, permission_code
            """
        )
    )

    rows = result.fetchall()
    session.close()

    return [
        {
            "role_code": row[0],
            "permission_code": row[1]
        }
        for row in rows
    ]
