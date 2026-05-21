from flask import Blueprint, Response, request
import sqlite3
import csv
import io
from controllers.auth import login_required
from services.permission_service import permission_required

balance_routes = Blueprint("balance", __name__)


def get_balance():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            p.numero,
            p.libelle,
            COALESCE(SUM(e.debit), 0) AS total_debit,
            COALESCE(SUM(e.credit), 0) AS total_credit,
            COALESCE(SUM(e.debit), 0) - COALESCE(SUM(e.credit), 0) AS solde
        FROM plan_comptable p
        LEFT JOIN ecritures e ON e.compte_id = p.id
        GROUP BY p.id, p.numero, p.libelle
        ORDER BY p.numero
    """)

    rows = c.fetchall()
    conn.close()
    return rows


@balance_routes.route("/")
@login_required
@permission_required("ACCESS_BILAN")
def balance_home():
    rows = get_balance()

    lignes = ""
    total_debit = 0
    total_credit = 0
    total_solde = 0

    for r in rows:
        total_debit += r[2]
        total_credit += r[3]
        total_solde += r[4]

        lignes += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td class="text-end">{r[2]:.2f}</td>
            <td class="text-end">{r[3]:.2f}</td>
            <td class="text-end">{r[4]:.2f}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Balance comptable</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">Balance comptable</h1>

            <div class="mb-3">
                <a href="/balance/export.csv" class="btn btn-success">Export CSV</a>
                <a href="/" class="btn btn-secondary">Retour</a>
            </div>

            <table class="table table-bordered table-striped bg-white">
                <thead class="table-dark">
                    <tr>
                        <th>Compte</th>
                        <th>Libellé</th>
                        <th class="text-end">Débit</th>
                        <th class="text-end">Crédit</th>
                        <th class="text-end">Solde</th>
                    </tr>
                </thead>
                <tbody>
                    {lignes}
                </tbody>
                <tfoot class="table-secondary fw-bold">
                    <tr>
                        <td colspan="2">TOTAL</td>
                        <td class="text-end">{total_debit:.2f}</td>
                        <td class="text-end">{total_credit:.2f}</td>
                        <td class="text-end">{total_solde:.2f}</td>
                    </tr>
                </tfoot>
            </table>
        </div>
    </body>
    </html>
    """


@balance_routes.route("/export.csv")
@login_required
@permission_required("ACCESS_BILAN")
def balance_export_csv():
    rows = get_balance()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    writer.writerow(["Compte", "Libellé", "Débit", "Crédit", "Solde"])

    for r in rows:
        writer.writerow(r)

    csv_data = "\ufeff" + output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8-sig",
        headers={
            "Content-Disposition": "attachment; filename=balance_comptable.csv"
        }
    )

