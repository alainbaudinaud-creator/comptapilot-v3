
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph
from services.pdf_theme import PAGE_SIZE, TABLE_STYLE, TOTAL_STYLE, SECTION, BODY, cover, kpi_table, money, header_footer

def generer_resultat_pdf(db="db.sqlite", fichier="compte_resultat.pdf"):
    con = sqlite3.connect(db)
    cur = con.cursor()

    rows = cur.execute("SELECT numero, libelle, resultat FROM vue_compte_resultat ORDER BY numero").fetchall()

    produits = sum(float(r[2] or 0) for r in rows if str(r[0]).startswith("7"))
    charges = sum(float(r[2] or 0) for r in rows if str(r[0]).startswith("6"))
    resultat = produits + charges

    doc = SimpleDocTemplate(
        fichier,
        pagesize=PAGE_SIZE,
        rightMargin=40,
        leftMargin=40,
        topMargin=70,
        bottomMargin=45,
    )

    elements = []
    elements += cover("Compte de résultat", "Analyse de la performance économique")

    elements.append(kpi_table([
        ("Produits", money(produits)),
        ("Charges", money(charges)),
        ("Résultat", money(resultat)),
    ]))

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("Détail du compte de résultat", SECTION))

    data = [["Compte", "Libellé", "Montant"]]
    for numero, libelle, montant in rows:
        data.append([numero or "", libelle or "", money(montant)])

    table = Table(data, colWidths=[80, 310, 120], repeatRows=1)
    table.setStyle(TABLE_STYLE)
    elements.append(table)

    elements.append(Spacer(1, 16))

    total = Table([["Résultat net", money(resultat)]], colWidths=[390, 120])
    total.setStyle(TOTAL_STYLE)
    elements.append(total)

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Ce document est généré à partir des comptes de charges et produits.", BODY))

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    con.close()
    return fichier

