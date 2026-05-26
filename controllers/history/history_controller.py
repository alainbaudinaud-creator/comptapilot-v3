from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.history.history_service import (
    get_history_dashboard
)


bp_history = Blueprint(
    "bp_history",
    __name__
)


@bp_history.route("/history")
@login_required
@permission_required("ACCESS_ECRITURES")
def history_page():

    return render_template(
        "history_v3.html"
    )


@bp_history.route("/api/v3/history")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_history():

    result = get_history_dashboard()

    return jsonify(
        success_response(result)
    )

