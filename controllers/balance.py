from flask import Blueprint, Response
import csv
import io
from sqlalchemy import text
from database import engine
from controllers.auth import login_required
from services.permission_service import permission_required

balance_routes = Blueprint("balance", __name__)


def get_balance():
    sql = """
        WITH lignes AS (
            SELECT
                societe_id,
                compte_debit AS numero,
                montant_ttc AS debit,
                0::numeric AS credit
            FROM ecritures_premium

            UNION ALL

            SELECT
                societe_id,
                compte_credit AS numero,
                0::numeric AS debit,
                montant_ttc AS credit
            FROM ecritures_premium
        )
        SELECT
            p.numero,
            p.libelle,
            COALESCE(SUM(l.debit), 0) AS total_debit,
            COALESCE(SUM(l.credit), 0) AS total_credit,
            COALESCE(SUM(l.debit), 0) - COALESCE(SUM(l.credit), 0) AS solde
        FROM plan_comptable p
        LEFT JOIN lignes l
            ON l.numero = p.numero
           AND (l.societe_id = p.societe_id OR p.societe_id IS NULL)
        GROUP BY p.numero, p.libelle
        ORDER BY p.numero
    """

    with engine.begin() as conn:
        return conn.execute(text(sql)).fetchall()


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
        total_debit += float(r[2] or 0)
        total_credit += float(r[3] or 0)
        total_solde += float(r[4] or 0)

        lignes += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td class="text-end">{float(r[2] or 0):.2f}</td>
            <td class="text-end">{float(r[3] or 0):.2f}</td>
            <td class="text-end">{float(r[4] or 0):.2f}</td>
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
            <h1 class="mb-4">Balance comptable PostgreSQL</h1>

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
        },
    )
