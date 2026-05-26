
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generer_liasse_pdf(fichier="liasse_fiscale.pdf"):

    doc = SimpleDocTemplate(fichier)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("LIASSE FISCALE COMPTAPILOT", styles["Title"]))
    elements.append(Spacer(1, 20))

    forms = [
        "2033-A",
        "2033-B",
        "2033-C",
        "2033-D",
        "2033-E",
        "2033-F",
        "2033-G",
    ]

    for f in forms:
        elements.append(Paragraph(f"Formulaire {f}", styles["Heading2"]))

    doc.build(elements)

    return fichier

