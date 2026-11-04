#!/usr/bin/env bash
# Instala (una sola vez) uv, ffsubsync y un ffmpeg estático. Imprime la ruta base;
# añade "$BASE/bin" al PATH y usa "$BASE/venv/bin/python".
# Si existe la instalación global (install-global.sh) la reutiliza; si no, usa ~/.cache/subtitulos.
set -euo pipefail
GLOBAL="$HOME/.local/share/subtitulos"
if [ -z "${SUBTITULOS_HOME:-}" ] && [ -x "$GLOBAL/venv/bin/ffsubsync" ]; then
  BASE="$GLOBAL"
else
  BASE="${SUBTITULOS_HOME:-$HOME/.cache/subtitulos}"
fi
mkdir -p "$BASE/bin"
export UV_CACHE_DIR="$BASE/uvcache"
if [ ! -x "$BASE/bin/uv" ]; then
  tmp=$(mktemp -d)
  curl -sL -m 120 https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz | tar xz -C "$tmp"
  cp "$tmp"/*/uv "$BASE/bin/" && rm -rf "$tmp"
fi
if [ ! -x "$BASE/venv/bin/ffsubsync" ]; then
  "$BASE/bin/uv" venv -q "$BASE/venv"
  VIRTUAL_ENV="$BASE/venv" "$BASE/bin/uv" pip install -q ffsubsync imageio-ffmpeg
fi
if [ ! -e "$BASE/bin/ffmpeg" ]; then
  ln -sf "$("$BASE/venv/bin/python" -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')" "$BASE/bin/ffmpeg"
fi
ln -sf "$BASE/venv/bin/ffsubsync" "$BASE/bin/ffsubsync"
echo "$BASE"
