from flask import Blueprint, redirect, render_template, session, jsonify
from sqlalchemy import text
from database import engine

bp_rapprochement_bancaire = Blueprint("rapprochement_bancaire", __name__)


@bp_rapprochement_bancaire.route("/rapprochement-bancaire")
def rapprochement_bancaire_index():

    if not session.get("user_id") and not session.get("user"):
        return redirect("/login")

    return render_template("rapprochement_bancaire_v3.html")


@bp_rapprochement_bancaire.route("/api/rapprochements-bancaires")
def api_rapprochements_bancaires():

    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT
                r.id,
                r.date_operation,
                r.libelle,
                r.montant,
                r.rapproche,
                s.nom AS societe
            FROM rapprochements_bancaires r
            LEFT JOIN societes_clientes_premium s ON s.id = r.societe_id
            ORDER BY r.date_operation DESC, r.id DESC
            LIMIT 100
        """)).mappings().all()

    return jsonify([
        {
            "id": r["id"],
            "date_operation": str(r["date_operation"]),
            "libelle": r["libelle"],
            "montant": float(r["montant"] or 0),
            "rapproche": bool(r["rapproche"]),
            "societe": r["societe"],
        }
        for r in rows
    ])
