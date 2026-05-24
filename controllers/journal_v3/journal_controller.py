from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.journal.journal_service import (
    get_journal_dashboard
)


bp_journal_v3 = Blueprint(
    "bp_journal_v3",
    __name__
)


@bp_journal_v3.route("/journal-v3")
@login_required
@permission_required("ACCESS_ECRITURES")
def journal_v3_page():

    return render_template(
        "journal_v3.html"
    )


@bp_journal_v3.route("/api/v3/journal")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_journal_v3():

    societe_id = request.args.get("societe_id")

    result = get_journal_dashboard(societe_id)

    return jsonify(
        success_response(result)
    )
