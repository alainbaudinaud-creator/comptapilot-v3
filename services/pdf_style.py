
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import TableStyle

styles = getSampleStyleSheet()

PRIMARY = colors.HexColor("#1d4ed8")
SECONDARY = colors.HexColor("#475467")
BG = colors.HexColor("#f8fafc")

TABLE_STYLE = TableStyle([

    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),

    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 11),

    ('BOTTOMPADDING', (0,0), (-1,0), 12),

    ('BACKGROUND', (0,1), (-1,-1), colors.white),

    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#d0d5dd")),

    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 10),

    ('ROWBACKGROUNDS', (0,1), (-1,-1),
        [colors.white, colors.HexColor("#f9fafb")]),

])
