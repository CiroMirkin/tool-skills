# /// script
# dependencies = ["reportlab", "pypdf"]
# ///
"""Convierte un archivo de texto en PDF.

  uv run pdf.py <entrada.txt> [-f columnas|simple|cuadernillo] [-o salida.pdf]

Texto de entrada: `# ` titulo, `## ` seccion, `### ` subseccion, parrafos separados por una
linea en blanco, bloques de `- ` vinetas, bloques de `> ` cita (sangrados), y `**negrita**`,
`*italica*` y `[texto](url)` dentro del texto. El resto se copia tal cual.

  columnas     A4, dos columnas, justificado (por defecto)
  simple       A4, una columna, justificado
  cuadernillo  paginas A5 impuestas de a dos por hoja A4 apaisada, en orden de cuadernillo:
               imprimir doble faz volteando por el borde corto, doblar al medio
"""
import argparse, io, re
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, FrameBreak, NextPageTemplate, PageTemplate, Paragraph

MARGIN, GUTTER, BODY, HEAD = 0.6 * inch, 0.3 * inch, 12, 14


# caracteres que Helvetica no tiene
MISSING = {"→": "->", "←": "<-", "≥": ">=", "≤": "<=", "≠": "!="}


def inline(s):
    for c, r in MISSING.items():
        s = s.replace(c, r)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2" color="#1a5fb4">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)


def story_from(text, body, head, sub, quote):
    title, story = None, []
    for block in re.split(r"\n\s*\n", text.replace("\r", "").strip()):
        lines = [l.strip() for l in block.splitlines()]
        if all(re.match(r"[-*] ", l) for l in lines):
            story += [Paragraph(inline(l[2:]), ParagraphStyle("l", parent=body, leftIndent=10), bulletText="•") for l in lines]
            continue
        line = " ".join(lines)
        if all(l.startswith(">") for l in lines):
            story.append(Paragraph(inline(" ".join(l[1:].strip() for l in lines)), quote))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), sub))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), head))
        elif line.startswith("# ") and title is None and not story:
            title = Paragraph(inline(line[2:]), head)
        else:
            story.append(Paragraph(inline(line), body))
    return title, story


def frame(x, y, w, h):
    return Frame(x, y, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)


def render(text, out, cols, pagesize, margin=MARGIN):
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=BODY, leading=BODY * 1.125,
                          alignment=TA_JUSTIFY, spaceAfter=5)
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=HEAD, leading=HEAD * 1.14,
                          spaceBefore=2, spaceAfter=5)
    sub = ParagraphStyle("s", parent=head, fontSize=BODY, leading=BODY * 1.2)
    quote = ParagraphStyle("q", parent=body, leftIndent=12)
    title, story = story_from(text, body, head, sub, quote)
    W, H = pagesize
    col_w = (W - 2 * margin - GUTTER * (cols - 1)) / cols

    def columns(top):
        return [frame(margin + i * (col_w + GUTTER), margin, col_w, top - margin) for i in range(cols)]

    def page_number(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(W / 2, margin / 2, str(doc.page))

    templates = [PageTemplate(id="rest", frames=columns(H - margin), onPage=page_number)]
    if title:
        title_h = 0.32 * inch
        first = [frame(margin, H - margin - title_h, W - 2 * margin, title_h)] + columns(H - margin - title_h)
        templates.insert(0, PageTemplate(id="first", frames=first, onPage=page_number))
        story = [title, NextPageTemplate("rest"), FrameBreak()] + story
    BaseDocTemplate(out, pagesize=pagesize, pageTemplates=templates).build(story)


def booklet(src, out):
    from pypdf import PageObject, PdfReader, PdfWriter, Transformation
    pages = PdfReader(src).pages
    w, h = A5
    n = -(-len(pages) // 4) * 4
    sheets = PdfWriter()
    for i in range(n // 2):
        # caras alternadas: frente (ultima, primera), dorso (segunda, penultima), ...
        left, right = (n - 1 - i, i) if i % 2 == 0 else (i, n - 1 - i)
        side = PageObject.create_blank_page(width=2 * w, height=h)
        for k, x in ((left, 0), (right, w)):
            if k < len(pages):
                side.merge_transformed_page(pages[k], Transformation().translate(x, 0))
        sheets.add_page(side)
    sheets.write(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", type=Path)
    ap.add_argument("-f", "--formato", choices=["columnas", "simple", "cuadernillo"], default="columnas")
    ap.add_argument("-o", "--salida", type=Path)
    a = ap.parse_args()
    out = str(a.salida or a.entrada.with_suffix(".pdf"))
    text = a.entrada.read_text(encoding="utf-8-sig")
    if a.formato == "cuadernillo":
        buf = io.BytesIO()
        render(text, buf, 1, A5, margin=0.5 * inch)
        buf.seek(0)
        booklet(buf, out)
    else:
        render(text, out, 2 if a.formato == "columnas" else 1, A4)
    print(out)


if __name__ == "__main__":
    main()
