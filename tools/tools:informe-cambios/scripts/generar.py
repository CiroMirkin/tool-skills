#!/usr/bin/env python3
"""Genera los PDF de un informe de cambios: uno general y uno por etapa.

Uso: generar.py informe.md --cliente "Nombre"

Salida, en la carpeta entrega/ junto al .md (el .md de origen no se toca):
  informe.md y informe.pdf       el informe completo, sin marcas {{}}
  etapa-N.md y etapa-N.pdf       una etapa: resumen, «De dónde salen los números» y la etapa

Formato del .md (ver SKILL.md):
  # Título
  ## Resumen                     lista numerada por etapa, cada ítem termina en [Ver](#mE-N)
  ## De dónde salen los números
  ## Etapa 1. Nombre: bajada     cada etapa con ### 1.1 Título y su tabla
  ## Otras secciones             solo van en el PDF completo
  {{2.2}}                        referencia a un ítem de otra etapa
"""
import argparse, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
AVISO = "mejora grande que estoy documentando"


def secciones(texto):
    """Parte el texto en bloques que empiezan en cada «## »."""
    return re.split(r"(?m)^(?=## )", texto)


def etapa_de(bloque):
    m = re.match(r"## Etapa (\d+)\. (.+)", bloque)
    return (int(m.group(1)), m.group(2).strip()) if m else None


def resumen_de_etapa(resumen, n):
    """Los ítems del resumen cuyo enlace apunta a la etapa n, con su número."""
    items = re.findall(rf"(?m)^\d+\. .*\(#m{n}-\d+\).*$", resumen)
    return "\n".join(items)


def pdf(md, salida, kicker, descripcion):
    env = dict(os.environ, COVER_KICKER=kicker, PIE_SIMPLE="1", PAGINAR="1", DESCRIPCION=descripcion)
    subprocess.run([os.path.join(AQUI, "md-a-pdf.sh"), md, salida], check=True, env=env)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("informe")
    ap.add_argument("--cliente", required=True)
    a = ap.parse_args()

    informe = os.path.abspath(a.informe)
    texto = open(informe, encoding="utf8").read()
    bloques = secciones(texto)
    cabecera = bloques[0].strip()

    resumen = next((b for b in bloques if b.startswith("## Resumen")), None)
    fuente = next((b for b in bloques if b.startswith("## De dónde salen los números")), None)
    if not resumen or not fuente:
        sys.exit("faltan «## Resumen» o «## De dónde salen los números» en el informe")
    etapas = {n: (nombre, b) for b in bloques if (e := etapa_de(b)) for n, nombre in [e]}
    if not etapas:
        sys.exit("no hay ninguna «## Etapa N. Nombre» en el informe")

    ids = set(re.findall(r"(?m)^### (\d+\.\d+) ", texto))
    for ref in re.findall(r"\{\{(\d+\.\d+)\}\}", texto):
        if ref not in ids:
            sys.exit(f"la referencia {{{{{ref}}}}} no apunta a ningún ítem")
    for enlace in re.findall(r"\(#m(\d+-\d+)\)", resumen):
        if enlace.replace("-", ".") not in ids:
            sys.exit(f"el resumen enlaza a #m{enlace}, que no existe como ### {enlace.replace('-', '.')}")

    # PDF completo: las referencias muestran el número del ítem.
    completo = re.sub(r"\{\{(\d+\.\d+)\}\}", r"\1", texto)
    carpeta = os.path.join(os.path.dirname(informe), "entrega")
    os.makedirs(carpeta, exist_ok=True)
    md_completo = os.path.join(carpeta, "informe.md")
    open(md_completo, "w", encoding="utf8").write(completo)
    pdf(md_completo, md_completo[:-3] + ".pdf", a.cliente, cabecera.lstrip("# ").strip())

    # Un PDF por etapa. Las referencias a otra etapa pasan a un aviso en palabras.
    for n, (nombre, bloque) in sorted(etapas.items()):
        titulo = nombre.split(":")[0].strip()
        propios = set(re.findall(rf"(?m)^### ({n}\.\d+) ", bloque))
        cuerpo = re.sub(r"\{\{(\d+\.\d+)\}\}",
                        lambda m: m.group(1) if m.group(1) in propios else AVISO, bloque)
        cuerpo = re.sub(r"(?m)^## Etapa \d+\. ", "## ", cuerpo, count=1)
        cuerpo = re.sub(rf"(?m)^## {re.escape(titulo)}: (.)",
                        lambda m: f"## {titulo}. {m.group(1).upper()}", cuerpo, count=1)
        lista = resumen_de_etapa(resumen, n)
        if not lista:
            sys.exit(f"el resumen no tiene ítems que enlacen a la etapa {n}")
        md = f"# {titulo}\n\n## Resumen\n\n{lista}\n\n{fuente.strip()}\n\n{cuerpo.strip()}\n"
        ruta = os.path.join(carpeta, f"etapa-{n}.md")
        open(ruta, "w", encoding="utf8").write(md)
        pdf(ruta, ruta[:-3] + ".pdf", a.cliente, titulo)


if __name__ == "__main__":
    main()
