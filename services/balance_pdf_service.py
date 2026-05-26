
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph
from services.pdf_theme import PAGE_SIZE, TABLE_STYLE, TOTAL_STYLE, SECTION, BODY, cover, kpi_table, money, header_footer

def generer_balance_pdf(db="db.sqlite", fichier="balance.pdf"):
    con = sqlite3.connect(db)
    cur = con.cursor()

    rows = cur.execute("SELECT numero, libelle, total_debit, total_credit, solde FROM vue_balance ORDER BY numero").fetchall()

    total_debit = sum(float(r[2] or 0) for r in rows)
    total_credit = sum(float(r[3] or 0) for r in rows)
    solde = sum(float(r[4] or 0) for r in rows)

    doc = SimpleDocTemplate(
        fichier,
        pagesize=PAGE_SIZE,
        rightMargin=30,
        leftMargin=30,
        topMargin=70,
        bottomMargin=45,
    )

    elements = []
    elements += cover("Balance générale", "Vue globale des comptes mouvementés")

    elements.append(kpi_table([
        ("Débit", money(total_debit)),
        ("Crédit", money(total_credit)),
        ("Solde", money(solde)),
    ]))

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("Détail de la balance", SECTION))

    data = [["Compte", "Libellé", "Débit", "Crédit", "Solde"]]
    for numero, libelle, debit, credit, s in rows:
        data.append([numero or "", libelle or "", money(debit), money(credit), money(s)])

    table = Table(data, colWidths=[65, 230, 85, 85, 85], repeatRows=1)
    table.setStyle(TABLE_STYLE)
    elements.append(table)

    elements.append(Spacer(1, 16))

    total = Table([["Totaux", money(total_debit), money(total_credit), money(solde)]], colWidths=[295, 85, 85, 85])
    total.setStyle(TOTAL_STYLE)
    elements.append(total)

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("La balance présente les mouvements débit/crédit par compte.", BODY))

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    con.close()
    return fichier

