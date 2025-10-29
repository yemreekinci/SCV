from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import HRFlowable
from reportlab.platypus import Image
import io

pdfmetrics.registerFont(TTFont("Montserrat", "fonts/Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Bold", "fonts/Montserrat-Bold.ttf"))

def line(spaceBefore=4, spaceAfter=4, color="#000000", thickness=0.5):
    return HRFlowable(
        width="100%",
        thickness=thickness,
        lineCap='round',
        color=colors.HexColor(color),
        spaceBefore=spaceBefore,
        spaceAfter=spaceAfter
    )
    
def icon_text_row(icon_path, text, style, icon_size=10, padding=2):
    """
    Bir ikon ve yanında metin gösteren tablo döndürür.
    """
    try:
        img = Image(icon_path, width=icon_size, height=icon_size)
    except Exception:
        return Paragraph(text, style)

    table = Table(
        [[img, Paragraph(text, style)]],
        colWidths=[icon_size + padding, None],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ])
    )
    return table

def create_cv(data):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    doc.title = f"{data['name']}"
    
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.replace("\n", "<br/>")

    styles = getSampleStyleSheet()

    style_normal = ParagraphStyle(
        'NormalMontserrat',
        parent=styles['Normal'],
        fontName='Montserrat',
        fontSize=8,
        leading=11,
        spaceAfter=5
    )

    style_bold = ParagraphStyle(
        'BoldMontserrat',
        parent=styles['Normal'],
        fontName='Montserrat-Bold',
        fontSize=12,
        textColor=colors.HexColor("#000000"),
        spaceBefore=12,
        spaceAfter=6
    )

    style_header_name = ParagraphStyle(
        'HeaderName',
        parent=styles['Normal'],
        fontName='Montserrat-Bold',
        fontSize=24,
        leading=26,
        spaceAfter=2
    )

    style_header_title = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Montserrat',
        fontSize=16,
        leading=18,
        textColor=colors.HexColor("#555555"),
        spaceAfter=10
    )

    story = []

    story.append(Paragraph(data["name"], style_header_name))
    story.append(Paragraph(data["title"], style_header_title))
    story.append(line(spaceAfter=20))

    left_column = []
    left_column.append(Paragraph("<b>İLETİŞİM</b>", style_bold))
    left_column.append(line())

    contact_items = [
        ("Telefon", data["telephone"]),
        ("E-posta", data["email"]),
        ("Web", data["web"]),
        ("Adres", data["address"]),
        ("LinkedIn", data["linkedin"]),
        ("GitHub", data["github"])
    ]

    icon_paths = {
        "Telefon": "icons/phone.png",
        "E-posta": "icons/email.png",
        "Web": "icons/web.png",
        "Adres": "icons/address.png",
        "LinkedIn": "icons/linkedin.png",
        "GitHub": "icons/github.png"
    }

    for label, value in contact_items:
        if value:
            icon = icon_paths.get(label, None)
            if icon:
                left_column.append(icon_text_row(icon, value, style_normal))
            else:
                left_column.append(Paragraph(value, style_normal))

        
    left_column.append(Paragraph("<b>YETENEKLER</b>", style_bold))
    left_column.append(line())
    left_column.append(Paragraph(data["skills"], style_normal))

    left_column.append(Paragraph("<b>YABANCI DİLLER</b>", style_bold))
    left_column.append(line())
    left_column.append(Paragraph(data["languages"], style_normal))

    left_column.append(Paragraph("<b>REFERANSLAR</b>", style_bold))
    left_column.append(line())
    left_column.append(Paragraph(data["references"], style_normal))

    right_column = []
    right_column.append(Paragraph("<b>HAKKIMDA</b>", style_bold))
    right_column.append(line())
    right_column.append(Paragraph(data["about"], style_normal))

    right_column.append(Paragraph("<b>DENEYİM</b>", style_bold))
    right_column.append(line())
    right_column.append(Paragraph(data["experience"], style_normal)) 

    right_column.append(Paragraph("<b>EĞİTİM</b>", style_bold))
    right_column.append(line())
    right_column.append(Paragraph(data["education"], style_normal))

    right_column.append(Paragraph("<b>SERTİFİKALAR</b>", style_bold))
    right_column.append(line())
    right_column.append(Paragraph(data["certificates"], style_normal))

    right_column.append(Paragraph("<b>PROJELER</b>", style_bold))
    right_column.append(line())
    right_column.append(Paragraph(data["projects"], style_normal))


    layout = Table(
        [[left_column, right_column]],
        colWidths=[160, 340],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LINEAFTER', (0, 0), (0, -1), 0.5, colors.HexColor("#000000")),
        ])
    )
    story.append(layout)

    doc.build(story)
    buffer.seek(0)
    return buffer
