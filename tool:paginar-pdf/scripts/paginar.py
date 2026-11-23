# /// script
# dependencies = ["pymupdf"]
# ///
"""Pone 2 paginas de un PDF por cara de una hoja A4 apaisada, con una linea de corte al medio.

  uv run paginar.py <entrada.pdf> [--recortar] [-o salida.pdf]

Hoja k (de 0): frente [4k+1, 4k+3], dorso [4k+4, 4k+2] (al voltear la hoja por el borde corto, la 1 queda detras de la 2). Si faltan paginas para completar
la ultima hoja, el hueco queda en blanco.

De cada pagina se toma solo lo que cae dentro de su area de pagina (MediaBox), asi las marcas de
corte y registro de la imprenta, que viven afuera, no se imprimen. Entre las dos paginas va una
linea vertical gris oscuro de 1 pt para cortar la hoja despues de imprimirla.

Con --recortar se quita ademas el margen en blanco: se mide el area con texto de todas las paginas
del mismo tamano y todas se recortan igual (union), asi el texto queda del mismo tamano en todas.
"""
import argparse
import sys
from pathlib import Path

import pymupdf

W, H = 842.0, 595.0  # A4 apaisada, en puntos
MARGEN = 18.0
RESPIRO = 6.0  # puntos de blanco que se dejan alrededor del texto con --recortar
LINEA = 1.0
GRIS = (0.25, 0.25, 0.25)


def areas_de_texto(doc):
    """Por tamano de pagina, la union del area con texto (marcas y bordes quedan afuera)."""
    union = {}
    for pg in doc:
        palabras = pg.get_text("words")
        if not palabras:
            continue
        r = pg.rect
        a = pymupdf.Rect(
            min(w[0] for w in palabras), min(w[1] for w in palabras),
            max(w[2] for w in palabras), max(w[3] for w in palabras),
        )
        a = pymupdf.Rect(a.x0 - RESPIRO, a.y0 - RESPIRO, a.x1 + RESPIRO, a.y1 + RESPIRO) & r
        clave = (round(r.width), round(r.height))
        union[clave] = union[clave] | a if clave in union else a
    return union


def colocar(cara, doc, n, mitad, areas):
    """Dibuja la pagina n de `doc` en su mitad de la cara, escalada y centrada."""
    if n >= len(doc):
        return
    pg = doc[n]
    clip = areas.get((round(pg.rect.width), round(pg.rect.height)), pg.rect)
    caja = pymupdf.Rect(mitad * W / 2 + MARGEN, MARGEN, (mitad + 1) * W / 2 - MARGEN, H - MARGEN)
    cara.show_pdf_page(caja, doc, n, clip=clip)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("--recortar", action="store_true")
    ap.add_argument("-o", "--salida")
    a = ap.parse_args()

    entrada = Path(a.entrada)
    salida = Path(a.salida) if a.salida else entrada.with_name(entrada.stem + "-paginado.pdf")
    doc = pymupdf.open(entrada)
    if not len(doc):
        sys.exit("El PDF no tiene paginas.")
    areas = areas_de_texto(doc) if a.recortar else {}
    total = len(doc) + (-len(doc) % 4)

    out = pymupdf.open()
    for k in range(0, total, 4):
        for izq, der in ((k, k + 2), (k + 3, k + 1)):
            cara = out.new_page(width=W, height=H)
            colocar(cara, doc, izq, 0, areas)
            colocar(cara, doc, der, 1, areas)
            cara.draw_line((W / 2, 0), (W / 2, H), color=GRIS, width=LINEA)
    out.save(salida, deflate=True)
    print(f"{salida}: {total // 2} caras, {total // 4} hojas")


main()
