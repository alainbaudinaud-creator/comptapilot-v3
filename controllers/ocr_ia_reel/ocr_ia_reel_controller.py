from flask import Blueprint, jsonify, redirect, render_template, request, session
from werkzeug.utils import secure_filename
from services.ocr_ia_reel_service import (
    initialiser_ocr_ia_reel,
    analyser_facture_ia,
    creer_ecriture_depuis_analyse,
)

bp_ocr_ia_reel = Blueprint("ocr_ia_reel", __name__)


@bp_ocr_ia_reel.route("/ocr-ia-reel", methods=["GET", "POST"])
def ocr_ia_reel_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_ocr_ia_reel()
    resultat = None

    if request.method == "POST":
        fichier = request.files.get("piece")

        if fichier and fichier.filename:
            nom = secure_filename(fichier.filename)
            chemin = "/app/uploads/ocr/" + nom
            fichier.save(chemin)

            analyse = analyser_facture_ia(nom, chemin)
            ecriture = creer_ecriture_depuis_analyse(analyse)

            resultat = {
                "analyse": analyse,
                "ecriture": ecriture,
            }

    return render_template("ocr_ia_reel_v3.html", resultat=resultat)


@bp_ocr_ia_reel.route("/api/v3/ocr-ia/demo")
def api_ocr_ia_demo():

    try:
        initialiser_ocr_ia_reel()

        analyse = analyser_facture_ia(
            "facture_demo.txt",
            "/app/uploads/ocr/facture_demo.txt",
        )

        ecriture = creer_ecriture_depuis_analyse(analyse)

        return jsonify({
            "success": True,
            "analyse": analyse,
            "ecriture": ecriture,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

