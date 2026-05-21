from functools import wraps
from flask import session, redirect
import sqlite3


def user_has_permission(user_id, permission):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    # ADMIN TOTAL
    if user_id == 1:
        conn.close()
        return True

    c.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS role_permissions (
            role_id INTEGER,
            permission TEXT
        )
    """)

    c.execute("""
        SELECT COUNT(*)
        FROM roles
    """)

    if c.fetchone()[0] == 0:

        roles = [
            "ADMIN",
            "COMPTABLE",
            "LECTURE",
            "AUDIT",
            "RGPD"
        ]

        for role in roles:
            c.execute(
                "INSERT INTO roles (nom) VALUES (?)",
                (role,)
            )

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

        for role_name, perms in permissions.items():

            c.execute(
                "SELECT id FROM roles WHERE nom=?",
                (role_name,)
            )

            role_id = c.fetchone()[0]

            for perm in perms:

                c.execute("""
                    INSERT INTO role_permissions (
                        role_id,
                        permission
                    )
                    VALUES (?, ?)
                """, (role_id, perm))

        # USER 1 = ADMIN

        c.execute("""
            SELECT id
            FROM roles
            WHERE nom='ADMIN'
        """)

        admin_role_id = c.fetchone()[0]

        c.execute("""
            INSERT INTO user_roles (
                user_id,
                role_id
            )
            VALUES (?, ?)
        """, (1, admin_role_id))

        conn.commit()

    c.execute("""
        SELECT COUNT(*)
        FROM role_permissions rp
        JOIN user_roles ur
            ON ur.role_id = rp.role_id
        WHERE ur.user_id = ?
        AND rp.permission = ?
    """, (user_id, permission))

    allowed = c.fetchone()[0] > 0

    conn.close()

    return allowed


def permission_required(permission):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:
                return redirect("/auth/login")

            user_id = session["user_id"]

            if not user_has_permission(user_id, permission):
                return "Accès refusé", 403

            return f(*args, **kwargs)

        return wrapper

    return decorator
def has_permission(permission):

    from flask import session
    import sqlite3

    user_id = session.get("user_id")

    if not user_id:
        return False

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT COUNT(*)
        FROM user_roles ur
        JOIN role_permissions rp
            ON ur.role_id = rp.role_id
        WHERE ur.user_id = ?
        AND rp.permission = ?
    """, (user_id, permission))

    result = c.fetchone()[0]

    conn.close()

    return result > 0
