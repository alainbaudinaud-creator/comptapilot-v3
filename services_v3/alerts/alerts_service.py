from repositories.alerts.alerts_repository import (
    get_alerts_raw_data
)


def get_alerts_center():

    raw = get_alerts_raw_data()

    alerts = []

    for row in raw.get("ocr_errors", []):
        alerts.append(
            {
                "level": "critique",
                "type": "ocr_erreur",
                "title": "Erreur OCR",
                "message": f"Le document {row[2]} est en erreur OCR.",
                "societe_id": row[1],
                "reference_id": row[0],
                "created_at": str(row[4]),
                "action": "Relancer OCR ou contrôler le fichier"
            }
        )

    for row in raw.get("ocr_pending", []):
        alerts.append(
            {
                "level": "normal",
                "type": "ocr_en_attente",
                "title": "OCR en attente",
                "message": f"Le document {row[2]} attend un traitement OCR.",
                "societe_id": row[1],
                "reference_id": row[0],
                "created_at": str(row[3]),
                "action": "Lancer OCR"
            }
        )

    for row in raw.get("precompta_pending", []):
        alerts.append(
            {
                "level": "important",
                "type": "precompta_a_valider",
                "title": "Précompta à valider",
                "message": f"La précompta fournisseur {row[3] or 'à vérifier'} est en attente.",
                "societe_id": row[2],
                "reference_id": row[0],
                "created_at": str(row[5]),
                "action": "Valider ou rejeter"
            }
        )

    for row in raw.get("precompta_rejected", []):
        alerts.append(
            {
                "level": "important",
                "type": "precompta_rejetee",
                "title": "Précompta rejetée",
                "message": f"La précompta {row[0]} a été rejetée.",
                "societe_id": row[2],
                "reference_id": row[0],
                "created_at": str(row[5]),
                "action": "Corriger extraction ou document"
            }
        )

    alerts = sorted(
        alerts,
        key=lambda item: item.get("created_at") or "",
        reverse=True
    )

    return {
        "count": len(alerts),
        "critical_count": len(
            [
                item for item in alerts
                if item.get("level") == "critique"
            ]
        ),
        "important_count": len(
            [
                item for item in alerts
                if item.get("level") == "important"
            ]
        ),
        "normal_count": len(
            [
                item for item in alerts
                if item.get("level") == "normal"
            ]
        ),
        "items": alerts[:100]
    }
