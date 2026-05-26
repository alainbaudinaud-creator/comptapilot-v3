from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.backup.backup_service import (
    list_backups
)


bp_backup = Blueprint(
    "bp_backup",
    __name__
)


@bp_backup.route("/backup")
@login_required
@permission_required("ACCESS_EXPORTS")
def backup_page():

    return render_template(
        "backup_v3.html"
    )


@bp_backup.route("/api/v3/backups")
@login_required
@permission_required("ACCESS_EXPORTS")
def api_backups():

    result = list_backups()

    return jsonify(
        success_response(
            {
                "count": len(result),
                "items": result
            }
        )
    )

