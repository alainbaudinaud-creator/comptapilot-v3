from flask import Blueprint, render_template

from controllers.auth import login_required
from services.audit_service import lister_logs
from services.permission_service import permission_required


audit_routes = Blueprint("audit", __name__)


@audit_routes.route("/journal-audit")
@login_required
@permission_required("ACCESS_JOURNAUX")
def journal_audit():

    logs = lister_logs()

    return render_template(
        "journal_audit.html",
        logs=logs
    )

