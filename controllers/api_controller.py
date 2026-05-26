from flask import Blueprint
from flask import jsonify
from flask import request

from sqlalchemy import text

from database import engine

bp_api = Blueprint("api", __name__)


@bp_api.route("/api/stats")
def api_stats():

    with engine.connect() as conn:

        users = conn.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar()

        companies = conn.execute(
            text("SELECT COUNT(*) FROM companies")
        ).scalar()

        clients = conn.execute(
            text("SELECT COUNT(*) FROM clients")
        ).scalar()

        documents = conn.execute(
            text("SELECT COUNT(*) FROM documents")
        ).scalar()

    return jsonify({
        "users": users,
        "companies": companies,
        "clients": clients,
        "documents": documents
    })


@bp_api.route("/api/client/create", methods=["POST"])
def create_client():

    data = request.json

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO clients(name,email)
                VALUES(:name,:email)
            """),
            {
                "name": data["name"],
                "email": data["email"]
            }
        )

    return jsonify({"status": "ok"})


