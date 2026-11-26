---
name: code:review-comments
description: Borra los comentarios del código dentro del alcance y escribe de nuevo solo los que el código necesita, y señala lo que pide aprobación. Usar cuando el usuario pida revisar, limpiar o auditar comentarios, y al terminar de editar código que agregó o tocó comentarios.
---

# Revisar comentarios

El código ya dice *qué* hace. Un comentario se gana su lugar contando lo **invisible**: lo que no está en el código y que nadie puede deducir leyéndolo. Todo lo demás es **eco**, y el eco se borra: un comentario innecesario no es inofensivo, es ruido que hay que mantener y que tapa a los que importan.

## Alcance

Lo que el usuario nombre (archivo, carpeta, commit, rama). Si no nombra nada, el diff sin commitear; si está limpio, el último commit.

En un archivo o carpeta entran todos sus comentarios. En un diff (sin commitear, commit o rama) entran solo los que el diff agregó o tocó y los que acompañan líneas modificadas.

Al terminar de editar código, el alcance es el del propio diff y se corre sin que el usuario lo pida.

## Pasos

1. **Borrar** todos los comentarios y docstrings del alcance, sin clasificarlos: los borrados se descartan. Se quedan los que cambian el comportamiento o son obligatorios: shebang, encoding, directivas (`eslint-disable`, `@ts-expect-error`, `# noqa`, `# type: ignore`, `//go:build`), cabeceras de licencia y docstrings que el programa lee (ayuda de CLI, docs de API). Si un docstring era todo el cuerpo, queda `pass`. Hecho cuando no queda ningún otro en el alcance y borrarlos no cambió el comportamiento.
2. **Leer el código nuevo y el modificado** del alcance, ya sin comentarios, y marcar cada lugar con un motivo invisible (número mágico, `sleep`, orden de líneas que importa, `catch` que traga errores, workaround, valor de config externo, regex cuyo nombre o validación cercana no dicen qué valida). El motivo se busca en el código, en los mensajes de commit (`git log -L`, `git blame`), en la issue o en el ADR. El texto de un comentario viejo, visto en el diff o en el historial, no cuenta como fuente. Hecho cuando cada lugar tiene su motivo encontrado o quedó marcado como *pregunta para el usuario*: el motivo se cita, no se inventa.
3. **Escribir** directo, sin pedir aprobación, un comentario en cada lugar con motivo encontrado, según *Qué se escribe*, *Cómo se escribe* y *Lo invisible*. Hecho cuando ninguno queda sin escribir.
4. **Reportar** cuántos comentarios se borraron y cuántos se escribieron, y en qué archivos. Aparte va lo que espera aprobación: preguntas, secciones y todo cambio de código (ej. un nombre mejor en vez de un comentario). Cada uno lleva un id correlativo (C1, C2…) para que el usuario los apruebe por id, y `archivo:línea`. Debajo va un bloque de código con el código y, abajo, la pregunta o el cambio propuesto. En una sección, el bloque lleva el lugar donde empieza y, abajo, el archivo propuesto. Se aplica recién cuando el usuario lo apruebe.

## Qué se escribe

Solo lo invisible (ver la lista de abajo), nunca eco. **Eco** es repetir el nombre de la función, variable, clase o método, o narrar lo que la línea ya dice (`# incrementa el contador`). También es eco el ruido: código comentado (para eso está git), separadores sin nombre, `// fin del if`, autor y fecha, historial de cambios. Si dan ganas de escribir un eco porque el nombre es malo, proponer el nombre mejor en vez del comentario.

Si una parte del archivo hace algo distinto del resto y se la podría nombrar como una **sección**, no se le pone un separador: se recomienda refactorizarla a su propio archivo.

De un dato invisible se escribe solo eso, sin lo que se puede leer en el código:

```python
# Con eco
"""IMDb ID que aparece en `texto` (ej. un link de imdb.com), o None."""
# Se escribe
"""IMDb ID que aparece en `texto` (ej. un link de imdb.com)"""

# Con eco
"""Baja el poster de OMDb a `destino` (de `destino_poster`); devuelve si se pudo. Corre fuera del hilo de la UI."""
# Se escribe
"""Corre fuera del hilo de la UI."""

# Con eco
"""Escribe los bytes `png` como captura en `posicion_ms` y devuelve la ruta. Crea `capturas/`
si falta. Escribe a un temporal oculto y lo pasa al nombre final recién completo, así `listar`
nunca ve un PNG a medias. Nunca pisa: si otra captura ocupa el nombre entre medio, prueba el
siguiente. Lanza OSError."""
# Se escribe
"""Pasa por un temporal oculto para que `listar` nunca vea un PNG a medias y lanza OSError."""
```

También es eco lo que ya sabe cualquiera que use el framework, pero en la misma frase puede haber un dato invisible que se escribe:

```ts
// Con eco
// Next llama a register al arrancar el servidor y no durante next build
export const register = async () => {
// Se escribe
// register no corre durante next build
export const register = async () => {
```

Hay eco que parece aportar contexto. Acá el nombre, la condición y el mensaje del error ya lo dicen todo:

```ts
// Con eco, no se escribe nada
/** Corta el arranque en producción si falta la cabecera */
export const exigirCabeceraIp = (env: Partial<NodeJS.ProcessEnv> = process.env) => {
    if (env.NODE_ENV === "production" && !cabeceraIpDelCliente(env)) {
        throw new Error("Falta AUTH_IP_HEADER: sin ella el límite de intentos de login por IP se puede evadir.")
    }
}
```

En una regex el comentario o el nombre dicen qué valida, salvo que ya lo diga la validación cercana:

```ts
// El mensaje ya lo aclara y no hace falta nada
.regex(/^\d{7,8}$/, "El DNI debe tener 7 u 8 dígitos")

// Sin mensaje va un comentario
// DNI de 7 u 8 dígitos
.regex(/^\d{7,8}$/)

// O un nombre
const DNI = regex(/^\d{7,8}$/) // el nombre ya dice qué valida y no necesita comentario
```

## Cómo se escribe

Un comentario se lee **de corrido**, con la relación entre las ideas dicha en palabras y el sujeto a la vista. Los signos pegan ideas y dejan al lector adivinando qué cosa va con cuál, o si la segunda idea es causa, consecuencia o algo aparte. Por eso `:`, `;` y `,` se reemplazan por la palabra que dice la relación: *es*, *y*, *entonces*, *porque*, *para que*, *pero*, *primero… luego*.

```python
# Antes
# Importan QtMultimedia y requests, que son gran parte de la espera: van después de la ventana
# Después
# Gran parte de la espera es debido a importar QtMultimedia y requests por eso se importan después de abrir la ventana

# Antes
"""Abre la ventana con el spinner y, ya pintada, carga el resto."""
# Después
"""Primero abre la ventana con el spinner y luego carga el resto."""

# Antes
# Arrancó bien: si venía de actualizar, ya no hace falta la versión anterior
# Después
# Arrancó bien y si arrancó luego de actualizar entonces ya no es necesaria la versión anterior

# Antes
# Nombre que pone `ruta_libre`: `HH-MM-SS.ext` o `HH-MM-SS(n).ext`
# Después
# Nombre que pone `ruta_libre` es `HH-MM-SS.ext` o `HH-MM-SS(n).ext`

# Antes
"""Ruta para una captura en `posicion_ms`: `capturas/HH-MM-SS.png`, o `HH-MM-SS(n).png`
con el primer n ≥ 2 libre. Nunca devuelve una que ya exista."""
# Después
"""La ruta para una captura en `posicion_ms` es `capturas/HH-MM-SS.png` o `HH-MM-SS(n).png` con el primer n ≥ 2 libre y nunca devuelve una que ya exista."""

# Antes
# Sistemas de archivos sin hard links (FAT, exFAT): rename sí pisa, así que se mira
# antes. Solo queda la ventana entre mirar y renombrar.
# Después
# En sistemas de archivos sin hard links (FAT, exFAT) rename sí pisa entonces se mira antes para que solo quede la ventana entre mirar y renombrar.

# Antes
""""Alien 1979" o "Alien (1979)" -> ("Alien", 1979); sin año -> (texto, None)."""
# Después
""""Alien 1979" o "Alien (1979)" se retorna ("Alien", 1979) y sin año se retorna (texto, None)."""

# Antes
# Puede haber más de uno por bajadas a rutas viejas; sorted para que la elección no dependa del orden del set.
# Después
# Puede haber más de uno por bajadas a rutas viejas entonces se ordenan para que la elección no dependa del orden del set.

# Antes
/**
 * Borra un lote que nunca tuvo movimientos. Con movimientos se rechaza porque el borrado en cascada
 * se llevaría sus cortes y el pedido quedaría sin cortes, sin poder finalizarse.
 */
# Después
/**
 * Si el lote tiene movimientos se rechaza porque el borrado en cascada se llevaría sus cortes entonces el pedido quedaría sin cortes y sin poder finalizarse.
 */
```

Tampoco se usa `→`. La relación se dice con *se convierte en*, *da* o *retorna*. Y si el comentario no lleva una lista de ejemplos, no termina en `:`.

```python
# Antes
# "40090" → "040090"
# Después
# "40090" se convierte en "040090"
```

El sujeto se nombra con un verbo, no con una preposición suelta.

```ts
// Antes
// Corte desde una mesa por la API v1. El DNI solo se usa si el corte comienza el pedido
// Después
// Corte que llega desde una mesa por la API v1. El DNI solo se usa si el corte comienza el pedido
```

Un signo se queda solo cuando es lo que mejor se lee:

- **`:`** antes de una lista de valores de ejemplo.
- **`,`** entre los elementos de una lista de tres o más. Dos casos o dos hechos se unen con *o* / *y*, sin coma, y antes de un conector (*para que*, *entonces*) tampoco lleva.
- **`.`** entre puntos realmente diferentes, que en una sola oración serían confusos. Cada uno va en su propia línea.

```python
# `:` con una lista de valores de ejemplo
# Antes
// Duración redondeada al minuto: "2 h 5 min", "2 h", "45 min"; vacío si no se conoce
# Después
// Duración redondeada al minuto: "2 h 5 min", "2 h", "45 min".

# `,` en una lista de tres o más
# Reintenta con timeout, error 500 o conexión cortada

# Dos casos con "o" y dos hechos con "y", sin coma
# Antes
# Disco lleno a mitad de camino, o ya movido: no dejar el temporal
# falla si existe; el temporal lo borra quien llama
# Después
# Disco lleno a mitad de camino o ya movido
# Falla si ya existe y el temporal lo borra quien llama

# `,` de más antes de un conector
# Antes
# antes que el puente, para que QML no lo lea ya destruido al cerrar
# Después
# antes que el puente para que QML no lo lea ya destruido al cerrar

# `.` entre puntos diferentes
# Antes
# Es el único que decide qué póster se muestra; db.reasignar y la fusión solo mueven filas de posters.
# Después
# Es el único que decide qué póster se muestra.
# db.reasignar y la fusión solo mueven filas de posters.
```

## Lo invisible

No hace falta documentar todo esto siempre; depende del caso. Es la lista contra la que se mide cada comentario antes de escribirlo:

- **Por qué** esta solución, y **por qué no** la otra que parecía más obvia o natural.
- **Para qué** existe el código: dónde encaja en la foto global, qué dependencias invisibles tiene, en qué situación se podría borrar.
- **Peligros**: qué cambios no hacer y por qué; efectos colaterales de cambios aparentemente inocuos (condiciones de carrera o interbloqueos al reordenar líneas).
- **Lo descartado**: lo que se probó y no funcionó, lo que se estudió y se descartó enseguida, para no volver a gastar tiempo ahí.
- **Factores externos**: config global, variables de entorno o sistemas de terceros de los que depende.
- **Depuración**: qué log o herramienta mirar si falla, sobre todo en tests de integración.
- **Troubleshooting de tests**: qué impide correrlos en paralelo, qué configuración previa necesitan, los fallos comunes cuando caen muchos juntos.
- **Deuda técnica**: hasta dónde aguanta la solución (librería sin soporte, infraestructura que llega a N usuarios).
- **Terceros**: cómo se comporta una librería o framework en un uso particular o mal documentado; sorpresas que dio, para llevárselas una sola vez.
- **API pública** de propósito general: su contrato. Describir parámetros y retorno solo cuando agregan contexto que el nombre y el tipo no dan (en lenguajes interpretados, el docstring además alimenta al IDE).
- **Arqueología**: en código heredado sin tests y sin nadie a quien preguntar, lo que se descifró depurando a prueba y error. Se escribe, y debe decir que es comportamiento deducido y por qué se comentó en vez de refactorizar.
