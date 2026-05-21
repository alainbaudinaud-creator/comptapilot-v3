import json
import os
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy import text

from extensions import db
from services.permission_service import permission_required

rgpd_routes = Blueprint("rgpd_routes", __name__)


def log_rgpd(action, user_id, details):
    with db.engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO rgpd_logs (action, user_id, details)
            VALUES (:action, :user_id, :details)
        """), {
            "action": action,
            "user_id": user_id,
            "details": details
        })


def fetch_all(conn, query, params=None):
    result = conn.execute(text(query), params or {}).mappings().all()
    return [dict(row) for row in result]


@rgpd_routes.route("/rgpd/export/<int:user_id>")
def export_rgpd(user_id):
    try:
        with db.engine.connect() as conn:
            export_data = {
                "generated_at": datetime.now().isoformat(),
                "user_id": user_id,
                "user": fetch_all(
                    conn,
                    "SELECT id, username FROM users WHERE id = :user_id",
                    {"user_id": user_id}
                ),
                "audit_log": fetch_all(
                    conn,
                    "SELECT * FROM audit_log LIMIT 500"
                ),
                "journal_acces": fetch_all(
                    conn,
                    "SELECT * FROM journal_acces_v6 LIMIT 500"
                ),
                "factures": fetch_all(
                    conn,
                    "SELECT * FROM factures LIMIT 500"
                ),
                "clients": fetch_all(
                    conn,
                    "SELECT * FROM clients LIMIT 500"
                ),
                "ecritures": fetch_all(
                    conn,
                    "SELECT * FROM ecritures LIMIT 500"
                ),
                "documents_comptables_importes": fetch_all(
                    conn,
                    "SELECT * FROM documents_comptables_importes LIMIT 500"
                )
            }

        export_dir = "C:/Users/alain/mon-projet-agent/exports/rgpd"
        os.makedirs(export_dir, exist_ok=True)

        export_path = f"{export_dir}/user_{user_id}_export_rgpd.json"

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=4, ensure_ascii=False, default=str)

        log_rgpd("EXPORT_COMPLET", user_id, export_path)

        return {
            "status": "ok",
            "file": export_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
@rgpd_routes.route("/rgpd/delete/<int:user_id>")
def delete_rgpd_user(user_id):

    try:

        with db.engine.begin() as conn:

            conn.execute(text("""
                UPDATE users
                SET
                    username = :username,
                    password = :password
                WHERE id = :user_id
            """), {
                "username": f"utilisateur_supprime_{user_id}",
                "password": "SUPPRIME_RGPD",
                "user_id": user_id
            })

        log_rgpd(
            "SUPPRESSION_RGPD",
            user_id,
            f"Utilisateur {user_id} anonymisé"
        )

        return {
            "status": "ok",
            "message": f"Utilisateur {user_id} anonymisé"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }, 500
@rgpd_routes.route("/rgpd/anonymiser/<int:user_id>")
def anonymiser_comptabilite(user_id):

    try:

        with db.engine.begin() as conn:

            conn.execute(text("""
                UPDATE clients
                SET
                    nom = :nom
            """), {
                "nom": f"CLIENT_ANONYMISE_{user_id}"
            })

            conn.execute(text("""
                UPDATE factures
                SET
                    client = :nom
            """), {
                "nom": f"CLIENT_ANONYMISE_{user_id}"
            })

            conn.execute(text("""
                UPDATE ecritures
                SET
                    libelle = :libelle
            """), {
                "libelle": f"ECRITURE_ANONYMISEE_{user_id}"
            })

        log_rgpd(
            "ANONYMISATION_COMPTABLE",
            user_id,
            f"Comptabilité anonymisée pour utilisateur {user_id}"
        )

        return {
            "status": "ok",
            "message": f"Comptabilité anonymisée pour utilisateur {user_id}"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }, 500
@rgpd_routes.route("/rgpd/cookies/accept")
def accept_cookies():

    try:

        ip = request.remote_addr

        with db.engine.begin() as conn:

            conn.execute(text("""
                INSERT INTO consentements_cookies (
                    ip,
                    consentement
                )
                VALUES (
                    :ip,
                    :consentement
                )
            """), {
                "ip": ip,
                "consentement": "ACCEPTE"
            })

        log_rgpd(
            "CONSENTEMENT_COOKIES",
            None,
            f"Cookies acceptés depuis IP {ip}"
        )

        return {
            "status": "ok",
            "message": "Consentement cookies enregistré"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }, 500

