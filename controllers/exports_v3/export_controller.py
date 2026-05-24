from flask import Blueprint
from flask import request
from flask import jsonify
from flask import send_file

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.exports.export_service import (
    export_journal_csv
)


bp_exports_v3 = Blueprint(
    "bp_exports_v3",
    __name__
)


@bp_exports_v3.route(
    "/api/v3/exports/journal",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_export_journal():

    data = request.json or {}

    societe_id = data.get("societe_id")

    result = export_journal_csv(societe_id)

    return jsonify(
        success_response(result)
    )


@bp_exports_v3.route(
    "/api/v3/exports/journal/download"
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_download_journal_export():

    filepath = request.args.get("filepath")

    if not filepath:
        return jsonify(
            success_response(
                {
                    "success": False,
                    "message": "Chemin fichier manquant"
                }
            )
        )

    return send_file(
        filepath,
        as_attachment=True
    )
