
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph
from services.pdf_theme import PAGE_SIZE, TABLE_STYLE, TOTAL_STYLE, SECTION, BODY, cover, kpi_table, money, header_footer

def generer_bilan_pdf(db="db.sqlite", fichier="bilan.pdf"):
    con = sqlite3.connect(db)
    cur = con.cursor()

    rows = cur.execute("SELECT numero, libelle, solde FROM vue_bilan ORDER BY numero").fetchall()

    total_actif = sum(float(r[2] or 0) for r in rows if str(r[0]).startswith(("2", "3", "4", "5")))
    total_passif = sum(float(r[2] or 0) for r in rows if str(r[0]).startswith("1"))

    doc = SimpleDocTemplate(
        fichier,
        pagesize=PAGE_SIZE,
        rightMargin=40,
        leftMargin=40,
        topMargin=70,
        bottomMargin=45,
    )

    elements = []
    elements += cover("Bilan comptable", "Synthèse patrimoniale de la société")

    elements.append(kpi_table([
        ("Total actif", money(total_actif)),
        ("Total passif", money(total_passif)),
        ("Équilibre", money(total_actif + total_passif)),
    ]))

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("Détail des comptes de bilan", SECTION))

    data = [["Compte", "Libellé", "Solde"]]
    for numero, libelle, solde in rows:
        data.append([numero or "", libelle or "", money(solde)])

    table = Table(data, colWidths=[80, 310, 120], repeatRows=1)
    table.setStyle(TABLE_STYLE)
    elements.append(table)

    elements.append(Spacer(1, 16))

    total = Table([["Total bilan", money(sum(float(r[2] or 0) for r in rows))]], colWidths=[390, 120])
    total.setStyle(TOTAL_STYLE)
    elements.append(total)

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Ce document est généré à partir des écritures validées dans ComptaPilot ERP.", BODY))

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    con.close()
    return fichier


