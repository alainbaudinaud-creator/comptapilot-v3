
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

PAGE_SIZE = A4

NAVY = colors.HexColor("#0F172A")
BLUE = colors.HexColor("#2563EB")
LIGHT_BLUE = colors.HexColor("#EFF6FF")
GRAY = colors.HexColor("#667085")
BORDER = colors.HexColor("#E5E7EB")
SOFT = colors.HexColor("#F8FAFC")
WHITE = colors.white
GREEN = colors.HexColor("#16A34A")
RED = colors.HexColor("#DC2626")

base = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "CP_Title",
    parent=base["Title"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=28,
    textColor=NAVY,
    spaceAfter=8,
)

SUBTITLE = ParagraphStyle(
    "CP_Subtitle",
    parent=base["Normal"],
    fontName="Helvetica",
    fontSize=10,
    leading=14,
    textColor=GRAY,
    spaceAfter=18,
)

SECTION = ParagraphStyle(
    "CP_Section",
    parent=base["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=18,
    textColor=NAVY,
    spaceBefore=16,
    spaceAfter=10,
)

BODY = ParagraphStyle(
    "CP_Body",
    parent=base["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=13,
    textColor=NAVY,
)

RIGHT = ParagraphStyle(
    "CP_Right",
    parent=BODY,
    alignment=TA_RIGHT,
)

CENTER = ParagraphStyle(
    "CP_Center",
    parent=BODY,
    alignment=TA_CENTER,
)

def money(value):
    try:
        return f"{float(value):,.2f} €".replace(",", " ").replace(".", ",")
    except Exception:
        return "0,00 €"

def header_footer(canvas, doc):
    canvas.saveState()

    width, height = PAGE_SIZE

    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 46, width, 46, fill=True, stroke=False)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(40, height - 29, "ComptaPilot ERP")

    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 40, height - 28, "Document comptable professionnel")

    canvas.setStrokeColor(BORDER)
    canvas.line(40, 32, width - 40, 32)

    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(40, 20, "Généré automatiquement par ComptaPilot")
    canvas.drawRightString(width - 40, 20, f"Page {doc.page}")

    canvas.restoreState()

def cover(title, subtitle):
    return [
        Spacer(1, 18),
        Paragraph(title, TITLE),
        Paragraph(subtitle, SUBTITLE),
        Spacer(1, 10),
    ]

def kpi_table(items):
    data = []
    row = []
    for label, value in items:
        row.append(Paragraph(f"<b>{label}</b><br/><font size='14'>{value}</font>", BODY))
    data.append(row)

    from reportlab.platypus import Table

    t = Table(data, colWidths=[125] * len(items))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BLUE),
        ("BOX", (0,0), (-1,-1), 0.6, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.6, WHITE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
    ]))
    return t

TABLE_STYLE = TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,0), 8),
    ("TOPPADDING", (0,0), (-1,0), 8),
    ("BOTTOMPADDING", (0,0), (-1,0), 8),

    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,1), (-1,-1), 8),
    ("TEXTCOLOR", (0,1), (-1,-1), NAVY),
    ("GRID", (0,0), (-1,-1), 0.4, BORDER),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, SOFT]),
    ("TOPPADDING", (0,1), (-1,-1), 6),
    ("BOTTOMPADDING", (0,1), (-1,-1), 6),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
])

TOTAL_STYLE = TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), LIGHT_BLUE),
    ("BOX", (0,0), (-1,-1), 0.6, BLUE),
    ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("TEXTCOLOR", (0,0), (-1,-1), NAVY),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
])

