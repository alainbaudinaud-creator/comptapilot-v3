from functools import wraps
from flask import session, redirect
from sqlalchemy import text

from services.db_postgres import get_engine


def init_permissions_if_needed(conn):

    roles = [
        "ADMIN",
        "COMPTABLE",
        "LECTURE",
        "AUDIT",
        "RGPD"
    ]

    permissions = {
        "ADMIN": [
            "ACCESS_DASHBOARD",
            "ACCESS_ECRITURES",
            "ACCESS_EXPORT",
            "ACCESS_BILAN",
            "ACCESS_JOURNAUX",
            "ACCESS_RGPD",
            "ACCESS_ADMIN"
        ],
        "COMPTABLE": [
            "ACCESS_DASHBOARD",
            "ACCESS_ECRITURES",
            "ACCESS_EXPORT",
            "ACCESS_BILAN"
        ],
        "LECTURE": [
            "ACCESS_DASHBOARD"
        ],
        "AUDIT": [
            "ACCESS_JOURNAUX"
        ],
        "RGPD": [
            "ACCESS_RGPD"
        ]
    }

    role_count = conn.execute(text("SELECT COUNT(*) FROM roles")).scalar()

    if role_count == 0:
        for role in roles:
            conn.execute(text("""
                INSERT INTO roles (nom)
                VALUES (:nom)
                ON CONFLICT (nom) DO NOTHING
            """), {"nom": role})

    permission_count = conn.execute(text("SELECT COUNT(*) FROM role_permissions")).scalar()

    if permission_count == 0:
        for role_name, perms in permissions.items():
            role_id = conn.execute(text("""
                SELECT id
                FROM roles
                WHERE nom = :nom
            """), {"nom": role_name}).scalar()

            if role_id:
                for perm in perms:
                    conn.execute(text("""
                        INSERT INTO role_permissions (role_id, permission)
                        VALUES (:role_id, :permission)
                    """), {
                        "role_id": role_id,
                        "permission": perm
                    })

    admin_role_id = conn.execute(text("""
        SELECT id
        FROM roles
        WHERE nom = 'ADMIN'
    """)).scalar()

    if admin_role_id:
        exists = conn.execute(text("""
            SELECT COUNT(*)
            FROM user_roles
            WHERE user_id = 1
            AND role_id = :role_id
        """), {
            "role_id": admin_role_id
        }).scalar()

        if exists == 0:
            conn.execute(text("""
                INSERT INTO user_roles (user_id, role_id)
                VALUES (1, :role_id)
            """), {
                "role_id": admin_role_id
            })


def user_has_permission(user_id, permission):

    if user_id == 1:
        return True

    with get_engine().begin() as conn:
        init_permissions_if_needed(conn)

        allowed = conn.execute(text("""
            SELECT COUNT(*)
            FROM role_permissions rp
            JOIN user_roles ur
                ON ur.role_id = rp.role_id
            WHERE ur.user_id = :user_id
            AND rp.permission = :permission
        """), {
            "user_id": user_id,
            "permission": permission
        }).scalar()

    return allowed > 0


def permission_required(permission):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:
                return redirect("/login")

            user_id = session["user_id"]

            if not user_has_permission(user_id, permission):
                return "Accès refusé", 403

            return f(*args, **kwargs)

        return wrapper

    return decorator


def has_permission(permission):

    user_id = session.get("user_id")

    if not user_id:
        return False

    if user_id == 1:
        return True

    with get_engine().begin() as conn:
        init_permissions_if_needed(conn)

        result = conn.execute(text("""
            SELECT COUNT(*)
            FROM user_roles ur
            JOIN role_permissions rp
                ON ur.role_id = rp.role_id
            WHERE ur.user_id = :user_id
            AND rp.permission = :permission
        """), {
            "user_id": user_id,
            "permission": permission
        }).scalar()

    return result > 0
