---
name: tools:policy
description: Prepara los documentos legales para lanzar un repositorio a producción a partir de su código real (política de privacidad, política de seguridad, SECURITY.md, términos y condiciones, cookies, proveedores, procedimientos, tiendas y checklist de trámites). Usar cuando el usuario pida políticas, términos, un SECURITY.md o lanzar legalmente una app, o quiera revisar que lo que ya tiene diga lo que el código hace.
---

# Policy

Una política es una **promesa pública**: todo lo que afirma tiene que poder verificarse en el código, y todo dato que el código toca tiene que estar en ella. Un borrador escrito desde el README miente en los dos sentidos (en el caso que originó esta skill, el README decía NextAuth y el código usaba better-auth, decía que el archivo se purgaba solo y era un tope de capacidad, y callaba que la sesión guarda IP y user-agent, que Sentry recibe errores y que los tokens de GitHub se persisten). Por eso se lee el código primero y se escribe después.

Qué debe contener cada documento y cómo lo resuelven plataformas reales: leer [`investigacion.md`](investigacion.md) (normas, SECURITY.md, divulgación responsable) antes del paso 3 y [`ejemplos.md`](ejemplos.md) (Mercado Libre, Didi, Uber, PedidosYa, Lemon: esqueletos y citas) antes del paso 4. Los documentos de lanzamiento (términos, cookies, registro de bases, proveedores, procedimientos, tiendas, checklist) y el interrogatorio están en [`lanzamiento.md`](lanzamiento.md), que se lee al llegar al paso 2. Cada documento aplicable se escribe en su rama; los que no aplican se nombran en el checklist como "no aplica" con el motivo.

## Pasos

1. **Levantar los hechos del código** en una tabla de evidencia, una fila por hecho con su archivo y línea. Es el gemba: leer, no suponer. Recorrer en este orden: autenticación (librería, proveedores OAuth, qué se guarda de cada uno, hash y política de contraseñas), esquema de datos (cada columna que sea dato personal, IP y user-agent incluidos), almacenamiento en el navegador (cookies, `localStorage`, modo sin cuenta), terceros (SDKs, analítica, monitoreo de errores, hosting, base de datos, correo, pagos, listados en `package.json` y `.env.example`), autorización (guards o middleware que aíslan datos por cuenta), límites y retención (topes, jobs que borran, lo que nunca se borra), rate limiting, headers, validación de entrada, logs. Hecho cuando cada categoría tiene filas o la línea "revisado, no existe" con el archivo donde se buscó, y no queda ninguna dependencia de `package.json` que toque datos de usuarios sin clasificar.

2. **Interrogar al dueño** sobre lo que el código no prueba, con el método de `lanzamiento.md` (un bloque por vez, respuesta recomendada en cada pregunta). Cada hecho queda *verificado* (fila de la tabla) o *declarado por el dueño* (anotado con fecha en `respuestas.md`); lo que siga sin respuesta se escribe como `[pendiente: ...]` visible en el texto. Hecho cuando ninguna afirmación de los documentos queda sin una de las dos etiquetas y cada rama aplicable tiene todos sus datos.

3. **Escribir la política de privacidad** con el esqueleto de `ejemplos.md` ajustado a la jurisdicción del dueño: qué datos, de dónde salen, para qué se usan, con quién se comparten (cada tercero del paso 1 con su nombre y su finalidad), cuánto se conservan, qué derechos tiene la persona y cómo ejercerlos, cookies y almacenamiento local, menores, cambios de la política y contacto. Una tabla de datos para la lista de categorías, prosa para el resto. Hecho cuando cada fila de la tabla de evidencia que toca datos personales aparece en el texto, y cada tercero, nombrado.

4. **Escribir la política de seguridad** en dos piezas con roles distintos. La página para usuarios describe los controles que existen hoy, con el nombre real del mecanismo ("`requireBoardAccess` valida que el tablero pertenezca a la sesión"), y cierra con una sección de limitaciones honesta sobre lo que no hay. El `SECURITY.md` de la raíz solo dice cómo reportar una vulnerabilidad: canal privado, qué incluir, alcance, plazos de respuesta y divulgación, y enlaza a la página. Hecho cuando cada control nombrado tiene su fila de evidencia y cada hueco encontrado en el paso 1 (sin rate limiting, sin headers, sin scrubbing en el monitoreo) figura en limitaciones.

5. **Escribir los documentos de lanzamiento aplicables** siguiendo cada rama de `lanzamiento.md`, incluido `checklist-lanzamiento.md`, que se escribe siempre. Hecho cuando cada rama tiene su archivo o su "no aplica" con motivo, y cada trámite del dueño o del abogado figura como pendiente con su dato faltante.

6. **Ubicar los archivos como el proyecto ya ubica sus páginas.** Copiar la estructura de una página existente simple (mismo layout, mismas clases, misma convención de rutas) y dejar los enlaces desde footer, registro e inicio de sesión. Si no se pueden tocar sin poder ejecutar la app, decir qué archivo falta editar. Hecho cuando las rutas `/privacy` y `/security` y el `SECURITY.md` existen en el repo, o el usuario sabe exactamente qué falta.

7. **Releer contra el código, al revés.** Tomar cada afirmación de las dos políticas y buscar su fila de evidencia; después tomar cada fila y buscar dónde se la menciona. Hecho cuando no sobra ni falta ninguna, y los `[pendiente]` están listados.

8. **Compartir** las rutas, los hallazgos que contradecían al README, los `[pendiente]` y el checklist, con esta aclaración: son borradores fieles al código, y el cumplimiento legal lo decide quien los revisa (abogado o responsable de datos).

## Voz

El dueño habla a quien usa la app: frases cortas, "usamos", "guardamos", "no guardamos", con los números del código (10 intentos por minuto, 30 días de sesión). Un control se afirma una vez, en una sola sección; los demás lugares enlazan. Lo que el código no hace se dice como límite, nunca se omite ni se adorna.
