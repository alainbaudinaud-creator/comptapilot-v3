from pathlib import Path
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generer_pdf_liasse_v3(data, output_dir="/app/app_refonte/exports/fiscal"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    client = data.get("client", {})
    kpis = data.get("kpis", {})
    formulaires = data.get("formulaires", [])
    controles = data.get("controles", {})

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    client_id = client.get("id", "client")
    filename = f"liasse_fiscale_v3_client_{client_id}_{horodatage}.pdf"
    path = Path(output_dir) / filename

    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ComptaPilot V3 — Liasse fiscale", styles["Title"]))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph(f"Dossier : {client.get('raison_sociale', '-')}", styles["Heading2"]))
    elements.append(Paragraph(f"SIREN : {client.get('siren', '-')}", styles["Normal"]))
    elements.append(Paragraph(f"Régime fiscal : {client.get('regime_fiscal', '-')}", styles["Normal"]))
    elements.append(Spacer(1, 14))

    synthese = [
        ["Indicateur", "Valeur"],
        ["Résultat fiscal", str(kpis.get("resultat_fiscal", 0))],
        ["Type résultat", str(kpis.get("type_resultat", "-"))],
        ["Total actif", str(kpis.get("total_actif", 0))],
        ["Total passif", str(kpis.get("total_passif", 0))],
        ["Bilan équilibré", "Oui" if kpis.get("equilibre_bilan") else "Non"],
        ["Immobilisations", str(kpis.get("nb_immobilisations", 0))],
        ["Emprunts", str(kpis.get("nb_emprunts", 0))],
    ]

    table = Table(synthese, colWidths=[220, 260])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 18))

    elements.append(Paragraph("Formulaires 2033 A/B/C", styles["Heading2"]))

    rows = [["Formulaire", "Rubrique", "Valeur", "Statut"]]
    for f in formulaires:
        rows.append([
            str(f.get("formulaire", "")),
            str(f.get("rubrique", "")),
            str(f.get("valeur", "")),
            str(f.get("statut", "")),
        ])

    table = Table(rows, colWidths=[70, 210, 130, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 18))

    elements.append(Paragraph("Contrôles préalables", styles["Heading2"]))
    rows = [["Contrôle", "Résultat"]]
    for k, v in controles.items():
        rows.append([str(k), "OK" if v else "À contrôler"])

    table = Table(rows, colWidths=[280, 180])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#334155")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))
    elements.append(table)

    doc.build(elements)

    return {
        "filename": filename,
        "path": str(path),
    }
