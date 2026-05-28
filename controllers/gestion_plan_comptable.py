from flask import Blueprint, request, jsonify, render_template, Response, redirect
from controllers.auth import login_required
from services.permission_service import permission_required
from sqlalchemy import text
from database import engine
import csv
import io

plan_comptable_routes = Blueprint("plan_comptable", __name__)


@plan_comptable_routes.route("/ui")
@login_required
@permission_required("ACCESS_ADMIN")
def ui():
    return render_template("plan_comptable.html")


@plan_comptable_routes.route("/", methods=["GET"])
@login_required
@permission_required("ACCESS_ADMIN")
def get_plan_comptable():
    societe_id = request.args.get("societe_id")

    if societe_id:
        sql = """
            SELECT id, numero, libelle, type
            FROM plan_comptable
            WHERE societe_id = :societe_id
            ORDER BY numero
        """
        params = {"societe_id": societe_id}
    else:
        sql = """
            SELECT id, numero, libelle, type
            FROM plan_comptable
            ORDER BY societe_id NULLS FIRST, numero
        """
        params = {}

    with engine.begin() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return jsonify([
        {
            "id": r["id"],
            "numero": r["numero"],
            "libelle": r["libelle"],
            "type": r["type"],
        }
        for r in rows
    ])


@plan_comptable_routes.route("/add", methods=["POST"])
@login_required
@permission_required("ACCESS_ADMIN")
def add_compte():
    data = request.get_json() or {}

    numero = data.get("numero")
    libelle = data.get("libelle")
    type_compte = data.get("type")
    societe_id = data.get("societe_id")

    if not numero or not libelle:
        return jsonify({"error": "numero et libelle obligatoires"}), 400

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO plan_comptable (numero, libelle, type, societe_id)
            VALUES (:numero, :libelle, :type, :societe_id)
            ON CONFLICT (numero, societe_id)
            DO UPDATE SET
                libelle = EXCLUDED.libelle,
                type = EXCLUDED.type
        """), {
            "numero": numero,
            "libelle": libelle,
            "type": type_compte,
            "societe_id": societe_id,
        })

    return jsonify({"message": "Compte ajouté"}), 201


@plan_comptable_routes.route("/modele.csv")
@login_required
@permission_required("ACCESS_ADMIN")
def modele_plan_comptable():
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    writer.writerow(["numero", "libelle", "type"])
    writer.writerow(["101000", "Capital social", "Passif"])
    writer.writerow(["164000", "Emprunts auprès des établissements de crédit", "Passif"])
    writer.writerow(["401000", "Fournisseurs", "Passif"])
    writer.writerow(["411000", "Clients", "Actif"])
    writer.writerow(["512000", "Banque", "Actif"])
    writer.writerow(["606000", "Achats non stockés", "Charge"])
    writer.writerow(["607000", "Achats de marchandises", "Charge"])
    writer.writerow(["661100", "Intérêts des emprunts", "Charge"])
    writer.writerow(["681120", "Dotations amortissements immobilisations", "Charge"])
    writer.writerow(["701000", "Ventes de produits finis", "Produit"])
    writer.writerow(["706000", "Prestations de services", "Produit"])
    writer.writerow(["707000", "Ventes de marchandises", "Produit"])

    csv_data = "\ufeff" + output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8-sig",
        headers={
            "Content-Disposition": "attachment; filename=modele_plan_comptable.csv"
        },
    )


@plan_comptable_routes.route("/import", methods=["POST"])
@login_required
@permission_required("ACCESS_ADMIN")
def import_plan_comptable():
    file = request.files.get("file")
    societe_id = request.form.get("societe_id")

    if not file:
        return "Aucun fichier sélectionné", 400

    if not societe_id:
        return "Société obligatoire", 400

    content = file.read().decode("utf-8-sig").splitlines()
    reader = csv.DictReader(content, delimiter=";")

    with engine.begin() as conn:
        for row in reader:
            numero = row.get("numero")
            libelle = row.get("libelle")
            type_compte = row.get("type")

            if numero and libelle:
                conn.execute(text("""
                    INSERT INTO plan_comptable (numero, libelle, type, societe_id)
                    VALUES (:numero, :libelle, :type, :societe_id)
                    ON CONFLICT (numero, societe_id)
                    DO UPDATE SET
                        libelle = EXCLUDED.libelle,
                        type = EXCLUDED.type
                """), {
                    "numero": numero,
                    "libelle": libelle,
                    "type": type_compte,
                    "societe_id": societe_id,
                })

    return redirect("/plan-comptable/ui")


@plan_comptable_routes.route("/import-pcg/<int:societe_id>")
@login_required
@permission_required("ACCESS_ADMIN")
def import_pcg_standard(societe_id):
    comptes = [
        ("101000", "Capital social", "Passif"),
        ("164000", "Emprunts auprès des établissements de crédit", "Passif"),
        ("218300", "Matériel informatique", "Actif"),
        ("281830", "Amortissements du matériel informatique", "Passif"),
        ("401000", "Fournisseurs", "Passif"),
        ("411000", "Clients", "Actif"),
        ("445620", "TVA déductible sur immobilisations", "Actif"),
        ("445660", "TVA déductible sur autres biens et services", "Actif"),
        ("445710", "TVA collectée", "Passif"),
        ("512000", "Banque", "Actif"),
        ("530000", "Caisse", "Actif"),
        ("606000", "Achats non stockés", "Charge"),
        ("607000", "Achats de marchandises", "Charge"),
        ("613000", "Locations", "Charge"),
        ("622000", "Honoraires", "Charge"),
        ("641000", "Rémunérations du personnel", "Charge"),
        ("661100", "Intérêts des emprunts", "Charge"),
        ("681120", "Dotations amortissements immobilisations corporelles", "Charge"),
        ("701000", "Ventes de produits finis", "Produit"),
        ("706000", "Prestations de services", "Produit"),
        ("707000", "Ventes de marchandises", "Produit"),
    ]

    with engine.begin() as conn:
        for numero, libelle, type_compte in comptes:
            conn.execute(text("""
                INSERT INTO plan_comptable (numero, libelle, type, societe_id)
                VALUES (:numero, :libelle, :type, :societe_id)
                ON CONFLICT (numero, societe_id)
                DO UPDATE SET
                    libelle = EXCLUDED.libelle,
                    type = EXCLUDED.type
            """), {
                "numero": numero,
                "libelle": libelle,
                "type": type_compte,
                "societe_id": societe_id,
            })

    return redirect("/plan-comptable/ui")
