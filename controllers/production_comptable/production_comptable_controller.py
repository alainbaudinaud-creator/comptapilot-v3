from flask import Blueprint, redirect, render_template, request, session, flash
from werkzeug.utils import secure_filename
from sqlalchemy import text
from database import engine
from services.production_comptable_service import (
    enregistrer_piece,
    analyser_piece_ia,
    generer_pre_ecriture,
)

bp_production_comptable = Blueprint("production_comptable", __name__)


@bp_production_comptable.route("/production-comptable", methods=["GET", "POST"])
def production_comptable_index():

    if not session.get("user_id"):
        return redirect("/login")

    resultat = None

    if request.method == "POST":

        fichier = request.files.get("piece")

        if fichier and fichier.filename:

            nom_fichier = secure_filename(fichier.filename)

            chemin = f"uploads/{nom_fichier}"

            fichier.save(chemin)

            piece_id = enregistrer_piece(
                client_id=1,
                nom_fichier=nom_fichier,
                chemin_stockage=chemin,
            )

            analyse = analyser_piece_ia(
                piece_id=piece_id,
                chemin_piece=chemin,
            )

            ecriture = generer_pre_ecriture(
                client_id=1,
                analyse=analyse,
            )

            resultat = {
                "piece_id": piece_id,
                "analyse": analyse,
                "ecriture": ecriture,
            }

            flash("Pièce analysée avec succès.", "success")

    stats = {}

    with engine.connect() as conn:

        tables = {
            "pieces": "pieces_v3",
            "factures": "factures_v3",
            "ecritures": "ecritures_v3",
            "lignes": "lignes_ecritures_v3",
        }

        for label, table in tables.items():

            try:
                stats[label] = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table}")
                ).scalar() or 0

            except Exception:
                stats[label] = 0

    return render_template(
        "production_comptable_v3.html",
        resultat=resultat,
        stats=stats,
    )
