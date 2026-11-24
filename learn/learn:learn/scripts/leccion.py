#!/usr/bin/env python3
"""Arma y comprueba una lección de learn:learn. Necesita pygments:

  uv run --no-project --with pygments python leccion.py <orden> ...

  leccion.py armar <fuente.html> <leccion.html> [--proyecto DIR] [--ejemplo DIR] [--diagramas DIR]
      Reemplaza cada línea @@proyecto:ruta[:ini-fin]@@ y @@ejemplo:ruta[:ini-fin]@@ por ese código,
      copiado del archivo y resaltado, y cada @@svg:archivo.svg@@ por el diagrama en línea.
      Mete en la plantilla los estilos del resaltado.

  leccion.py ejemplo <carpeta>
      Revisa que la carpeta de práctica arranque sola: docker-compose.yml, README.md, package.json con
      los scripts preparar y test, y en el README los pasos de inicio y un comando por cada escalón
      (practica/NN-nombre). Sale con código 1 si falta algo.

  leccion.py comprobar <leccion.html> [--sin-enlaces]
      Revisa la estructura, que no queden marcadores, que sea un solo archivo, las anclas, los
      diagramas, las reglas de interfaz (sin "·", sin mayúsculas forzadas, sin rayas largas), la tarea y sus ayudas, y que los
      enlaces externos respondan. Sale con código 1 si encuentra algún problema.
"""
import argparse
import html
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

SECCIONES = ["resumen", "concepto", "practica", "codigo-proyecto", "codigo-ejemplo", "bugs", "tarea", "fuentes"]
INCLUSION = re.compile(r"^[ \t]*@@(proyecto|ejemplo|svg):([^@\n]+)@@[ \t]*$", re.M)
RANGO = re.compile(r"^(.*):(\d+)(?:-(\d+))?$")
MAYUSCULAS = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{3,}(?:\s+[A-ZÁÉÍÓÚÑ]{3,})+\b")
VOID = {"meta", "link", "input", "br", "hr", "img", "path", "rect", "circle", "line", "polygon", "polyline", "ellipse", "use", "stop"}
MIN_PROYECTO, MIN_EJEMPLO, MIN_EJERCICIOS, MIN_PASOS = 2, 2, 3, 3
MIN_ESCALONES, MAX_ESCALONES, MAX_FICTICIOS = 4, 6, 2


def git(proyecto, *args):
    r = subprocess.run(["git", "-C", str(proyecto), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def css_resaltado():
    from pygments.formatters import HtmlFormatter

    def reglas(estilo):
        salida = []
        for linea in HtmlFormatter(style=estilo).get_style_defs(".codigo").splitlines():
            if re.match(r"^\.codigo \.\w+ \{", linea) and not re.search(r"background|border", linea):
                salida.append(linea)
        return "\n".join(salida)

    return reglas("default") + "\n@media (prefers-color-scheme: dark) {\n" + reglas("monokai") + "\n}"


def bloque_codigo(origen, base, spec, proyecto):
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import TextLexer, get_lexer_for_filename
    from pygments.util import ClassNotFound

    m = RANGO.match(spec)
    ruta, ini, fin = (m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))) if m else (spec, None, None)
    archivo = base / ruta
    if not archivo.is_file():
        sys.exit(f"no existe {archivo}")
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    ini, fin = (ini or 1), (fin or len(lineas))
    if not 1 <= ini <= fin <= len(lineas):
        sys.exit(f"{ruta}: rango {ini}-{fin} fuera del archivo ({len(lineas)} líneas)")
    texto = "\n".join(lineas[ini - 1 : fin])
    try:
        lexer = get_lexer_for_filename(ruta)
    except ClassNotFound:
        lexer = TextLexer()
    marcado = highlight(texto, lexer, HtmlFormatter(nowrap=True)).rstrip("\n").split("\n")
    cuerpo = "\n".join(f'<span class="l" data-n="{ini + i}">{l}</span>' for i, l in enumerate(marcado))
    rango = f"línea {ini}" if ini == fin else f"líneas {ini} a {fin}"
    extra = ""
    if origen == "proyecto":
        commit = git(proyecto, "rev-parse", "--short", "HEAD")
        sucio = git(proyecto, "status", "--porcelain", "--", ruta)
        extra = f'<span class="commit">commit {commit}{", con cambios sin commitear" if sucio else ""}</span>' if commit else ""
    return (
        f'<figure class="codigo" data-origen="{origen}" data-ruta="{html.escape(ruta)}" data-lineas="{ini}-{fin}">\n'
        f'<figcaption><span class="ruta">{html.escape(ruta)}</span><span class="rango">{rango}</span>{extra}</figcaption>\n'
        f"<pre><code>{cuerpo}</code></pre>\n</figure>"
    )


def bloque_svg(base, nombre):
    archivo = base / nombre
    if not archivo.is_file():
        sys.exit(f"no existe {archivo}")
    svg = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", archivo.read_text(encoding="utf-8"))
    titulo = re.search(r"<title[^>]*>(.*?)</title>", svg, re.S)
    leyenda = f"\n<figcaption>{titulo.group(1)}</figcaption>" if titulo else ""
    tipo = "flujo" if nombre.startswith("flujo") else "secuencia" if nombre.startswith("secuencia") else "otro"
    return f'<figure class="diagrama" data-tipo="{tipo}">\n{svg.strip()}{leyenda}\n</figure>'


def marcar_lineas(texto):
    """Pone un puntito rojo en las líneas de cada modelo que las notas de abajo nombran (Línea 8, Líneas 6 y 7, Líneas 7 a 9)."""

    def lineas_citadas(notas):
        citadas = set()
        for li in re.findall(r"<li>(.*?)</li>", notas, re.S):
            m = re.match(r"\s*Líneas?\s+(\d+)(?:\s+(?:y|a)\s+(\d+))?", li)
            if not m:
                continue
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            citadas.update(range(a, b + 1) if " a " in m.group(0) else {a, b})
        return citadas

    def marcar(m):
        citadas = lineas_citadas(m.group(2))
        figura = re.sub(
            r'<span class="l(?: marca)?" data-n="(\d+)">',
            lambda x: f'<span class="l{" marca" if int(x.group(1)) in citadas else ""}" data-n="{x.group(1)}">',
            m.group(1),
        )
        return figura + m.group(2)

    return re.sub(r'(<figure class="codigo"[^>]*data-ruta="modelo/.*?</figure>)(\s*<ul>.*?</ul>)', marcar, texto, flags=re.S)


def armar(fuente, salida, proyecto, ejemplo, diagramas):
    texto = fuente.read_text(encoding="utf-8")

    def sustituir(m):
        tipo, spec = m.group(1), m.group(2)
        if tipo == "svg":
            return bloque_svg(diagramas, spec)
        base = proyecto if tipo == "proyecto" else ejemplo
        if base is None:
            sys.exit(f"falta --{tipo} para {spec}")
        return bloque_codigo(tipo, base, spec, proyecto)

    armado = marcar_lineas(INCLUSION.sub(sustituir, texto))
    armado = armado.replace("/*PYGMENTS*/", css_resaltado())
    salida.write_text(armado, encoding="utf-8")
    print(salida)


class Revisor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.anclas, self.externos, self.enlaces = set(), [], [], []
        self.problemas = []
        self.texto = []  # (texto, dentro_de_codigo)
        self.pila = []
        self.svgs = []  # [tiene_role_img, tiene_title]
        self.figuras = []  # (clase, atributos)

    def error(self, msg):
        self.problemas.append(msg)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.pila.append(tag)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            if a["href"].startswith("#"):
                self.anclas.append(a["href"][1:])
            elif a["href"].startswith("http"):
                self.enlaces.append(a["href"])
        if tag == "script" and a.get("src"):
            self.externos.append(f"<script src={a['src']}>")
        if tag == "link" and (a.get("href") or "").startswith("http"):
            self.externos.append(f"<link href={a['href']}>")
        if tag == "img" and (a.get("src") or "").startswith("http"):
            self.externos.append(f"<img src={a['src']}>")
        if tag == "svg":
            self.svgs.append([a.get("role") == "img", False])
        if tag == "title" and "svg" in self.pila and self.svgs:
            self.svgs[-1][1] = True
        if tag == "figure":
            self.figuras.append((a.get("class", ""), a))

    def handle_endtag(self, tag):
        if tag not in self.pila:
            return
        while self.pila:
            if self.pila.pop() == tag:
                break

    def handle_data(self, data):
        if self.pila and self.pila[-1] in ("style", "script", "title") and "svg" not in self.pila:
            return
        self.texto.append((data, "pre" in self.pila or "code" in self.pila))


def seccion(texto, id_):
    m = re.search(rf'<section id="{id_}".*?</section>', texto, re.S)
    return m.group(0) if m else ""


def comprobar(ruta, con_enlaces):
    texto = ruta.read_text(encoding="utf-8")
    r = Revisor()
    r.feed(texto)
    p = r.problemas
    sin_codigo = re.sub(r"<pre.*?</pre>", "", texto, flags=re.S)

    for marca in ("{{", "@@", "<!--", "TODO", "[falta dato]"):
        if marca in sin_codigo:
            p.append(f"queda el marcador {marca!r}")
    for s in SECCIONES:
        if f'id="{s}"' not in texto:
            p.append(f"falta la sección #{s}")
    for a in r.anclas:
        if a not in r.ids:
            p.append(f"ancla rota: #{a}")
    for e in r.externos:
        p.append(f"no es un solo archivo, depende de {e}")
    if "@import" in texto:
        p.append("no es un solo archivo, usa @import")

    if "·" in sin_codigo:
        p.append('hay un "·"')
    if "—" in sin_codigo:
        p.append("hay una raya larga")
    for regla in ("text-transform", "uppercase", "letter-spacing"):
        if regla in sin_codigo:
            p.append(f"mayúsculas forzadas: aparece {regla}")
    visibles = [t for t, en_codigo in r.texto if not en_codigo]
    for t in visibles:
        for hallado in MAYUSCULAS.findall(t):
            p.append(f"texto en mayúsculas sostenidas: {hallado!r}")

    for i, (rol, titulo) in enumerate(r.svgs, 1):
        if not rol or not titulo:
            p.append(f"el diagrama {i} necesita role=\"img\" y un <title>")

    def figuras(clase, **attrs):
        return [a for c, a in r.figuras if clase in c.split() and all(a.get(k) == v for k, v in attrs.items())]

    if len(figuras("codigo", **{"data-origen": "proyecto"})) < MIN_PROYECTO:
        p.append(f"menos de {MIN_PROYECTO} fragmentos del proyecto")
    if len(figuras("codigo", **{"data-origen": "ejemplo"})) < MIN_EJEMPLO:
        p.append(f"menos de {MIN_EJEMPLO} fragmentos del ejemplo ficticio")
    for tipo in ("flujo", "secuencia"):
        if not figuras("diagrama", **{"data-tipo": tipo}):
            p.append(f"falta un diagrama de {tipo}")

    bugs = seccion(texto, "bugs")
    if len(re.findall(r'class="ejercicio"', bugs)) < MIN_EJERCICIOS:
        p.append(f"menos de {MIN_EJERCICIOS} ejercicios de error")
    if len(re.findall(r'<details class="respuesta"', bugs)) != len(re.findall(r'class="ejercicio"', bugs)):
        p.append("cada ejercicio necesita su <details class=\"respuesta\">")

    practica = seccion(texto, "practica")
    escalones = re.findall(r'<div class="escalon"[^>]*>.*?(?=<div class="escalon"|\Z)', practica, re.S)
    if not MIN_ESCALONES <= len(escalones) <= MAX_ESCALONES:
        p.append(f"la práctica tiene {len(escalones)} escalones, debe tener de {MIN_ESCALONES} a {MAX_ESCALONES}")
    ficticios = len(re.findall(r'data-dominio="ficticio"', practica))
    if not 1 <= ficticios <= min(MAX_FICTICIOS, max(1, len(escalones) // 3)):
        p.append(f"la práctica tiene {ficticios} escalones de dominio ficticio, debe haber 1 o 2 y no más de un tercio")
    if escalones and not re.search(r'data-dominio="proyecto"', escalones[0]):
        p.append("el primer escalón de la práctica debe ser del dominio del proyecto")
    for i, esc in enumerate(escalones, 1):
        if 'class="comprobacion"' not in esc or "<code>" not in re.search(r'class="comprobacion".*?</p>', esc, re.S).group(0):
            p.append(f"el escalón {i} necesita un <p class=\"comprobacion\"> con el comando")
        if not re.search(r'class="etiqueta">(Ejecutar|Completar|Escribir)<', esc):
            p.append(f"el escalón {i} necesita su clase (Ejecutar, Completar o Escribir)")
        if not re.search(r'href="#modelo-\d+"', esc):
            p.append(f"el escalón {i} necesita un enlace a su modelo, que vive en el concepto (href=\"#modelo-N\")")
        if "<pre" in esc or 'class="codigo"' in esc or "@@" in esc:
            p.append(f"el escalón {i} lleva código: el modelo vive en el concepto y la solución queda fuera de la lección")
    concepto = seccion(texto, "concepto")
    ids_modelo = set(re.findall(r'id="(modelo-\d+)"', concepto))
    modelos = [a for c, a in r.figuras if "codigo" in c.split() and a.get("data-ruta", "").startswith("modelo/")]
    if len(modelos) < len(escalones) or len(ids_modelo) < len(escalones):
        p.append(f"el concepto trae {len(modelos)} modelos con {len(ids_modelo)} anclas, debe haber uno por escalón ({len(escalones)}), cada uno con su id=\"modelo-N\"")
    for destino in set(re.findall(r'href="#(modelo-\d+)"', practica)) - ids_modelo:
        p.append(f"un escalón enlaza a #{destino} y el concepto no tiene ese modelo")
    if "<table" not in practica:
        p.append("la práctica necesita la tabla pieza a escalón")
    proy = seccion(texto, "codigo-proyecto")
    if len(re.findall(r'class="piezas"', proy)) < len(re.findall(r'data-origen="proyecto"', proy)):
        p.append("cada fragmento del proyecto necesita su línea <p class=\"piezas\">")
    for ancla in re.findall(r'<p class="piezas">.*?</p>', proy, re.S):
        if 'href="#escalon-' not in ancla:
            p.append("una línea de piezas no enlaza a ningún escalón")

    tarea = seccion(texto, "tarea")
    pasos = re.findall(r"<li>.*?</li>", re.search(r'<ol class="pasos">.*?</ol>', tarea, re.S).group(0), re.S) if re.search(r'<ol class="pasos">', tarea) else []
    if len(pasos) < MIN_PASOS:
        p.append(f"la tarea tiene menos de {MIN_PASOS} pasos")
    for i, paso in enumerate(pasos, 1):
        if len(re.findall(r'<details class="pista"', paso)) < 2:
            p.append(f"el paso {i} de la tarea necesita al menos 2 ayudas")
    for pista in re.findall(r'<details class="pista".*?</details>', practica + tarea, re.S):
        if "<pre" in pista or 'class="codigo"' in pista or "@@" in pista:
            p.append("una ayuda lleva código: manda a releer o pregunta, no da la solución")
    if "Cómo saber que terminaste" not in tarea:
        p.append("la tarea no dice cómo saber que terminaste")
    if not re.search(r"<a href=\"https?://", seccion(texto, "fuentes")):
        p.append("las fuentes no traen ningún enlace")

    if con_enlaces:
        for url in dict.fromkeys(r.enlaces):
            codigo = ""
            for metodo in ("-I", "-r0-0"):
                c = subprocess.run(
                    ["curl", "-sL", "-m", "30", "-A", "Mozilla/5.0", metodo, "-o", "/dev/null", "-w", "%{http_code}", url],
                    capture_output=True, text=True,
                ).stdout
                codigo = c
                if c.startswith(("2", "3")):
                    break
            if not codigo.startswith(("2", "3")):
                p.append(f"el enlace no responde ({codigo or 'sin respuesta'}): {url}")

    if p:
        print("Problemas:")
        for x in dict.fromkeys(p):
            print("  -", x)
        sys.exit(1)
    print("Sin problemas.")


def comprobar_ejemplo(carpeta):
    import json

    p = []
    for archivo in ("docker-compose.yml", "README.md", "package.json"):
        if not (carpeta / archivo).is_file():
            p.append(f"falta {archivo}")
    readme = (carpeta / "README.md").read_text(encoding="utf-8") if (carpeta / "README.md").is_file() else ""
    if (carpeta / "package.json").is_file():
        scripts = json.loads((carpeta / "package.json").read_text(encoding="utf-8")).get("scripts", {})
        for nombre in ("preparar", "test"):
            if nombre not in scripts:
                p.append(f"package.json no tiene el script {nombre}")
        if "preparar" in scripts and "docker compose" not in scripts["preparar"]:
            p.append("el script preparar no levanta la base con docker compose")
    for paso in ("npm install", "npm run preparar"):
        if paso not in readme:
            p.append(f"el README no dice {paso!r}")
    escalones = sorted(d.name for d in (carpeta / "practica").glob("[0-9][0-9]-*") if d.is_dir())
    if not escalones:
        p.append("no hay escalones en practica/NN-nombre")
    for nombre in escalones:
        numero = nombre[:2]
        if f"npx vitest run practica/{numero}" not in readme:
            p.append(f"el README no trae el comando del escalón {numero} (npx vitest run practica/{numero})")
        if nombre not in readme:
            p.append(f"el README no nombra la carpeta practica/{nombre}")
        if not list((carpeta / "practica" / nombre).glob("*.test.ts")):
            p.append(f"el escalón {nombre} no tiene su test")
    if p:
        print("Problemas:")
        for x in dict.fromkeys(p):
            print("  -", x)
        sys.exit(1)
    print(f"Sin problemas: {len(escalones)} escalones con su comando en el README.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    a = sub.add_parser("armar")
    a.add_argument("fuente", type=Path)
    a.add_argument("salida", type=Path)
    a.add_argument("--proyecto", type=Path)
    a.add_argument("--ejemplo", type=Path)
    a.add_argument("--diagramas", type=Path, default=Path("."))
    e = sub.add_parser("ejemplo")
    e.add_argument("carpeta", type=Path)
    c = sub.add_parser("comprobar")
    c.add_argument("leccion", type=Path)
    c.add_argument("--sin-enlaces", action="store_true")
    args = ap.parse_args()
    if args.orden == "armar":
        armar(args.fuente, args.salida, args.proyecto, args.ejemplo, args.diagramas)
    elif args.orden == "ejemplo":
        comprobar_ejemplo(args.carpeta)
    else:
        comprobar(args.leccion, not args.sin_enlaces)
