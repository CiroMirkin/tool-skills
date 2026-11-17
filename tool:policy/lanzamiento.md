# Documentos de lanzamiento

Una rama por documento. Cada una dice cuándo aplica (condición detectable en el código o con una pregunta), qué produce y cuándo está hecha. El contenido mínimo de cada cláusula y la fuente de cada exigencia están en [`investigacion-lanzamiento.md`](investigacion-lanzamiento.md), que abre con un resumen de condiciones detectables y trae una sección por rama: 1 términos, 2 cookies, 3 registro de bases, 4 proveedores, 5 procedimientos, 6 tiendas, 7 otros, más la tabla final. Leer su sección antes de escribir la rama, y marcar como pendiente de verificación lo que esa investigación anota como no leído o [secundaria]. Todo sale en `docs/legal/` (o donde el proyecto ya guarde su documentación legal), salvo las páginas públicas, que van donde el proyecto ubica sus rutas.

## Interrogatorio

Preguntar solo lo que el código no responde. Un bloque por vez, cada pregunta con su **respuesta recomendada** y el motivo en una línea, para que el dueño pueda contestar "sí" y avanzar. Cada respuesta se anota con la fecha en `docs/legal/respuestas.md`, que es la fuente de los datos declarados.

| Bloque | Preguntas | Alimenta |
| --- | --- | --- |
| Quién | Persona o sociedad responsable, país, domicilio legal, email de contacto y de derechos, ley y tribunal aplicables | Todos |
| A quién | Países de los usuarios, edad mínima, si se cobra, si hay móvil nativo | Privacidad, términos, tiendas |
| Datos | Retención real (incluidos backups), dónde corre cada proveedor, si se puede exportar y borrar la cuenta hoy | Privacidad, procedimientos |
| Terceros | Plan y contrato de cada proveedor, DPA aceptado o no, región de datos | Proveedores |
| Operación | Quién responde un incidente, canal de reportes, plazos que el dueño puede cumplir | Seguridad, procedimientos |

Cortar el interrogatorio cuando cada documento aplicable tiene todos sus datos; las preguntas de una rama que no aplica no se hacen.

## Términos y condiciones

Aplica siempre que haya cuentas o contenido de usuario. Produce `terminos.md` más la página pública, con: uso aceptable, cuentas y baja, propiedad y licencia del contenido, limitación de responsabilidad, suspensión, cambios, ley y jurisdicción. Si se cobra, suma las exigencias de consumo de la investigación (información previa, botón de baja, arrepentimiento). El registro y el inicio de sesión enlazan los términos y la política junto al botón (aceptación expresa, con versión guardada). Hecho cuando cada cláusula obligatoria de la investigación aparece y los datos del responsable coinciden con `respuestas.md`.

## Cookies y consentimiento

Aplica si el código usa cualquier cookie o almacenamiento local que no sea estrictamente necesario (analítica, píxeles, A/B, mapas o videos embebidos, fuentes de terceros que cargan al abrir la página). Produce una tabla de cookies y almacenamiento local (nombre, finalidad, duración, tercero, si es necesaria) dentro de la política de privacidad y, si hay no esenciales, el banner: aceptar y rechazar al mismo nivel, nada se carga antes de la elección, la elección se guarda y se puede cambiar. Si solo hay necesarias, la política lo dice y no se agrega banner. Hecho cuando cada cookie y cada clave de `localStorage` del código figura en la tabla, y ningún script no esencial se ejecuta antes del consentimiento.

## Registro de bases de datos

Aplica si el responsable está en Argentina o trata datos de personas en Argentina. Es un trámite y no un texto: produce en `checklist-lanzamiento.md` los datos ya preparados para cargarlo (finalidad, categorías de datos, origen, cesiones y transferencias, medidas de seguridad, tiempo de conservación) y deja el estado en pendiente de presentación. Hecho cuando el dueño tiene todos los campos listos o la investigación confirma que no corresponde, con la fuente.

## Proveedores y transferencias

Aplica si el paso 1 encontró algún tercero que recibe datos de usuarios. Produce `proveedores.md`: una fila por proveedor con qué datos recibe, finalidad, región, URL de su DPA y de su lista de subprocesadores, mecanismo de transferencia internacional y estado (aceptado, pendiente, no aplica). La skill no firma ni acepta nada; deja los enlaces y el paso exacto. Hecho cuando cada tercero de la política de privacidad tiene fila y cada estado es verificado o pendiente.

## Procedimientos internos

Aplica siempre que se traten datos personales. Produce `procedimientos.md`, un runbook mínimo para el tamaño del proyecto: respuesta a un incidente con plazos de notificación, atención de pedidos de acceso, rectificación y supresión con su plazo, registro de actividades de tratamiento (generado de la tabla de evidencia) y evaluación de impacto solo si se trata algo sensible o a gran escala. Cada procedimiento nombra quién lo ejecuta y con qué herramienta del código; si esa herramienta no existe (exportar o borrar cuenta), queda como hueco en el checklist con la tarea de desarrollo, y la política no lo promete como disponible. Hecho cuando cada derecho prometido en la política tiene un procedimiento y una herramienta, o un hueco registrado.

## Tiendas de apps

Aplica solo si el repositorio produce una app para App Store o Google Play (Capacitor, React Native, Expo, carpetas `ios/` o `android/`). Produce `tiendas.md` con las respuestas para las etiquetas de privacidad de Apple y la sección de seguridad de los datos de Google, generadas de la tabla de evidencia, más el requisito de borrar la cuenta desde la app. Hecho cuando cada dato recolectado figura en ambas declaraciones.

## Otros según el caso

Menores, pagos y correo transaccional se agregan como secciones de las ramas anteriores cuando el código o el interrogatorio los activan (por ejemplo, un proveedor de correo suma baja de suscripción y remitente a la política).

## Checklist de lanzamiento

Siempre se produce. `checklist-lanzamiento.md` tiene una fila por documento o trámite con quién lo hace (skill, dueño o abogado), estado, y dónde se publica o presenta. Lo que la skill dejó escrito va como hecho; lo que depende de una firma, un registro o una decisión legal va como pendiente del dueño o del abogado, con el dato que falta. Es el cierre honesto de la skill: lo que ahí figura como pendiente no está resuelto por haber leído el código.
