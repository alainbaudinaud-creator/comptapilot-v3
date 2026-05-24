from repositories.audit.audit_repository import (
    get_audit_metrics
)


def get_audit_dashboard():

    metrics = get_audit_metrics()

    total = metrics.get("total_actions", 0)
    errors = metrics.get("error_actions", 0)

    if total > 0:
        error_rate = round(
            errors / total * 100,
            2
        )
    else:
        error_rate = 0

    health = compute_audit_health(
        total,
        error_rate
    )

    return {
        "metrics": metrics,
        "error_rate": error_rate,
        "health": health
    }


def compute_audit_health(total, error_rate):

    if total == 0:
        return {
            "status": "vide",
            "message": "Aucune action historisée pour le moment."
        }

    if error_rate >= 20:
        return {
            "status": "critique",
            "message": "Taux d'erreur élevé dans les actions historisées."
        }

    if error_rate > 0:
        return {
            "status": "attention",
            "message": "Des erreurs sont présentes dans l'historique."
        }

    return {
        "status": "ok",
        "message": "Audit V3 stable."
    }


def get_audit_comptable():

    dashboard = get_audit_dashboard()

    metrics = dashboard.get("metrics", {})

    return {
        "success": True,
        "audit": {
            "total_actions": metrics.get("total_actions", 0),
            "ok_actions": metrics.get("ok_actions", 0),
            "error_actions": metrics.get("error_actions", 0),
            "error_rate": dashboard.get("error_rate", 0),
            "health": dashboard.get("health", {})
        },
        "message": "Audit comptable V3 disponible"
    }
