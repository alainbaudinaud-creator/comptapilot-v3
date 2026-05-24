import csv
import os
import uuid
from datetime import datetime

from repositories.exports.export_repository import (
    get_ecritures_for_export
)

from services_v3.history.history_service import (
    log_action
)


EXPORT_ROOT = "/app/exports/journal_v3"


def export_journal_csv(societe_id=None):

    os.makedirs(EXPORT_ROOT, exist_ok=True)

    ecritures = get_ecritures_for_export(societe_id)

    export_id = str(uuid.uuid4())

    filename = f"journal_v3_{export_id}.csv"
    filepath = os.path.join(EXPORT_ROOT, filename)

    with open(
        filepath,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as csvfile:

        writer = csv.writer(
            csvfile,
            delimiter=";"
        )

        writer.writerow(
            [
                "EcritureID",
                "DateEcriture",
                "Journal",
                "Compte",
                "Libelle",
                "Debit",
                "Credit",
                "Source",
                "SocieteID",
                "DocumentID",
                "PrecomptaID"
            ]
        )

        for item in ecritures:
            writer.writerow(
                [
                    item.get("id"),
                    item.get("date_ecriture"),
                    item.get("journal"),
                    item.get("compte"),
                    item.get("libelle"),
                    format_amount(item.get("debit")),
                    format_amount(item.get("credit")),
                    item.get("source"),
                    item.get("societe_id"),
                    item.get("document_id"),
                    item.get("precompta_id")
                ]
            )

    log_action(
        module="exports",
        action="export_journal_csv",
        statut="ok",
        societe_id=societe_id,
        reference_type="export",
        reference_id=None,
        message="Export journal V3 généré",
        metadata={
            "filename": filename,
            "filepath": filepath,
            "count": len(ecritures)
        }
    )

    return {
        "success": True,
        "filename": filename,
        "filepath": filepath,
        "count": len(ecritures),
        "generated_at": datetime.utcnow().isoformat(),
        "message": "Export journal V3 généré"
    }


def format_amount(value):

    if value is None:
        value = 0

    return "{:.2f}".format(float(value)).replace(".", ",")
