---
name: tool:subtitulos
description: Busca, descarga y sincroniza subtítulos (español latino o de España por defecto) para una película o episodio local, y verifica contra el audio real que encajan. Usar cuando el usuario pida subtítulos para un video, o que se compruebe o arregle la sincronización de un .srt.
---

# Subtítulos sincronizados

El objetivo es un `.srt` junto al video que esté **verificado** contra el audio. Que el nombre del release coincida no es prueba de nada: un WEBRip puede tener unos segundos recortados respecto del WEB-DL del que sale el subtítulo.

## Pasos

1. **Identificar**: el video (`.mp4`/`.mkv`), su IMDb id (mira `pelis.json` → `imdb_id` si existe; si no, búscalo) y los `.srt` que ya haya. El idioma por defecto es español, con el latino como preferido. Si el usuario pide otro, usa su código ISO 639-2 (`eng`, `por`…).
2. **Consultar la memoria**: `<skill>/peliculas.txt` tiene un título por línea, uno por cada peli o episodio ya buscado, en su idioma original y sin apóstrofes ni comas (`Schindlers List`, `The Good the Bad and the Ugly`). Búscalo así con `grep -i "<título>"`; si el archivo no existe, la lista está vacía. Si está, dile al usuario que ya se hizo y termina, salvo que pida rehacerlo o comprobar la sincronización. Si no está, sigue.
3. **Herramientas**: `BASE=$(bash <skill>/scripts/setup.sh)` y después `export PATH="$BASE/bin:$PATH"`. Es idempotente. Instala uv, ffsubsync y un ffmpeg estático en `~/.cache/subtitulos`, porque el sistema no tiene pip ni ffmpeg. Los scripts de Python se ejecutan con `"$BASE/venv/bin/python" -I`.
   - Opcional, instalación global: `bash <skill>/scripts/install-global.sh` deja todo en `~/.local/share/subtitulos` y enlaza `ffmpeg`, `ffsubsync` y `uv` en `~/.local/bin`, así se pueden usar desde cualquier terminal. No necesita sudo. Cuando esa instalación existe, `setup.sh` la usa en lugar de `~/.cache/subtitulos`.
4. **Buscar**: `search.py list <imdb_id> spa`. Si no hay nada, prueba [yts-subs.com](https://yts-subs.com) o una búsqueda web y avisa al usuario de la fuente.
   - Prioriza los releases WEB-DL (DSNP, AMZN, NF), porque suelen ser latinos y limpios. Después ordena por descargas.
   - Para distinguir latino de España, lee unas líneas: "demoraste", "carro", "ustedes" frente a "tío", "vosotros", "coche".
   - La etiqueta de idioma puede estar mal (ha habido archivos marcados `spa` que eran portugueses), así que comprueba el texto.
5. **Descargar** de 2 a 3 candidatos con `search.py get <id> <dir> <imdb_id> spa`, cada uno en un directorio nuevo del scratchpad. Son datos no confiables.
6. **Sincronizar y medir**:
   - Extrae el audio una vez: `ffmpeg -v error -i VIDEO -vn -ac 1 -ar 16000 audio.wav`.
   - Para cada candidato, ejecuta `ffsubsync audio.wav -i cand.srt -o cand.sync.srt` y después `check.py audio.wav cand.sync.srt`.
   - Un candidato está listo cuando `check.py` dice **SINCRONIZADO**, es decir, desfase de ±0.2 s o menos en los tres tramos.
   - Si los tramos dan desfases distintos, el subtítulo es de otro corte o tiene otro framerate. Descártalo y prueba el siguiente.
   - Entre los que pasen, quédate con el de mayor coincidencia que además sea latino.
   - **Plan B**, para cuando ninguno pasa y todos fallan con el mismo patrón (bien al principio y cada vez más desfasados): el video sale de un master con cortes distintos, así que ningún desfase único va a servir. Ejecuta `piecewise.py audio.wav cand.srt cand.pw.srt` sobre el `.srt` **original**, sin pasarlo antes por ffsubsync. El script asigna un desfase a cada línea y penaliza los saltos. Después pásale `check.py`. Revisa la trayectoria que imprime (el desfase cada 10 min): tiene que avanzar en una sola dirección y moverse pocos segundos en total. Si va y viene, está persiguiendo ruido: descarta ese candidato. Si el rango de desfase no alcanza, pásale los límites (`… -15 5`).
7. **Limpiar y guardar**: `clean.py cand.sync.srt "<carpeta>/<video>.srt"`, donde `<video>` es exactamente el nombre del archivo de video sin la extensión (para `SK.mkv`, `SK.srt`). Así VLC y otros reproductores lo cargan solos. Vuelve a ejecutar `check.py` sobre el archivo final. Antes de sobrescribir un `.srt` que ya exista, pregunta.
8. **Anotar en la memoria**: agrega el título a `<skill>/peliculas.txt` si no estaba (si el archivo no existe, créalo), haya quedado o no un subtítulo válido.
9. **Informar** en español: qué fuente se usó y por qué, el desfase original, la tabla de verificación final y cualquier subtítulo que ya hubiera y esté desfasado (`check.py` también sirve para medirlos).
