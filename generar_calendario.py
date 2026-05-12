from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = r"C:\Users\USUARIO\redes\calendario\calendario_editorial_semanal.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

DARK = colors.HexColor("#0F172A")
ACCENT = colors.HexColor("#6366F1")
ACCENT_LIGHT = colors.HexColor("#EEF2FF")
TIKTOK = colors.HexColor("#FE2C55")
TIKTOK_LIGHT = colors.HexColor("#FFF0F2")
IG = colors.HexColor("#C13584")
IG_LIGHT = colors.HexColor("#FDF0F8")
HEADER_BG = colors.HexColor("#1E293B")
ROW_ALT = colors.HexColor("#F8FAFC")
WHITE = colors.white

title_style = ParagraphStyle(
    "Title",
    fontName="Helvetica-Bold",
    fontSize=22,
    textColor=DARK,
    alignment=TA_CENTER,
    spaceAfter=4,
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    fontName="Helvetica",
    fontSize=11,
    textColor=colors.HexColor("#475569"),
    alignment=TA_CENTER,
    spaceAfter=2,
)
section_style = ParagraphStyle(
    "Section",
    fontName="Helvetica-Bold",
    fontSize=13,
    textColor=DARK,
    spaceBefore=16,
    spaceAfter=6,
)
note_style = ParagraphStyle(
    "Note",
    fontName="Helvetica-Oblique",
    fontSize=8.5,
    textColor=colors.HexColor("#64748B"),
    alignment=TA_LEFT,
    spaceBefore=8,
)

story = []

story.append(Paragraph("Calendario Editorial Semanal", title_style))
story.append(Paragraph("Personal Branding · Desarrollador Web · TikTok &amp; Instagram", subtitle_style))
story.append(Spacer(1, 0.4*cm))

# ── Main calendar table ──────────────────────────────────────────────────────
cal_data = [
    ["Día", "Plataforma", "Formato", "Cant."],
    ["Lunes",     "TikTok",           "Video",           "1"],
    ["Lunes",     "Instagram",        "Historia",        "3"],
    ["Martes",    "Instagram",        "Reel",            "1"],
    ["Martes",    "Instagram",        "Historia",        "3"],
    ["Miércoles", "Instagram",        "Historia",        "3"],
    ["Miércoles", "Instagram (Feed)", "Posteo estático", "1"],
    ["Jueves",    "TikTok",           "Video",           "1"],
    ["Jueves",    "Instagram",        "Historia",        "2"],
    ["Viernes",   "Instagram",        "Reel",            "1"],
    ["Viernes",   "Instagram",        "Historia",        "3"],
    ["Sábado",    "Instagram",        "Historia",        "2"],
    ["Sábado",    "Instagram (Feed)", "Carrusel",        "1"],
    ["Domingo",   "TikTok",           "Video",           "1"],
    ["Domingo",   "Instagram",        "Historia",        "2"],
]

col_widths = [3.8*cm, 4.8*cm, 5.2*cm, 2.2*cm]

def platform_color(plataforma):
    if "TikTok" in plataforma:
        return TIKTOK_LIGHT
    return IG_LIGHT

def row_styles(data):
    cmds = [
        # Header
        ("BACKGROUND",   (0,0), (-1,0), HEADER_BG),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 11),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",    (0,0), (-1,0), 0.8*cm),
        ("ROWHEIGHT",    (0,1), (-1,-1), 0.72*cm),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,1), (-1,-1), 9.5),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
        ("LINEABOVE",    (0,0), (-1,0), 0, WHITE),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]
    for i, row in enumerate(data[1:], start=1):
        plat = row[1]
        bg = platform_color(plat)
        if i % 2 == 0:
            bg = colors.HexColor("#F1F5F9") if "TikTok" not in plat else colors.HexColor("#FFE8EC")
        cmds.append(("BACKGROUND", (0,i), (-1,i), bg))
        # Bold platform cell
        cmds.append(("FONTNAME", (1,i), (1,i), "Helvetica-Bold"))
        clr = TIKTOK if "TikTok" in plat else IG
        cmds.append(("TEXTCOLOR", (1,i), (1,i), clr))
    return cmds

cal_table = Table(cal_data, colWidths=col_widths, repeatRows=1)
cal_table.setStyle(TableStyle(row_styles(cal_data)))
story.append(cal_table)

# ── Summary table ────────────────────────────────────────────────────────────
story.append(Paragraph("Resumen semanal", section_style))

sum_data = [
    ["Formato", "Plataforma", "Total semanal"],
    ["Video",           "TikTok",    "3"],
    ["Reel",            "Instagram", "2"],
    ["Historia",        "Instagram", "18"],
    ["Posteo estático", "Instagram", "1"],
    ["Carrusel",        "Instagram", "1"],
]

sum_col_widths = [5.5*cm, 4.5*cm, 4*cm]
sum_table = Table(sum_data, colWidths=sum_col_widths)
sum_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), HEADER_BG),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,0), 10),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("ROWHEIGHT",     (0,0), (-1,0), 0.75*cm),
    ("ROWHEIGHT",     (0,1), (-1,-1), 0.68*cm),
    ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",      (0,1), (-1,-1), 9.5),
    ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
    ("BACKGROUND",    (0,1), (-1,1), TIKTOK_LIGHT),
    ("BACKGROUND",    (0,2), (-1,2), IG_LIGHT),
    ("BACKGROUND",    (0,3), (-1,3), colors.HexColor("#F0FDF4")),
    ("BACKGROUND",    (0,4), (-1,4), IG_LIGHT),
    ("BACKGROUND",    (0,5), (-1,5), colors.HexColor("#F0FDF4")),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(sum_table)

# ── Notes ───────────────────────────────────────────────────────────────────
notas = (
    "Logica de distribucion:  "
    "TikTok publica lunes, jueves y domingo (cada 3 dias).  "
    "Reels publican martes y viernes, sin coincidir con dias de TikTok.  "
    "Historias presentes los 7 dias (min. 2, max. 3 por dia).  "
    "Feed de Instagram activo miercoles (estatico) y sabado (carrusel).  "
    "Ningun dia queda sin actividad."
)
story.append(Paragraph(notas, note_style))

doc.build(story)
print(f"PDF generado: {OUTPUT}")
