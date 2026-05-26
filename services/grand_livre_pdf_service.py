
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph
from reportlab.lib.pagesizes import landscape, A4
from services.pdf_theme import TABLE_STYLE, TOTAL_STYLE, SECTION, BODY, cover, kpi_table, money, header_footer

def generer_grand_livre_pdf(db="db.sqlite", fichier="grand_livre.pdf"):
    con = sqlite3.connect(db)
    cur = con.cursor()

    rows = cur.execute("""
        SELECT date_ecriture, journal, piece, libelle, numero, compte, debit, credit
        FROM vue_grand_livre
        ORDER BY date_ecriture
    """).fetchall()

    total_debit = sum(float(r[6] or 0) for r in rows)
    total_credit = sum(float(r[7] or 0) for r in rows)

    doc = SimpleDocTemplate(
        fichier,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=70,
        bottomMargin=45,
    )

    elements = []
    elements += cover("Grand livre", "Détail chronologique des écritures comptables")

    elements.append(kpi_table([
        ("Écritures", str(len(rows))),
        ("Débit", money(total_debit)),
        ("Crédit", money(total_credit)),
    ]))

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("Détail des écritures", SECTION))

    data = [["Date", "Journal", "Pièce", "Libellé", "Compte", "Nom", "Débit", "Crédit"]]
    for r in rows:
        data.append([r[0] or "", r[1] or "", r[2] or "", r[3] or "", r[4] or "", r[5] or "", money(r[6]), money(r[7])])

    table = Table(data, colWidths=[65, 55, 70, 190, 65, 150, 80, 80], repeatRows=1)
    table.setStyle(TABLE_STYLE)
    elements.append(table)

    elements.append(Spacer(1, 16))

    total = Table([["Totaux", money(total_debit), money(total_credit)]], colWidths=[595, 80, 80])
    total.setStyle(TOTAL_STYLE)
    elements.append(total)

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Le grand livre reprend chaque écriture avec son compte comptable.", BODY))

    doc.build(elements)
    con.close()
    return fichier


