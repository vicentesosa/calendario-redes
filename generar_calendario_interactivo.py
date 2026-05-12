"""
Genera el calendario editorial semanal como PDF interactivo.
Cada fila tiene un boton triangulo (flecha abajo) junto a la cantidad.
Al hacer clic en Adobe Acrobat Reader se abre un popup con ideas de contenido.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DictionaryObject, ArrayObject, NameObject,
    FloatObject, NumberObject, DecodedStreamObject,
    create_string_object,
)

# ── Dimensiones de pagina ────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.28 x 841.89 pts
MARGIN = 2 * cm              # 56.69 pts

# ── Columnas tabla principal ─────────────────────────────────────────────────
C0 = MARGIN                  # Dia      3.8 cm
C1 = C0 + 3.8 * cm           # Plataforma 4.8 cm
C2 = C1 + 4.8 * cm           # Formato  5.2 cm
C3 = C2 + 5.2 * cm           # Cant.    2.2 cm
C4 = C3 + 2.2 * cm

ROW_H_HDR = 0.80 * cm
ROW_H_DAT = 0.72 * cm

# ── Columnas tabla resumen ───────────────────────────────────────────────────
S0 = MARGIN
S1 = S0 + 5.5 * cm
S2 = S1 + 4.5 * cm
S3 = S2 + 4.0 * cm

ROW_H_SHDR = 0.75 * cm
ROW_H_SDAT = 0.68 * cm

# ── Paleta ───────────────────────────────────────────────────────────────────
DARK    = colors.HexColor("#0F172A")
SLATE   = colors.HexColor("#475569")
HDR_BG  = colors.HexColor("#1E293B")
TT      = colors.HexColor("#FE2C55")
TT_L    = colors.HexColor("#FFF0F2")
TT_A    = colors.HexColor("#FFE8EC")
IG      = colors.HexColor("#C13584")
IG_L    = colors.HexColor("#FDF0F8")
IG_A    = colors.HexColor("#F1F5F9")
INDIGO  = colors.HexColor("#6366F1")
INDIG_L = colors.HexColor("#EEF2FF")
GREEN_L = colors.HexColor("#F0FDF4")
GREEN_T = colors.HexColor("#16a34a")
BORDER  = colors.HexColor("#CBD5E1")
WHITE   = colors.white

# ── Datos del calendario ─────────────────────────────────────────────────────
ROWS = [
    ("Lunes",     "TikTok",           "Video",            "1",
     "Ideas - Lunes / TikTok / Video:\n"
     "- Transicion mostrando tu setup de trabajo\n"
     "- Antes y despues de un proyecto real\n"
     "- Rutina de desarrollador en 60 segundos"),
    ("Lunes",     "Instagram",        "Historia",         "3",
     "Ideas - Lunes / Instagram / Historias:\n"
     "- Encuesta sobre tecnologias favoritas\n"
     "- Cuenta regresiva de entrega de proyecto\n"
     "- Pregunta abierta a tu audiencia"),
    ("Martes",    "Instagram",        "Reel",             "1",
     "Ideas - Martes / Instagram / Reel:\n"
     "- Tip de herramienta en 30 segundos\n"
     "- Error frecuente mas solucion rapida\n"
     "- Comparativa visual de dos frameworks"),
    ("Martes",    "Instagram",        "Historia",         "3",
     "Ideas - Martes / Instagram / Historias:\n"
     "- Behind the scenes del Reel de hoy\n"
     "- Repost de menciones recibidas\n"
     "- Poll sobre preferencias tech"),
    ("Miercoles", "Instagram",        "Historia",         "3",
     "Ideas - Miercoles / Instagram / Historias:\n"
     "- Dia a dia mostrando tu flujo de trabajo\n"
     "- Screenshot de proyecto en curso\n"
     "- Recomendacion de recurso o herramienta"),
    ("Miercoles", "Instagram (Feed)", "Posteo estatico",  "1",
     "Ideas - Miercoles / Feed / Posteo:\n"
     "- Foto profesional de tu workspace\n"
     "- Cita inspiradora del sector tech\n"
     "- Dato estadistico con diseno minimalista"),
    ("Jueves",    "TikTok",           "Video",            "1",
     "Ideas - Jueves / TikTok / Video:\n"
     "- Review de herramienta o libreria nueva\n"
     "- Duet o Stitch con creador tech\n"
     "- Error comun en desarrollo y como evitarlo"),
    ("Jueves",    "Instagram",        "Historia",         "2",
     "Ideas - Jueves / Instagram / Historias:\n"
     "- Reflexion breve del dia\n"
     "- Compartir un post antiguo destacado\n"
     "- Cuenta regresiva al viernes"),
    ("Viernes",   "Instagram",        "Reel",             "1",
     "Ideas - Viernes / Instagram / Reel:\n"
     "- Resumen de aprendizajes de la semana\n"
     "- Top 3 tips que aplicaste esta semana\n"
     "- Celebracion de logro o entrega completada"),
    ("Viernes",   "Instagram",        "Historia",         "3",
     "Ideas - Viernes / Instagram / Historias:\n"
     "- Celebracion de cierre de semana\n"
     "- Pregunta abierta para conectar con seguidores\n"
     "- Contenido UGC o mensajes de la comunidad"),
    ("Sabado",    "Instagram",        "Historia",         "2",
     "Ideas - Sabado / Instagram / Historias:\n"
     "- Contenido relajado o lifestyle tech\n"
     "- Hobby relacionado con tecnologia\n"
     "- Recomendacion de libro, podcast o canal"),
    ("Sabado",    "Instagram (Feed)", "Carrusel",         "1",
     "Ideas - Sabado / Feed / Carrusel:\n"
     "- 5 errores comunes en X tecnologia\n"
     "- Checklist de buenas practicas\n"
     "- Comparativa visual de herramientas o stacks"),
    ("Domingo",   "TikTok",           "Video",            "1",
     "Ideas - Domingo / TikTok / Video:\n"
     "- Reflexion y aprendizajes de la semana\n"
     "- Motivacion para arrancar la proxima semana\n"
     "- Video personal sobre vida como desarrollador"),
    ("Domingo",   "Instagram",        "Historia",         "2",
     "Ideas - Domingo / Instagram / Historias:\n"
     "- Preview del contenido de la semana siguiente\n"
     "- Pregunta para arrancar el lunes con energia\n"
     "- Agradecimiento a la comunidad"),
]

SUMMARY = [
    ("Video",           "TikTok",    "3",  TT_L,    TT),
    ("Reel",            "Instagram", "2",  IG_L,    IG),
    ("Historia",        "Instagram", "18", GREEN_L, GREEN_T),
    ("Posteo estatico", "Instagram", "1",  IG_L,    IG),
    ("Carrusel",        "Instagram", "1",  INDIG_L, INDIGO),
]

# ── Helpers canvas ───────────────────────────────────────────────────────────
def sf(cv, col): cv.setFillColor(col)
def ss(cv, col): cv.setStrokeColor(col)

def row_bg(idx, plat):
    is_tt = "TikTok" in plat
    return (TT_L if is_tt else IG_L) if idx % 2 == 0 else (TT_A if is_tt else IG_A)

# ── Dibujar fila tabla principal ─────────────────────────────────────────────
def draw_main_row(cv, y_top, cells, bg, plat_col=None, is_hdr=False):
    rh = ROW_H_HDR if is_hdr else ROW_H_DAT
    y_bot = y_top - rh
    xs = [C0, C1, C2, C3, C4]
    ws = [C1-C0, C2-C1, C3-C2, C4-C3]

    sf(cv, bg)
    cv.rect(C0, y_bot, C4-C0, rh, fill=1, stroke=0)
    ss(cv, BORDER); cv.setLineWidth(0.4)
    cv.rect(C0, y_bot, C4-C0, rh, fill=0, stroke=1)
    for x in xs[1:-1]:
        cv.line(x, y_bot, x, y_top)

    fs = 11 if is_hdr else 9.5
    ty = y_bot + rh * 0.30

    for i, (txt, x, w) in enumerate(zip(cells, xs, ws)):
        if is_hdr:
            cv.setFont("Helvetica-Bold", fs); sf(cv, WHITE)
            cv.drawCentredString(x + w/2, ty, txt)
        elif i == 1 and plat_col:
            cv.setFont("Helvetica-Bold", fs); sf(cv, plat_col)
            cv.drawCentredString(x + w/2, ty, txt)
        elif i == 3:
            # Numero alineado a la izquierda del col, deja espacio al boton
            cv.setFont("Helvetica-Bold", fs); sf(cv, DARK)
            cv.drawCentredString(x + w * 0.32, ty, txt)
        else:
            cv.setFont("Helvetica", fs); sf(cv, DARK)
            cv.drawCentredString(x + w/2, ty, txt)
    return y_bot

# ── Dibujar fila tabla resumen ───────────────────────────────────────────────
def draw_sum_row(cv, y_top, cells, bg, txt_col=None, is_hdr=False):
    rh = ROW_H_SHDR if is_hdr else ROW_H_SDAT
    y_bot = y_top - rh
    xs = [S0, S1, S2, S3]
    ws = [S1-S0, S2-S1, S3-S2]

    sf(cv, bg)
    cv.rect(S0, y_bot, S3-S0, rh, fill=1, stroke=0)
    ss(cv, BORDER); cv.setLineWidth(0.4)
    cv.rect(S0, y_bot, S3-S0, rh, fill=0, stroke=1)
    for x in xs[1:-1]:
        cv.line(x, y_bot, x, y_top)

    fs = 10 if is_hdr else 9.5
    ty = y_bot + rh * 0.30
    for i, (txt, x, w) in enumerate(zip(cells, xs, ws)):
        if is_hdr:
            cv.setFont("Helvetica-Bold", fs); sf(cv, WHITE)
        elif i == 0 and txt_col:
            cv.setFont("Helvetica-Bold", fs); sf(cv, txt_col)
        else:
            cv.setFont("Helvetica", fs); sf(cv, DARK)
        cv.drawCentredString(x + w/2, ty, txt)
    return y_bot

# ── Construir PDF base con reportlab ─────────────────────────────────────────
buf = BytesIO()
cv = canvas.Canvas(buf, pagesize=A4)

# Titulo
cv.setFont("Helvetica-Bold", 22); sf(cv, DARK)
cv.drawCentredString(PAGE_W/2, PAGE_H - MARGIN - 26, "Calendario Editorial Semanal")
cv.setFont("Helvetica", 11); sf(cv, SLATE)
cv.drawCentredString(PAGE_W/2, PAGE_H - MARGIN - 46,
                     "Personal Branding  ·  Desarrollador Web  ·  TikTok & Instagram")

table_top = PAGE_H - MARGIN - 68

# Header
y = table_top
y = draw_main_row(cv, y, ["Dia", "Plataforma", "Formato", "Cant."], HDR_BG, is_hdr=True)

btn_data = []
for i, (day, plat, fmt, qty, ideas) in enumerate(ROWS):
    bg = row_bg(i, plat)
    plat_col = TT if "TikTok" in plat else IG
    y_bot = draw_main_row(cv, y, [day, plat, fmt, qty], bg, plat_col=plat_col)

    # Rectangulo del boton: parte derecha de la columna Cant.
    bw, bh = 14, 11
    bx1 = C3 + (C4 - C3) * 0.57
    by1 = y_bot + (ROW_H_DAT - bh) / 2
    btn_data.append((bx1, by1, bx1 + bw, by1 + bh, ideas, f"btn_{i}"))
    y = y_bot

# Seccion resumen
y -= 0.55 * cm
cv.setFont("Helvetica-Bold", 12); sf(cv, DARK)
cv.drawString(S0, y - 11, "Resumen semanal")
y -= 0.48 * cm

y = draw_sum_row(cv, y, ["Formato", "Plataforma", "Total semanal"], HDR_BG, is_hdr=True)
for fmt, plat, total, bg, txt_col in SUMMARY:
    y = draw_sum_row(cv, y, [fmt, plat, total], bg, txt_col=txt_col)

# Notas al pie
y -= 0.32 * cm
cv.setFont("Helvetica-Oblique", 8); sf(cv, SLATE)
for line in [
    "Logica de distribucion:  TikTok publica lunes, jueves y domingo (cada 3 dias).",
    "Reels publican martes y viernes, sin coincidir con TikTok.  Historias presentes los 7 dias (min. 2, max. 3 por dia).",
    "Feed activo miercoles (estatico) y sabado (carrusel).  Ningun dia queda sin actividad.",
]:
    cv.drawString(S0, y - 9, line)
    y -= 11

cv.save()

# ── Agregar botones interactivos con pypdf ───────────────────────────────────
buf.seek(0)
reader = PdfReader(buf)
writer = PdfWriter()
writer.append(reader)
page = writer.pages[0]


def make_triangle_ap(bw, bh):
    """Appearance stream: triangulo indigo apuntando hacia abajo."""
    cx = bw / 2
    pad = 2.2
    code = (
        f"q\n"
        f"0.388 0.400 0.945 rg\n"          # indigo #6366F1
        f"{cx - 4:.2f} {bh - pad:.2f} m\n"
        f"{cx + 4:.2f} {bh - pad:.2f} l\n"
        f"{cx:.2f} {pad:.2f} l\n"
        f"f\n"
        f"Q\n"
    ).encode("latin-1")
    stream = DecodedStreamObject()
    stream.set_data(code)
    stream[NameObject("/Type")]    = NameObject("/XObject")
    stream[NameObject("/Subtype")] = NameObject("/Form")
    stream[NameObject("/BBox")]    = ArrayObject([
        FloatObject(0), FloatObject(0), FloatObject(bw), FloatObject(bh)
    ])
    return stream


# Crear AcroForm en el catalogo
catalog = writer._root_object
acroform = DictionaryObject({
    NameObject("/Fields"): ArrayObject(),
    NameObject("/DR"):     DictionaryObject(),
    NameObject("/DA"):     create_string_object("/Helv 0 Tf 0 g"),
})
acroform_ref = writer._add_object(acroform)
catalog[NameObject("/AcroForm")] = acroform_ref

if "/Annots" not in page:
    page[NameObject("/Annots")] = ArrayObject()

for x1, y1, x2, y2, ideas, name in btn_data:
    bw = x2 - x1
    bh = y2 - y1

    ap_ref = writer._add_object(make_triangle_ap(bw, bh))
    ap_dict = DictionaryObject({NameObject("/N"): ap_ref})

    # Texto para el popup de JavaScript
    js_body = (ideas
               .replace("\\", "\\\\")
               .replace("'", "\\'")
               .replace("\r", "")
               .replace("\n", "\\n"))
    js_code = f"app.alert('{js_body}', 3);"

    action = DictionaryObject({
        NameObject("/Type"): NameObject("/Action"),
        NameObject("/S"):    NameObject("/JavaScript"),
        NameObject("/JS"):   create_string_object(js_code),
    })

    widget = DictionaryObject({
        NameObject("/Type"):    NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Widget"),
        NameObject("/FT"):      NameObject("/Btn"),
        NameObject("/Ff"):      NumberObject(65536),   # PushButton flag
        NameObject("/T"):       create_string_object(name),
        NameObject("/DA"):      create_string_object("/Helv 0 Tf 0 g"),
        NameObject("/Rect"):    ArrayObject([
            FloatObject(x1), FloatObject(y1),
            FloatObject(x2), FloatObject(y2),
        ]),
        NameObject("/AP"):  ap_dict,
        NameObject("/AA"):  DictionaryObject({
            NameObject("/U"): action,   # mouse up
        }),
        NameObject("/BS"):  DictionaryObject({
            NameObject("/W"): FloatObject(0),
            NameObject("/S"): NameObject("/S"),
        }),
    })

    widget_ref = writer._add_object(widget)
    page["/Annots"].append(widget_ref)
    acroform["/Fields"].append(widget_ref)

OUTPUT = r"C:\Users\USUARIO\redes\calendario\calendario_editorial_semanal.pdf"
with open(OUTPUT, "wb") as f:
    writer.write(f)
print(f"PDF interactivo generado: {OUTPUT}")
