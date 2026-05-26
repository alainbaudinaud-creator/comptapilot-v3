from pathlib import Path
from datetime import datetime

from database import engine
from sqlalchemy import text


CRITICAL_PATHS = [
    "/app/uploads",
    "/app/exports",
    "/app/backups"
]


def get_system_health():

    db_status = check_database()
    paths_status = check_paths()

    overall_status = "ok"

    if db_status.get("status") != "ok":
        overall_status = "critique"

    if any(item.get("status") != "ok" for item in paths_status):
        overall_status = "attention"

    return {
        "status": overall_status,
        "checked_at": datetime.utcnow().isoformat(),
        "database": db_status,
        "paths": paths_status,
        "metrics": get_basic_metrics()
    }


def check_database():

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1")
            ).scalar()

        return {
            "status": "ok",
            "message": "PostgreSQL accessible",
            "result": result
        }

    except Exception as exc:
        return {
            "status": "critique",
            "message": str(exc)
        }


def check_paths():

    results = []

    for path in CRITICAL_PATHS:
        p = Path(path)

        results.append(
            {
                "path": path,
                "exists": p.exists(),
                "status": "ok" if p.exists() else "manquant"
            }
        )

    return results


def get_basic_metrics():

    metrics = {}

    try:
        with engine.connect() as conn:
            metrics["documents"] = conn.execute(
                text("SELECT COUNT(*) FROM documents")
            ).scalar() or 0

            metrics["precompta"] = conn.execute(
                text("SELECT COUNT(*) FROM precompta_documents")
            ).scalar() or 0

            metrics["ecritures"] = conn.execute(
                text("SELECT COUNT(*) FROM ecritures_v3")
            ).scalar() or 0

            metrics["history"] = conn.execute(
                text("SELECT COUNT(*) FROM actions_history_v3")
            ).scalar() or 0

    except Exception:
        metrics["error"] = "metrics_unavailable"

    return metrics

