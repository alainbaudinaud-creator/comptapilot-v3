from repositories.production.production_repository import (
    get_production_metrics,
    get_recent_production_items
)


def get_production_dashboard():

    metrics = get_production_metrics()
    recent_items = get_recent_production_items()

    documents_total = metrics.get(
        "documents_total",
        0
    )

    if documents_total > 0:

        ocr_success_rate = round(
            (
                metrics.get("ocr_termine", 0)
                / documents_total
            ) * 100,
            2
        )

    else:

        ocr_success_rate = 0

    return {
        "metrics": metrics,
        "ocr_success_rate": ocr_success_rate,
        "recent_items": recent_items,
        "health": compute_production_health(metrics)
    }


def compute_production_health(metrics):

    if metrics.get("ocr_erreur", 0) > 0:

        return {
            "status": "attention",
            "message": "Des erreurs OCR nécessitent un contrôle."
        }

    if metrics.get("precompta_a_valider", 0) > 0:

        return {
            "status": "a_traiter",
            "message": "Des précomptas sont en attente de validation."
        }

    return {
        "status": "ok",
        "message": "Production cabinet stable."
    }
