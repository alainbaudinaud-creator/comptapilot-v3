
import sqlite3
from pathlib import Path
from flask import Blueprint, render_template, redirect, url_for

from services.veille_reglementaire_service import (
    verifier_et_telecharger,
    remplir_liasse_depuis_comptabilite
)

bp_veille_reglementaire = Blueprint("veille_reglementaire", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_veille_reglementaire.route("/reglementaire")
def reglementaire():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    try:
        veille = cur.execute("""
            SELECT code, type_document, millesime, description, statut, derniere_verification
            FROM veille_reglementaire
            ORDER BY id DESC
            LIMIT 30
        """).fetchall()
    except Exception:
        veille = []

    try:
        obligations = cur.execute("""
            SELECT code, libelle, regime, periodicite, source
            FROM obligations_fiscales
            WHERE actif=1
            ORDER BY code
        """).fetchall()
    except Exception:
        obligations = []

    try:
        liasse = cur.execute("""
            SELECT formulaire, case_fiscale, valeur
            FROM liasse_fiscale
            ORDER BY formulaire, case_fiscale
        """).fetchall()
    except Exception:
        liasse = []

    con.close()

    return render_template(
        "reglementaire/index.html",
        veille=veille,
        obligations=obligations,
        liasse=liasse
    )

@bp_veille_reglementaire.route("/reglementaire/actualiser")
def actualiser_reglementaire():
    verifier_et_telecharger()
    return redirect(url_for("veille_reglementaire.reglementaire"))

@bp_veille_reglementaire.route("/reglementaire/remplir-liasse")
def remplir_liasse():
    remplir_liasse_depuis_comptabilite("2026", "RSI")
    return redirect(url_for("veille_reglementaire.reglementaire"))
