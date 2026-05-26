from sqlalchemy import text

from database import engine


def fetch_user_by_username(username: str):

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT id, username, password
            FROM users
            WHERE username = :username
            LIMIT 1
        """), {
            "username": username
        })

        return result.fetchone()


def fetch_users_with_roles():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                u.id,
                u.username,
                COALESCE(r.nom, 'AUCUN') AS role
            FROM users u
            LEFT JOIN user_roles ur
                ON u.id = ur.user_id
            LEFT JOIN roles r
                ON ur.role_id = r.id
            ORDER BY u.id
        """))

        return result.fetchall()


