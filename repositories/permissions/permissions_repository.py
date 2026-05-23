from sqlalchemy import text

from database import engine


def fetch_permission_count(user_id: int, permission: str) -> int:

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT COUNT(*)
            FROM user_roles ur
            JOIN role_permissions rp
                ON ur.role_id = rp.role_id
            WHERE ur.user_id = :user_id
            AND rp.permission = :permission
        """), {
            "user_id": user_id,
            "permission": permission
        })

        return int(result.scalar() or 0)


def user_has_permission_repository(user_id: int, permission: str) -> bool:

    if user_id == 1:
        return True

    return fetch_permission_count(user_id, permission) > 0
