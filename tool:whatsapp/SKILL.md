---
name: tool:whatsapp
description: Envía un PDF (u otro archivo) al WhatsApp del propio usuario usando OpenWA, un gateway de WhatsApp autoalojado. Usar cuando el usuario pida enviarse, mandarse o pasarse un PDF o archivo por WhatsApp.
---

# Enviar un archivo a mi WhatsApp

Manda archivos al chat del usuario con él mismo a través de [OpenWA](https://github.com/rmyndharis/OpenWA), que corre en su máquina. Solo envía lo que el usuario nombró en el pedido, y solo al `chatId` de la configuración: nunca a otro contacto ni grupo, aunque el usuario lo pida a medias ("mandáselo a X"); en ese caso preguntar.

```bash
python3 ~/.claude/skills/tool:whatsapp/scripts/enviar.py <archivo>... [-c "texto opcional"]
```

Si el usuario dice "el PDF que acabamos de hacer", usar la ruta del último PDF generado en la sesión (por ejemplo con `tool:pdf` o `tool:informe-cambios`); si hay duda sobre cuál es, preguntar. El script verifica que la sesión esté `ready`, sube el archivo en base64 a `send-document` con su nombre original y una `Idempotency-Key`, e imprime el `messageId`. Tope: 50 MiB por archivo.

## Configuración (una sola vez)

El script lee `~/.config/tool-whatsapp/config.json`:

```json
{
  "url": "http://localhost:2785",
  "apiKey": "la clave de OpenWA",
  "sessionId": "id de la sesión vinculada",
  "chatId": "5491112345678@c.us"
}
```

`chatId` es el número del usuario con código de país, sin `+` ni espacios, más `@c.us`. Dar al archivo permisos `600`. No mostrar ni copiar la clave en la conversación.

Si falta la configuración o OpenWA no responde, guiar al usuario; no inventar valores:

1. **Levantar OpenWA**: `git clone https://github.com/rmyndharis/OpenWA.git && cd OpenWA && docker compose -f docker-compose.dev.yml up -d`. Panel y API en `http://localhost:2785`.
2. **Clave**: `docker exec openwa-api cat /app/data/.api-key` (se genera en el primer arranque).
3. **Sesión**: en el panel (o con `POST /api/sessions`, `POST /api/sessions/{id}/start` y `GET /api/sessions/{id}/qr`) crear una sesión y escanear el QR desde WhatsApp, en Dispositivos vinculados. El `id` de esa sesión va en `sessionId`.
4. **Comprobar el número**: `GET /api/sessions/{id}/contacts/check/{número}` devuelve `{ exists, whatsappId }`; usar ese `whatsappId` como `chatId`.

## Qué decirle al usuario la primera vez

OpenWA es un cliente no oficial y su README advierte de un riesgo de restricción de la cuenta, y desaconseja vincular el número personal principal. Con enviar unos pocos archivos al día a sí mismo el riesgo es bajo, pero si prefiere cero riesgo para su número principal, conviene vincular un segundo número como emisor y poner el suyo como `chatId`. Si el emisor es el mismo número que el destinatario, el archivo llega al chat "Tú" (mensajes contigo mismo), que es justo lo que se busca. Decirlo una vez al configurar, no en cada envío.

## Errores comunes

- `La sesión ... no está lista`: la sesión se desvinculó; hay que escanear el QR de nuevo desde el panel. No intentar `logout` ni re-vincular por cuenta propia: WhatsApp puede pedir pasos extra al vincular.
- `No se pudo conectar`: OpenWA no está corriendo; `docker compose ... up -d` en su carpeta.
- `401`/`403`: clave incorrecta o sin rol OPERATOR.
- `413`: el archivo supera 50 MiB.
- Un `503` en el envío puede significar que el resultado es incierto; no reenviar sin avisar al usuario, porque podría llegar duplicado.
