#!/usr/bin/env python3
"""Envía archivos (PDF por defecto) al WhatsApp del usuario con OpenWA.

Uso: enviar.py <archivo>... [-c "texto"] [--config ruta]
Config (JSON): url, apiKey, sessionId, chatId. Por defecto ~/.config/tool-whatsapp/config.json
"""
import argparse, base64, json, mimetypes, os, sys, urllib.error, urllib.request, uuid

p = argparse.ArgumentParser()
p.add_argument("archivos", nargs="+")
p.add_argument("-c", "--caption", default="")
p.add_argument("--config", default=os.path.expanduser("~/.config/tool-whatsapp/config.json"))
a = p.parse_args()

try:
    cfg = json.load(open(a.config))
    url, key, sid, chat = (cfg[k] for k in ("url", "apiKey", "sessionId", "chatId"))
except (OSError, KeyError, ValueError) as e:
    sys.exit(f"Config inválida o ausente en {a.config}: {e!r}. Ver la sección Configuración de SKILL.md.")

url = url.rstrip("/")
MAX = 50 * 1024 * 1024  # tope de OpenWA por envío (MEDIA_DOWNLOAD_MAX_BYTES)


def api(method, path, body=None, headers=None):
    req = urllib.request.Request(
        f"{url}/api{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"X-API-Key": key, "Content-Type": "application/json", **(headers or {})},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"OpenWA respondió {e.code}: {e.read().decode(errors='replace')[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"No se pudo conectar con OpenWA en {url}: {e.reason}. ¿Está levantado?")


estado = api("GET", f"/sessions/{sid}").get("status")
if estado != "ready":
    sys.exit(f"La sesión de WhatsApp no está lista (estado: {estado}). Hay que volver a vincularla con el QR.")

for ruta in a.archivos:
    if not os.path.isfile(ruta):
        sys.exit(f"No existe: {ruta}")
    if os.path.getsize(ruta) > MAX:
        sys.exit(f"{ruta} pesa más de 50 MiB, el tope de OpenWA.")
    mime = mimetypes.guess_type(ruta)[0] or "application/octet-stream"
    r = api(
        "POST",
        f"/sessions/{sid}/messages/send-document",
        {
            "chatId": chat,
            "base64": base64.b64encode(open(ruta, "rb").read()).decode(),
            "mimetype": mime,
            "filename": os.path.basename(ruta),
            **({"caption": a.caption} if a.caption else {}),
        },
        # evita duplicados si se reintenta tras un corte de conexión
        {"Idempotency-Key": str(uuid.uuid4())},
    )
    print(f"Enviado: {os.path.basename(ruta)} ({r.get('messageId')})")
