#!/usr/bin/env bash
# Opcional: instala las herramientas de forma persistente en ~/.local/share/subtitulos
# y enlaza ffmpeg, ffsubsync y uv en ~/.local/bin para usarlas desde cualquier terminal.
# Después setup.sh detecta esta instalación y no descarga nada. Sin sudo.
set -euo pipefail
BASE=$(SUBTITULOS_HOME="$HOME/.local/share/subtitulos" bash "$(dirname "$0")/setup.sh")
mkdir -p "$HOME/.local/bin"
for t in ffmpeg ffsubsync uv; do
  if [ -e "$HOME/.local/bin/$t" ] && [ ! -L "$HOME/.local/bin/$t" ]; then
    echo "aviso: ~/.local/bin/$t ya existe y no es un enlace; no lo toco" >&2
  else
    ln -sfn "$BASE/bin/$t" "$HOME/.local/bin/$t"
  fi
done
echo "$BASE"
