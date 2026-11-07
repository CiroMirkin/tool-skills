# /// script
# dependencies = ["reportlab", "pypdf", "svglib"]
# ///
"""Convierte un archivo de texto en PDF.

  uv run pdf.py <entrada.txt> [-f columnas|simple|cuadernillo] [--color] [-o salida.pdf]

Texto de entrada: `# ` titulo, `## ` seccion, `### ` subseccion, parrafos separados por una
linea en blanco, bloques de `- ` vinetas, bloques de `> ` cita (sangrados), y `**negrita**`,
`*italica*` y `[texto](url)` dentro del texto. El resto se copia tal cual.

Un bloque `![epigrafe](diagrama.svg)` inserta un diagrama centrado en la pagina, con la ruta
relativa al archivo de entrada. En dos columnas interrumpe ambas: el texto anterior se reparte
parejo arriba y el siguiente sigue debajo. Sin --color, un SVG con colores es un error.

Un bloque de tabla (`| a | b |`, con `|---|---|` como segunda linea) ocupa todo el ancho, igual que
un diagrama. Se corta entre filas, tras MIN_LINES filas o mas, y repite el encabezado en la pagina
siguiente.

Cada `## ` y `### ` lleva en el margen su numero de seccion (1, 1.1, ...), para poder citarla.

Un bloque que no llega a mostrar MIN_LINES lineas empieza en la columna o pagina siguiente, y un
titulo (o un parrafo todo en negrita) va pegado al comienzo de lo que le sigue. Si aun asi una
pagina termina con un titulo o un bloque recien empezado, el script sale con error.

  columnas     A4, dos columnas, justificado (por defecto)
  simple       A4, una columna, justificado
  cuadernillo  paginas A5 impuestas de a dos por hoja A4 apaisada, en orden de cuadernillo:
               imprimir doble faz volteando por el borde corto, doblar al medio
"""
import argparse, io, re
from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import BalancedColumns, BaseDocTemplate, Flowable, Frame, FrameBreak, NextPageTemplate, PageTemplate, Paragraph, Table
from svglib.svglib import svg2rlg

MARGIN, GUTTER, BODY, HEAD = 0.6 * inch, 0.3 * inch, 12, 14
NEEDED = 72  # lo minimo que debe quedar en la pagina para empezar el texto siguiente
MIN_LINES = 3  # lineas que un bloque cortado debe mostrar antes del corte
REF_SIZE, REF_ALPHA, REF_GAP = 7, 0.45, 6  # numero de seccion en el margen
CELL, CELL_PAD = BODY - 2, 5
LAST_DRAWN = {}  # pagina -> ultimo elemento dibujado en ella


# caracteres que Helvetica no tiene
MISSING = {"→": "->", "←": "<-", "≥": ">=", "≤": "<=", "≠": "!="}


def inline(s):
    for c, r in MISSING.items():
        s = s.replace(c, r)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2" color="#1a5fb4">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)


class Block(Paragraph):
    def split(self, aW, aH):
        return [] if aH < MIN_LINES * self.style.leading else super().split(aW, aH)

    def draw(self):
        LAST_DRAWN[self.canv.getPageNumber()] = self
        super().draw()


class Head(Block):
    """Titulo o rotulo: va pegado a lo que le sigue. `ref` es su numero de seccion."""
    ref = None

    def draw(self):
        if self.ref:
            self.draw_ref()
        super().draw()

    def draw_ref(self):
        """En el margen de la pagina mas cercano, sobre la linea base de la primera linea. Va antes
        que el titulo para que al extraer el texto del PDF quede "2.1 Titulo"."""
        c = self.canv
        y = self.height - self.style.fontSize
        c.saveState()
        c.setFont("Helvetica", REF_SIZE)
        c.setFillAlpha(REF_ALPHA)
        if c.absolutePosition(0, 0)[0] > c._pagesize[0] / 2:
            c.drawString(self.width + REF_GAP, y, self.ref)
        else:
            c.drawRightString(-REF_GAP, y, self.ref)
        c.restoreState()


class Kept(Flowable):
    """Titulos con lo que les sigue. Se corta como su ultimo elemento, nunca antes de el."""

    def __init__(self, heads, next):
        super().__init__()
        self.heads, self.next = heads, next

    def getSpaceBefore(self):
        return self.heads[0].getSpaceBefore()

    def getSpaceAfter(self):
        return self.next.getSpaceAfter()

    def layout(self, width):
        """Cada titulo con la altura a la que termina, medida desde arriba."""
        y, out = 0, []
        for head, following in zip(self.heads, self.heads[1:] + [self.next]):
            y += head.wrap(width, 1000)[1]
            out.append((head, y))
            y += max(head.getSpaceAfter(), following.getSpaceBefore())
        return out, y

    def wrap(self, aW, aH):
        self.width = aW
        self.heads_h = self.layout(aW)[1]
        self.height = self.heads_h + self.next.wrapOn(self.canv, aW, aH - self.heads_h)[1]
        return aW, self.height

    def split(self, aW, aH):
        heads_h = self.layout(aW)[1]
        parts = self.next.splitOn(self.canv, aW, aH - heads_h)
        if not parts:
            return []
        first = Kept(self.heads, parts[0])
        first.canv = self.canv
        first.wrap(aW, aH)
        del first.canv
        return [first, *parts[1:]]

    def draw(self):
        # si lo que sigue se centra en la pagina, los titulos bajan con el
        pad = getattr(self.next, "pad", 0)
        for head, y in self.layout(self.width)[0]:
            head.drawOn(self.canv, 0, self.height - y - pad)
        self.next.drawOn(self.canv, 0, 0)


def keep_with_next(story):
    out, heads = [], []
    for f in story:
        if isinstance(f, Head):
            heads.append(f)
        elif heads:
            out.append(Kept(heads, f))
            heads = []
        else:
            out.append(f)
    return out + heads


def check_page_ends():
    problems = []
    for page in sorted(LAST_DRAWN)[:-1]:
        f = LAST_DRAWN[page]
        if isinstance(f, Head):
            problems.append(f"pagina {page}: termina con el titulo \"{f.getPlainText()}\"")
        elif isinstance(f, Block) and getattr(f, "_JustifyLast", 0) and len(f.blPara.lines) < MIN_LINES:
            problems.append(f"pagina {page}: bloque cortado tras {len(f.blPara.lines)} lineas: \"{f.getPlainText()[:60]}\"")
    if problems:
        raise SystemExit("cortes al final de pagina:\n" + "\n".join(problems))


def has_color(node):
    for attr in ("fillColor", "strokeColor"):
        c = getattr(node, attr, None)
        if c is not None and max(c.red, c.green, c.blue) - min(c.red, c.green, c.blue) > 0.01:
            return True
    return any(has_color(child) for child in getattr(node, "contents", []))


def diagram(path, caption, max_w, max_h, color, style):
    drawing = svg2rlg(str(path))
    if drawing is None:
        raise SystemExit(f"no se pudo leer el SVG: {path}")
    if not color and has_color(drawing):
        raise SystemExit(f"{path} tiene colores: redibujalo en grises o pasa --color")
    k = min(1, max_w / drawing.width, max_h / drawing.height)
    drawing.scale(k, k)
    drawing.width, drawing.height = drawing.width * k, drawing.height * k
    return drawing, Paragraph(inline(caption), style) if caption else None


class Figures(Flowable):
    """Diagramas apilados que no se separan. Si lo que sigue no entra en el resto de la pagina,
    se centran en ese espacio."""
    GAP, AFTER = 6, 8
    spaceBefore = spaceAfter = 10

    def __init__(self, figures, page_h):
        super().__init__()
        self.figures, self.page_h, self.last = figures, page_h, False

    def height_for(self, width):
        h = 0
        for drawing, caption in self.figures:
            h += 2 * self.GAP + drawing.height
            if caption:
                h += caption.wrap(width, 1000)[1] + self.AFTER
        return h

    def wrap(self, aW, aH):
        self.width, self.content_h = aW, self.height_for(aW)
        left = aH - self.content_h
        self.pad = left / 2 if 0 < left and (self.last or left < NEEDED) else 0
        return aW, self.content_h + 2 * self.pad

    def split(self, aW, aH):
        if self.height_for(aW) <= self.page_h or len(self.figures) == 1:
            return []
        parts = [Figures([f], self.page_h) for f in self.figures]
        parts[-1].last = self.last
        return parts

    def draw(self):
        LAST_DRAWN[self.canv.getPageNumber()] = self
        y = self.content_h + self.pad
        for drawing, caption in self.figures:
            y -= self.GAP + drawing.height
            drawing.drawOn(self.canv, (self.width - drawing.width) / 2, y)
            y -= self.GAP
            if caption:
                h = caption.wrap(self.width, 1000)[1]
                y -= h
                caption.drawOn(self.canv, 0, y)
                y -= self.AFTER


class Grid(Table):
    """Tabla de ancho completo. Cortada, muestra al menos MIN_LINES filas antes del corte."""

    def split(self, aW, aH):
        parts = super().split(aW, aH)
        return parts if parts and parts[0]._nrows - 1 >= MIN_LINES else []

    def draw(self):
        LAST_DRAWN[self.canv.getPageNumber()] = self
        super().draw()


def table_rows(lines):
    """Las filas de un bloque `| a | b |` sin la linea separadora, o None si no es una tabla."""
    if len(lines) < 2 or "|" not in lines[0] or "|" not in lines[1]:
        return None
    if not re.fullmatch(r"\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?", lines[1]):
        return None
    rows = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l.strip("|"))] for l in lines[:1] + lines[2:]]
    n = max(map(len, rows))
    return [r + [""] * (n - len(r)) for r in rows]


def col_widths(rows, total):
    """Reparte todo el ancho segun el texto de cada columna, sin bajar de su palabra mas larga si se puede."""
    def width(s):
        return stringWidth(s, "Helvetica-Bold", CELL)

    # el texto visible: de un link cuenta el rotulo, no la url
    rows = [[re.sub(r"\[([^\]]+)\]\([^)\s]+\)", r"\1", c).replace("*", "") for c in row] for row in rows]
    full = [max(width(c) for c in col) + 2 * CELL_PAD for col in zip(*rows)]
    if sum(full) <= total:
        return [w * total / sum(full) for w in full]
    least = [max(width(w) for c in col for w in c.split() or [""]) + 2 * CELL_PAD for col in zip(*rows)]
    spare = total - sum(least)
    if spare <= 0:
        return [w * total / sum(least) for w in least]
    slack = sum(full) - sum(least)
    return [m + spare * (f - m) / slack for m, f in zip(least, full)]


def grid(rows, total, cell, head):
    data = [[Paragraph(inline(c), head if i == 0 else cell) for c in row] for i, row in enumerate(rows)]
    return Grid(data, colWidths=col_widths(rows, total), repeatRows=1, spaceBefore=16, spaceAfter=18, style=[
        ("BACKGROUND", (0, 0), (-1, 0), "#e6e6e6"),
        ("BACKGROUND", (0, 1), (-1, -1), "#ffffff"),
        ("GRID", (0, 0), (-1, -1), 0.5, "#999999"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), CELL_PAD),
        ("RIGHTPADDING", (0, 0), (-1, -1), CELL_PAD),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])


def bands(story, cols):
    """Reparte el texto entre diagramas y tablas en columnas parejas; cada uno queda entre dos tramos."""
    out, text = [], []

    def flush():
        if text:
            out.append(BalancedColumns(text[:], nCols=cols, needed=NEEDED, innerPadding=GUTTER, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0))
            text.clear()

    for f in story:
        if isinstance(f, (Figures, Grid)) or isinstance(f, Kept) and isinstance(f.next, (Figures, Grid)):
            flush()
            out.append(f)
        else:
            text.append(f)
    flush()
    return out


def story_from(text, body, head, sub, quote, figure, table, page_h):
    title, story = None, []
    section, subsection = 0, 0

    def numbered(style, ref, line):
        h = Head(inline(line), style)
        h.ref = ref
        return h

    for block in re.split(r"\n\s*\n", text.replace("\r", "").strip()):
        lines = [l.strip() for l in block.splitlines()]
        if all(re.match(r"[-*] ", l) for l in lines):
            story += [Block(inline(l[2:]), ParagraphStyle("l", parent=body, leftIndent=10), bulletText="•") for l in lines]
            continue
        rows = table_rows(lines)
        if rows:
            story.append(table(rows))
            continue
        line = " ".join(lines)
        fig = re.fullmatch(r"!\[(.*?)\]\((.+)\)", line)
        if fig:
            f = figure(*fig.groups())
            # diagramas seguidos van juntos, uno debajo del otro
            if story and isinstance(story[-1], Figures):
                story[-1].figures.append(f)
            else:
                story.append(Figures([f], page_h))
        elif all(l.startswith(">") for l in lines):
            story.append(Block(inline(" ".join(l[1:].strip() for l in lines)), quote))
        elif line.startswith("### "):
            subsection += 1
            story.append(numbered(sub, f"{section}.{subsection}", line[4:]))
        elif line.startswith("## "):
            section, subsection = section + 1, 0
            story.append(numbered(head, str(section), line[3:]))
        elif line.startswith("# ") and title is None and not story:
            title = Paragraph(inline(line[2:]), head)
        elif re.fullmatch(r"\*\*[^*]+\*\*", line):
            story.append(Head(inline(line), body))
        else:
            story.append(Block(inline(line), body))
    return title, story


def frame(x, y, w, h):
    return Frame(x, y, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)


def render(text, out, cols, pagesize, base, color, margin=MARGIN):
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=BODY, leading=BODY * 1.125,
                          alignment=TA_JUSTIFY, spaceAfter=5)
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=HEAD, leading=HEAD * 1.14,
                          spaceBefore=2, spaceAfter=5)
    sub = ParagraphStyle("s", parent=head, fontSize=BODY, leading=BODY * 1.2)
    quote = ParagraphStyle("q", parent=body, leftIndent=12)
    caption = ParagraphStyle("c", parent=body, fontName="Helvetica-Oblique", fontSize=BODY - 2,
                             leading=(BODY - 2) * 1.2, alignment=TA_CENTER, spaceAfter=8)
    cell = ParagraphStyle("td", fontName="Helvetica", fontSize=CELL, leading=CELL * 1.2, alignment=TA_LEFT)
    cell_head = ParagraphStyle("th", parent=cell, fontName="Helvetica-Bold")
    W, H = pagesize

    def table(rows):
        return grid(rows, W - 2 * margin, cell, cell_head)

    def figure(caption_text, path):
        return diagram(base / path, caption_text, W - 2 * margin, (H - 2 * margin) * 0.6, color, caption)

    title, story = story_from(text, body, head, sub, quote, figure, table, H - 2 * margin)
    if story and isinstance(story[-1], Figures):
        story[-1].last = True
    has_wide = any(isinstance(f, (Figures, Grid)) for f in story)
    story = keep_with_next(story)
    col_w = (W - 2 * margin - GUTTER * (cols - 1)) / cols

    def columns(top):
        return [frame(margin + i * (col_w + GUTTER), margin, col_w, top - margin) for i in range(cols)]

    def page_number(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(W / 2, margin / 2, str(doc.page))

    templates = [PageTemplate(id="rest", frames=columns(H - margin), onPage=page_number)]
    if cols > 1 and has_wide:
        templates = [PageTemplate(id="bands", frames=[Frame(margin, margin, W - 2 * margin, H - 2 * margin, 0, 0, 0, 0, id="full")], onPage=page_number)]
        story = ([title] if title else []) + bands(story, cols)
    elif title:
        title_h = 0.32 * inch
        first = [frame(margin, H - margin - title_h, W - 2 * margin, title_h)] + columns(H - margin - title_h)
        templates.insert(0, PageTemplate(id="first", frames=first, onPage=page_number))
        story = [title, NextPageTemplate("rest"), FrameBreak()] + story
    BaseDocTemplate(out, pagesize=pagesize, pageTemplates=templates).build(story)
    check_page_ends()


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
    ap.add_argument("--color", action="store_true", help="admite diagramas a color")
    ap.add_argument("-o", "--salida", type=Path)
    a = ap.parse_args()
    out = str(a.salida or a.entrada.with_suffix(".pdf"))
    text = a.entrada.read_text(encoding="utf-8-sig")
    base = a.entrada.resolve().parent
    if a.formato == "cuadernillo":
        buf = io.BytesIO()
        render(text, buf, 1, A5, base, a.color, margin=0.5 * inch)
        buf.seek(0)
        booklet(buf, out)
    else:
        render(text, out, 2 if a.formato == "columnas" else 1, A4, base, a.color)
    print(out)


if __name__ == "__main__":
    main()
