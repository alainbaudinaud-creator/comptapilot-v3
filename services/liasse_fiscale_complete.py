
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph, PageBreak
from services.pdf_theme import PAGE_SIZE, TABLE_STYLE, SECTION, BODY, cover, kpi_table, money, header_footer

def generer_liasse_complete(fichier="liasse_complete.pdf"):
    doc = SimpleDocTemplate(
        fichier,
        pagesize=PAGE_SIZE,
        rightMargin=40,
        leftMargin=40,
        topMargin=70,
        bottomMargin=45,
    )

    elements = []
    elements += cover("Liasse fiscale", "Préparation fiscale structurée et homogène")

    elements.append(kpi_table([
        ("Régime", "Simplifié"),
        ("Formulaires", "2033 A à G"),
        ("Statut", "Préparée"),
    ]))

    forms = [
        ("2033-A", "Bilan simplifié"),
        ("2033-B", "Compte de résultat simplifié"),
        ("2033-C", "Immobilisations et amortissements"),
        ("2033-D", "Provisions et déficits"),
        ("2033-E", "Valeur ajoutée"),
        ("2033-F", "Composition du capital"),
        ("2033-G", "Filiales et participations"),
    ]

    for code, label in forms:
        elements.append(Spacer(1, 18))
        elements.append(Paragraph(f"{code} — {label}", SECTION))

        data = [
            ["Rubrique", "Valeur"],
            ["Statut", "Préparé automatiquement"],
            ["Contrôle", "À valider"],
            ["Source", "ComptaPilot ERP"],
        ]

        table = Table(data, colWidths=[180, 310])
        table.setStyle(TABLE_STYLE)
        elements.append(table)

    elements.append(PageBreak())
    elements += cover("Synthèse de validation", "Contrôles préalables avant dépôt")
    elements.append(Paragraph("La liasse fiscale doit être validée par un professionnel avant transmission.", BODY))

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    return fichier
