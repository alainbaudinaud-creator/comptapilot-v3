from flask import Blueprint, render_template
from sqlalchemy import text

from controllers.auth import login_required
from services.permission_service import permission_required
from services.db_postgres import get_engine


admin_users_routes = Blueprint("admin_users_routes", __name__)


@admin_users_routes.route("/admin/users")
@login_required
@permission_required("ACCESS_ADMIN")
def admin_users():

    with get_engine().begin() as conn:
        users = conn.execute(text("""
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
        """)).fetchall()

    return render_template(
        "admin_users.html",
        users=users
    )

