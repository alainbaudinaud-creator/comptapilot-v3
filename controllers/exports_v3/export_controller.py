import os
import csv
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import send_file
from flask import render_template

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.exports.export_service import (
    export_journal_csv
)

from repositories.exports.export_repository import (
    get_ecritures_for_export
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


@bp_exports_v3.route("/fec")
@login_required
@permission_required("ACCESS_EXPORTS")
def fec_page():

    return render_template(
        "fec_v3.html"
    )


@bp_exports_v3.route(
    "/api/v3/fec/export",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_EXPORTS")
def api_export_fec():

    data = request.json or {}
    societe_id = data.get("societe_id")

    export_root = "/app/exports/fec"
    os.makedirs(export_root, exist_ok=True)

    ecritures = get_ecritures_for_export(societe_id)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"FEC_V3_{societe_id or 'ALL'}_{timestamp}.txt"
    filepath = os.path.join(export_root, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file, delimiter="|")

        writer.writerow(
            [
                "JournalCode",
                "JournalLib",
                "EcritureNum",
                "EcritureDate",
                "CompteNum",
                "CompteLib",
                "CompAuxNum",
                "CompAuxLib",
                "PieceRef",
                "PieceDate",
                "EcritureLib",
                "Debit",
                "Credit",
                "EcritureLet",
                "DateLet",
                "ValidDate",
                "Montantdevise",
                "Idevise"
            ]
        )

        index = 1

        for item in ecritures:

            date_ecriture = str(
                item.get("date_ecriture") or ""
            ).replace("-", "")[:8]

            writer.writerow(
                [
                    item.get("journal") or "AC",
                    item.get("journal") or "ACHATS",
                    index,
                    date_ecriture,
                    item.get("compte") or "",
                    item.get("libelle") or "",
                    "",
                    "",
                    "",
                    date_ecriture,
                    item.get("libelle") or "",
                    format_amount(item.get("debit")),
                    format_amount(item.get("credit")),
                    "",
                    "",
                    date_ecriture,
                    "",
                    "EUR"
                ]
            )

            index += 1

    return jsonify(
        success_response(
            {
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "count": len(ecritures),
                "message": "Export FEC DGFIP généré"
            }
        )
    )


def format_amount(value):

    if value is None:
        value = 0

    return "{:.2f}".format(float(value)).replace(".", ",")


