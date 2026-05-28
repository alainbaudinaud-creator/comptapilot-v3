from flask import Blueprint, Response
import csv
import io
from sqlalchemy import text
from database import engine
from controllers.auth import login_required
from services.permission_service import permission_required

grand_livre_routes = Blueprint("grand_livre", __name__)


def get_grand_livre():
    sql = """
        SELECT
            p.numero,
            p.libelle AS compte_libelle,
            e.date_ecriture,
            e.journal AS piece,
            e.libelle AS ecriture_libelle,
            CASE WHEN e.compte_debit = p.numero THEN e.montant_ttc ELSE 0 END AS debit,
            CASE WHEN e.compte_credit = p.numero THEN e.montant_ttc ELSE 0 END AS credit
        FROM plan_comptable p
        LEFT JOIN ecritures_premium e
            ON (e.compte_debit = p.numero OR e.compte_credit = p.numero)
           AND (e.societe_id = p.societe_id OR p.societe_id IS NULL)
        ORDER BY p.numero, e.date_ecriture, e.id
    """

    with engine.begin() as conn:
        return conn.execute(text(sql)).fetchall()


@grand_livre_routes.route("/")
@login_required
@permission_required("ACCESS_JOURNAUX")
def grand_livre_home():
    rows = get_grand_livre()

    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Grand livre</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">Grand livre comptable PostgreSQL</h1>

            <div class="mb-3">
                <a href="/grand-livre/export.csv" class="btn btn-success">Export CSV</a>
                <a href="/" class="btn btn-secondary">Retour</a>
            </div>
    """

    current_compte = None
    total_debit = 0
    total_credit = 0

    for row in rows:
        compte = f"{row[0]} - {row[1]}"

        if compte != current_compte:
            if current_compte is not None:
                solde = total_debit - total_credit
                html += f"""
                    <tfoot class="table-secondary fw-bold">
                        <tr>
                            <td colspan="3">TOTAL {current_compte}</td>
                            <td class="text-end">{total_debit:.2f}</td>
                            <td class="text-end">{total_credit:.2f}</td>
                            <td class="text-end">{solde:.2f}</td>
                        </tr>
                    </tfoot>
                </table>
                """

            current_compte = compte
            total_debit = 0
            total_credit = 0

            html += f"""
            <h3 class="mt-4">{current_compte}</h3>
            <table class="table table-bordered table-striped bg-white">
                <thead class="table-dark">
                    <tr>
                        <th>Date</th>
                        <th>Pièce</th>
                        <th>Libellé</th>
                        <th class="text-end">Débit</th>
                        <th class="text-end">Crédit</th>
                        <th class="text-end">Solde</th>
                    </tr>
                </thead>
                <tbody>
            """

        debit = float(row[5] or 0)
        credit = float(row[6] or 0)
        total_debit += debit
        total_credit += credit
        solde_ligne = total_debit - total_credit

        if row[2]:
            html += f"""
            <tr>
                <td>{row[2] or ""}</td>
                <td>{row[3] or ""}</td>
                <td>{row[4] or ""}</td>
                <td class="text-end">{debit:.2f}</td>
                <td class="text-end">{credit:.2f}</td>
                <td class="text-end">{solde_ligne:.2f}</td>
            </tr>
            """

    if current_compte is not None:
        solde = total_debit - total_credit
        html += f"""
                </tbody>
                <tfoot class="table-secondary fw-bold">
                    <tr>
                        <td colspan="3">TOTAL {current_compte}</td>
                        <td class="text-end">{total_debit:.2f}</td>
                        <td class="text-end">{total_credit:.2f}</td>
                        <td class="text-end">{solde:.2f}</td>
                    </tr>
                </tfoot>
            </table>
        """

    html += """
        </div>
    </body>
    </html>
    """

    return html


@grand_livre_routes.route("/export.csv")
@login_required
@permission_required("ACCESS_JOURNAUX")
def grand_livre_export_csv():
    rows = get_grand_livre()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    writer.writerow([
        "Compte", "Libellé compte", "Date", "Pièce",
        "Libellé écriture", "Débit", "Crédit"
    ])

    for r in rows:
        writer.writerow(r)

    csv_data = "\ufeff" + output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8-sig",
        headers={
            "Content-Disposition": "attachment; filename=grand_livre.csv"
        },
    )
