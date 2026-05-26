from flask import Blueprint
from flask import render_template

from sqlalchemy import text

from database import engine

bp_enterprise = Blueprint("enterprise", __name__)


@bp_enterprise.route("/enterprise")
def enterprise():

    stats = {
        "users": 0,
        "companies": 0,
        "clients": 0,
        "documents": 0,
        "scheduler_jobs": 0,
        "postgresql": 1,
        "saas": 1
    }

    with engine.connect() as conn:

        stats["users"] = conn.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar() or 0

        stats["companies"] = conn.execute(
            text("SELECT COUNT(*) FROM companies")
        ).scalar() or 0

        stats["clients"] = conn.execute(
            text("SELECT COUNT(*) FROM clients")
        ).scalar() or 0

        stats["documents"] = conn.execute(
            text("SELECT COUNT(*) FROM documents")
        ).scalar() or 0

        stats["scheduler_jobs"] = conn.execute(
            text("SELECT COUNT(*) FROM scheduler_jobs")
        ).scalar() or 0

    return render_template(
        "cabinet/enterprise.html",
        stats=stats
    )


