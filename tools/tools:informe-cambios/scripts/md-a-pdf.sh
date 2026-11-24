#!/usr/bin/env bash
# Pasa un .md a PDF con pdfcn + Takumi y el estilo escandinavo (src/build.tsx).
#
# Uso:
#   ./md-a-pdf.sh entrada.md [salida.pdf]
#   ./md-a-pdf.sh -w entrada.md        vuelve a generar cada vez que se guarda el .md
#
# Variables: COVER_KICKER (rótulo de la portada), PIE_SIMPLE=1 (pie con solo el número),
# PAGINAR=1 (portada pegada arriba y contenido pegado al margen), DESCRIPCION (metadato del PDF).
#
# Necesita internet (baja Inter y JetBrains Mono de Google Fonts) y node_modules
# instalado en esta carpeta (npm install).
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCH=0
if [[ "${1:-}" == "-w" ]]; then WATCH=1; shift; fi

[[ -n "${1:-}" ]] || { echo "uso: md-a-pdf.sh [-w] entrada.md [salida.pdf]" >&2; exit 1; }
ENTRADA="$(realpath "$1")"
SALIDA="$(realpath -m "${2:-${ENTRADA%.md}.pdf}")"

[[ -f "$ENTRADA" ]] || { echo "no existe: $ENTRADA" >&2; exit 1; }
[[ -d "$AQUI/node_modules" ]] || (cd "$AQUI" && npm install --no-audit --no-fund --silent)

generar() {
  (cd "$AQUI" && node node_modules/tsx/dist/cli.mjs src/build.tsx "$ENTRADA" "$SALIDA")
  if command -v pdfinfo >/dev/null; then
    echo "$SALIDA ($(pdfinfo "$SALIDA" 2>/dev/null | awk '/^Pages:/{print $2}') páginas)"
  else
    echo "$SALIDA"
  fi
}

generar
(( WATCH )) || exit 0

echo "mirando $ENTRADA (Ctrl+C para salir)"
ultimo="$(stat -c %Y "$ENTRADA")"
while sleep 1; do
  actual="$(stat -c %Y "$ENTRADA")"
  if [[ "$actual" != "$ultimo" ]]; then
    ultimo="$actual"
    generar || echo "falló la generación, sigo mirando" >&2
  fi
done
