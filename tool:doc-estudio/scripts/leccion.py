#!/usr/bin/env python3
"""Arma y comprueba una lección de doc-estudio. Solo usa la biblioteca estándar y curl.

  leccion.py armar <fuente.md> <leccion.md> --codigo <carpeta>
      Reemplaza cada línea @@ruta/al/archivo@@ por ese archivo, relativo a --codigo.

  leccion.py comprobar <leccion.md> --codigo <carpeta> [--sin-enlaces]
      Revisa que cada bloque de código esté en un archivo de --codigo, que existan las
      imágenes y tengan texto alternativo, que respondan los enlaces y sus anclas, que no
      queden marcadores ni rayas largas, y que la correcta del quiz no sea la más larga.
      Sale con código 1 si encuentra algún problema.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SIN_VERIFICAR = {"", "text", "bash", "sh", "console", "markdown", "md", "yaml", "json"}
BLOQUE = re.compile(r"^```([^\n]*)\n(.*?)^```", re.S | re.M)
INCLUSION = re.compile(r"^@@([^@\n]+)@@$", re.M)
ORDINALES = {"primera": 0, "segunda": 1, "tercera": 2, "cuarta": 3}
TOLERANCIA_QUIZ = 6


def normalizar(texto):
    return "\n".join(linea.rstrip() for linea in texto.strip("\n").splitlines())


def armar(fuente, salida, codigo):
    texto = fuente.read_text(encoding="utf-8")
    faltan = [r for r in INCLUSION.findall(texto) if not (codigo / r).is_file()]
    if faltan:
        sys.exit("no existen en --codigo: " + ", ".join(faltan))
    armado = INCLUSION.sub(lambda m: (codigo / m.group(1)).read_text(encoding="utf-8").rstrip("\n"), texto)
    salida.write_text(armado, encoding="utf-8")
    print(salida)


def revisar_codigo(md, codigo):
    archivos = []
    for ruta in codigo.rglob("*"):
        if ruta.is_file():
            try:
                archivos.append(normalizar(ruta.read_text(encoding="utf-8")))
            except UnicodeDecodeError:
                pass  # binarios de la compilación
    problemas, total = [], 0
    for info, cuerpo in BLOQUE.findall(md):
        partes = info.split()
        if (partes[0] if partes else "") in SIN_VERIFICAR:
            continue
        total += 1
        if not any(normalizar(cuerpo) in archivo for archivo in archivos):
            primera = normalizar(cuerpo).splitlines()[0] if cuerpo.strip() else ""
            problemas.append(f"bloque {info!r} sin archivo verificado: {primera[:70]}")
    print(f"código: {total} bloques revisados")
    return problemas


def revisar_imagenes(md, base):
    problemas = []
    for alt, ruta in re.findall(r"!\[(.*?)\]\((.+?)\)", md):
        if not alt.strip():
            problemas.append(f"imagen sin texto alternativo: {ruta}")
        if not (base / ruta.lstrip("/")).exists():
            problemas.append(f"imagen que no existe: {ruta}")
    return problemas


def revisar_enlaces(md):
    problemas = []
    urls = sorted(set(re.findall(r"\]\((https?://[^)\s]+)\)", md)))
    with tempfile.NamedTemporaryFile() as pagina:
        for url in urls:
            base, _, ancla = url.partition("#")
            resultado = subprocess.run(
                ["curl", "-sL", "-m", "40", "-A", "Mozilla/5.0", "-o", pagina.name, "-w", "%{http_code}", base],
                capture_output=True, text=True,
            )
            if resultado.stdout != "200":
                problemas.append(f"enlace con respuesta {resultado.stdout}: {url}")
            elif ancla and not re.fullmatch(r"L\d+(-L\d+)?", ancla):
                contenido = Path(pagina.name).read_text(encoding="utf-8", errors="replace")
                if not re.search(rf'(id|name)=["\']{re.escape(ancla)}["\']', contenido):
                    problemas.append(f"ancla que no aparece en la página: {url}")
    print(f"enlaces: {len(urls)} revisados")
    return problemas


def revisar_quiz(md):
    inicio = re.search(r"^## Quiz\s*$", md, re.M)
    if not inicio:
        return []
    fin = re.search(r"^## ", md[inicio.end():], re.M)
    quiz = md[inicio.end():inicio.end() + fin.start()] if fin else md[inicio.end():]
    problemas = []
    for numero, pregunta in enumerate(re.split(r"\n(?=\*\*\d+\. )", quiz)[1:], 1):
        opciones = [len(o) for o in re.findall(r"^- (.+)$", pregunta, re.M)]
        ordinal = re.search(r"La correcta es la (primera|segunda|tercera|cuarta)", pregunta)
        if len(opciones) != 4 or not ordinal:
            problemas.append(f"quiz {numero}: hacen falta 4 opciones y 'La correcta es la <ordinal>'")
            continue
        correcta = ORDINALES[ordinal.group(1)]
        otras = opciones[:correcta] + opciones[correcta + 1:]
        if opciones[correcta] > max(otras) + TOLERANCIA_QUIZ:
            problemas.append(f"quiz {numero}: la correcta se nota por el largo ({opciones})")
    return problemas


def comprobar(leccion, codigo, sin_enlaces):
    md = leccion.read_text(encoding="utf-8")
    problemas = revisar_codigo(md, codigo) + revisar_imagenes(md, leccion.parent) + revisar_quiz(md)
    if not sin_enlaces:
        problemas += revisar_enlaces(md)
    prosa = BLOQUE.sub("", md)
    if re.search("[—–]", prosa):
        problemas.append("quedan rayas largas en la prosa")
    if INCLUSION.search(md):
        problemas.append("quedan marcadores @@ sin reemplazar")
    if "[falta dato]" in md:
        problemas.append("queda algún [falta dato]")
    for problema in problemas:
        print("PROBLEMA:", problema)
    print(f"{len(problemas)} problemas")
    return 1 if problemas else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="accion", required=True)
    a = sub.add_parser("armar")
    a.add_argument("fuente", type=Path)
    a.add_argument("salida", type=Path)
    a.add_argument("--codigo", type=Path, required=True)
    c = sub.add_parser("comprobar")
    c.add_argument("leccion", type=Path)
    c.add_argument("--codigo", type=Path, required=True)
    c.add_argument("--sin-enlaces", action="store_true")
    args = ap.parse_args()
    if args.accion == "armar":
        armar(args.fuente, args.salida, args.codigo)
    else:
        sys.exit(comprobar(args.leccion, args.codigo, args.sin_enlaces))


if __name__ == "__main__":
    main()
