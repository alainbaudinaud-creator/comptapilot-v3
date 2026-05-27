from flask import Blueprint, render_template, request, redirect
from sqlalchemy import text
from database import engine

bp_ecritures_v3 = Blueprint("ecritures_v3", __name__)

@bp_ecritures_v3.route("/ecritures")
def ecritures():

    with engine.begin() as conn:

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ecritures (
            id SERIAL PRIMARY KEY,
            journal VARCHAR(20),
            compte VARCHAR(20),
            libelle TEXT,
            debit NUMERIC(14,2) DEFAULT 0,
            credit NUMERIC(14,2) DEFAULT 0,
            date_ecriture DATE DEFAULT CURRENT_DATE
        )
        """))

        rows = conn.execute(text("""
        SELECT
            id,
            journal,
            compte,
            libelle,
            debit,
            credit,
            date_ecriture
        FROM ecritures
        ORDER BY id DESC
        """)).fetchall()

    return render_template(
        "ecritures_v3.html",
        ecritures=rows
    )

@bp_ecritures_v3.route("/ecritures/ajouter", methods=["POST"])
def ajouter_ecriture():

    journal = request.form.get("journal")
    compte = request.form.get("compte")
    libelle = request.form.get("libelle")
    debit = request.form.get("debit") or 0
    credit = request.form.get("credit") or 0

    with engine.begin() as conn:

        conn.execute(text("""
        INSERT INTO ecritures
        (
            journal,
            compte,
            libelle,
            debit,
            credit
        )
        VALUES
        (
            :journal,
            :compte,
            :libelle,
            :debit,
            :credit
        )
        """), {
            "journal": journal,
            "compte": compte,
            "libelle": libelle,
            "debit": debit,
            "credit": credit
        })

    return redirect("/ecritures")
