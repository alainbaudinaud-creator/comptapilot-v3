from flask import Blueprint, render_template
import sqlite3

from controllers.auth import login_required
from services.permission_service import permission_required


admin_users_routes = Blueprint("admin_users_routes", __name__)


@admin_users_routes.route("/admin/users")
@login_required
@permission_required("ACCESS_ADMIN")
def admin_users():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            u.id,
            u.username,
            COALESCE(r.nom, 'AUCUN')
        FROM users u
        LEFT JOIN user_roles ur
            ON u.id = ur.user_id
        LEFT JOIN roles r
            ON ur.role_id = r.id
        ORDER BY u.id
    """)

    users = c.fetchall()

    conn.close()

    return render_template(
        "admin_users.html",
        users=users
    )
