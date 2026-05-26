
from flask import Blueprint, request, jsonify, render_template, Response, redirect
from controllers.auth import login_required
import sqlite3
import csv
import io
from services.permission_service import permission_required

plan_comptable_routes = Blueprint('plan_comptable', __name__)


@plan_comptable_routes.route('/ui')
@login_required
@permission_required("ACCESS_ADMIN")
def ui():
    return render_template("plan_comptable.html")


@plan_comptable_routes.route('/', methods=['GET'])
@login_required
@permission_required("ACCESS_ADMIN")
def get_plan_comptable():
    societe_id = request.args.get("societe_id")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    if societe_id:
        c.execute("""
            SELECT id, numero, libelle, type
            FROM plan_comptable
            WHERE societe_id = ?
            ORDER BY numero
        """, (societe_id,))
    else:
        c.execute("""
            SELECT id, numero, libelle, type
            FROM plan_comptable
            ORDER BY numero
        """)

    rows = c.fetchall()
    conn.close()

    return jsonify([
        {"id": r[0], "numero": r[1], "libelle": r[2], "type": r[3]}
        for r in rows
    ])


@plan_comptable_routes.route('/add', methods=['POST'])
@login_required
@permission_required("ACCESS_ADMIN")
def add_compte():
    data = request.get_json()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO plan_comptable (numero, libelle, type, societe_id)
        VALUES (?, ?, ?, ?)
    """, (
        data.get('numero'),
        data.get('libelle'),
        data.get('type'),
        data.get('societe_id')
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Compte ajouté"}), 201


@plan_comptable_routes.route('/modele.csv')
@login_required
@permission_required("ACCESS_ADMIN")
def modele_plan_comptable():
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow(["numero", "libelle", "type"])
    writer.writerow(["101", "Capital", "Passif"])
    writer.writerow(["164", "Emprunts", "Passif"])
    writer.writerow(["401", "Fournisseurs", "Passif"])
    writer.writerow(["411", "Clients", "Actif"])
    writer.writerow(["512", "Banque", "Actif"])
    writer.writerow(["530", "Caisse", "Actif"])
    writer.writerow(["601", "Achats de matières", "Charge"])
    writer.writerow(["606", "Achats non stockés", "Charge"])
    writer.writerow(["613", "Locations", "Charge"])
    writer.writerow(["622", "Honoraires", "Charge"])
    writer.writerow(["641", "Salaires", "Charge"])
    writer.writerow(["701", "Ventes de produits finis", "Produit"])
    writer.writerow(["706", "Prestations de services", "Produit"])

    csv_data = "\ufeff" + output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8-sig",
        headers={
            "Content-Disposition": "attachment; filename=modele_plan_comptable.csv"
        }
    )


@plan_comptable_routes.route('/import', methods=['POST'])
@login_required
@permission_required("ACCESS_ADMIN")
def import_plan_comptable():
    file = request.files.get('file')
    societe_id = request.form.get("societe_id")

    if not file:
        return "Aucun fichier sélectionné"

    if not societe_id:
        return "Société obligatoire"

    content = file.read().decode('utf-8-sig').splitlines()
    reader = csv.DictReader(content, delimiter=';')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    for row in reader:
        numero = row.get("numero")
        libelle = row.get("libelle")
        type_compte = row.get("type")

        if numero and libelle and type_compte:
            c.execute("""
                INSERT INTO plan_comptable (numero, libelle, type, societe_id)
                VALUES (?, ?, ?, ?)
            """, (numero, libelle, type_compte, societe_id))

    conn.commit()
    conn.close()

    return redirect('/plan-comptable/ui')
@plan_comptable_routes.route('/import-pcg/<int:societe_id>')
@login_required
@permission_required("ACCESS_ADMIN")
def import_pcg_standard(societe_id):
    comptes = [
        ("101", "Capital", "Passif"),
        ("401", "Fournisseurs", "Passif"),
        ("411", "Clients", "Actif"),
        ("512", "Banque", "Actif"),
        ("601", "Achats", "Charge"),
        ("606", "Fournitures", "Charge"),
        ("701", "Ventes", "Produit"),
        ("706", "Prestations", "Produit"),
    ]

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    for numero, libelle, type_compte in comptes:
        c.execute("""
            INSERT INTO plan_comptable (numero, libelle, type, societe_id)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM plan_comptable
                WHERE numero = ? AND societe_id = ?
            )
        """, (numero, libelle, type_compte, societe_id, numero, societe_id))

    conn.commit()
    conn.close()

    return redirect('/plan-comptable/ui')



