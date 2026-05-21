from flask import Blueprint, render_template, request, redirect
from sqlalchemy import text

from extensions import db
from services.permission_service import permission_required

registre_rgpd_routes = Blueprint(
    "registre_rgpd_routes",
    __name__
)


@registre_rgpd_routes.route("/rgpd/registre")
def registre_rgpd():

    with db.engine.connect() as conn:

        traitements = conn.execute(
            text("""
                SELECT *
                FROM registre_traitements_rgpd
                ORDER BY id DESC
            """)
        ).mappings().all()

    return render_template(
        "registre_rgpd.html",
        traitements=traitements
    )


@registre_rgpd_routes.route(
    "/rgpd/registre/ajouter",
    methods=["GET", "POST"]
)
def ajouter_traitement_rgpd():

    if request.method == "POST":

        nom_traitement = request.form["nom_traitement"]
        finalite = request.form["finalite"]
        base_legale = request.form["base_legale"]
        duree_conservation = request.form["duree_conservation"]
        responsable = request.form["responsable"]

        with db.engine.begin() as conn:

            conn.execute(
                text("""
                    INSERT INTO registre_traitements_rgpd (
                        nom_traitement,
                        finalite,
                        base_legale,
                        duree_conservation,
                        responsable
                    )
                    VALUES (
                        :nom_traitement,
                        :finalite,
                        :base_legale,
                        :duree_conservation,
                        :responsable
                    )
                """),
                {
                    "nom_traitement": nom_traitement,
                    "finalite": finalite,
                    "base_legale": base_legale,
                    "duree_conservation": duree_conservation,
                    "responsable": responsable
                }
            )

        return redirect("/rgpd/registre")

    return render_template(
        "ajouter_traitement_rgpd.html"
    )

