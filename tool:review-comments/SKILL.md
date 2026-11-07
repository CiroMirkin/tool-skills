---
name: tool:review-comments
description: Revisa los comentarios del código y señala cuáles sobran, cuáles mienten y dónde falta uno. Usar cuando el usuario pida revisar, limpiar o auditar comentarios.
---

# Revisar comentarios

El código ya dice *qué* hace. Un comentario se gana su lugar contando lo **invisible**: lo que no está en el código y que nadie puede deducir leyéndolo. Todo lo demás es **eco**, y el eco se borra: un comentario innecesario no es inofensivo, es ruido que hay que mantener y que tapa a los que importan.

## Alcance

Lo que el usuario nombre (archivo, carpeta, commit, rama). Si no nombra nada, el diff sin commitear; si está limpio, el último commit.

## Pasos

1. **Leer cada comentario del alcance junto al código que acompaña** (incluye docstrings y cabeceras). Hecho cuando cada uno quedó clasificado en una de las categorías de abajo.
2. **Buscar los huecos**: código cuyo motivo es invisible y no tiene comentario (número mágico, `sleep`, orden de líneas que importa, `catch` que traga errores, workaround, valor de config externo). Para cada uno, buscar el motivo en `git log -L`/`git blame`, el commit, la issue o el ADR que lo introdujo. Hecho cuando cada hueco tiene su motivo encontrado o quedó marcado como *pregunta para el usuario*: el motivo se cita, no se inventa.
3. **Reportar**, agrupado por categoría. Cada hallazgo lleva un id correlativo en todo el reporte (C1, C2…, sin reiniciar por categoría) para que el usuario los apruebe por id, y `archivo:línea`. Debajo va un bloque de código con el comentario actual y, en la línea siguiente, el propuesto:

   ```tsx
   // 7rem = header h-16 + py-6 del layout; solo la tabla scrollea
   // 7rem = header h-16 + py-6 del layout (Alto fijo para que solo scrollee la tabla)
   ```

   Si la propuesta es borrar, el bloque lleva solo el comentario actual y abajo dice *borrar*. En un hueco, el bloque lleva el código y, abajo, el comentario nuevo o la pregunta. En una sección, el bloque lleva el separador y, abajo, el archivo propuesto. El código entra en el bloque solo cuando también cambia (ej. un nombre mejor en vez de un eco). Aplicar los cambios recién cuando el usuario los apruebe.

## Categorías

- **Se queda**: cuenta algo invisible (ver la lista de abajo).
- **Eco** → borrar: repite el nombre de la función, variable, clase o método, o narra lo que la línea ya dice (`# incrementa el contador`). También es eco el ruido: código comentado (para eso está git), separadores sin nombre, `// fin del if`, autor y fecha, historial de cambios. Si el eco existe porque el nombre es malo, proponer el nombre mejor en vez del comentario.
- **Mezcla** → reescribir: tiene algo invisible enterrado entre eco. Quedarse solo con lo invisible.
- **Mentira** → corregir o borrar: contradice al código actual (desfasado, TODO ya resuelto, parámetro que ya no existe). Es peor que no tener comentario.
- **Hueco** → agregar: salió del paso 2.
- **Confuso** → reescribir: cuenta algo invisible pero no se lee de corrido (ver *Cómo se escribe*).
- **Sección** → proponer un archivo: un comentario que delimita una sección con nombre muestra que el archivo hace varias cosas. Recomendar refactorizar cada sección a su propio archivo.

Ejemplos de **Mezcla**, donde lo que se va se puede leer en el código:

```python
# Antes
"""IMDb ID que aparece en `texto` (ej. un link de imdb.com), o None."""
# Después
"""IMDb ID que aparece en `texto` (ej. un link de imdb.com)"""

# Antes
"""Baja el poster de OMDb a `destino` (de `destino_poster`); devuelve si se pudo. Corre fuera del hilo de la UI."""
# Después
"""Corre fuera del hilo de la UI."""

# Antes
"""Escribe los bytes `png` como captura en `posicion_ms` y devuelve la ruta. Crea `capturas/`
si falta. Escribe a un temporal oculto y lo pasa al nombre final recién completo, así `listar`
nunca ve un PNG a medias. Nunca pisa: si otra captura ocupa el nombre entre medio, prueba el
siguiente. Lanza OSError."""
# Después
"""Pasa por un temporal oculto para que `listar` nunca vea un PNG a medias y lanza OSError."""
```

Ejemplos de **Sección**:

```
# --- escaneo ---
// ==================== TOUCH ====================
// ==================== WIFI ====================
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

No hace falta documentar todo esto siempre; depende del caso. Es la lista contra la que se mide cada comentario y cada hueco:

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
- **Arqueología**: en código heredado sin tests y sin nadie a quien preguntar, lo que se descifró depurando a prueba y error. Se queda, y debe decir que es comportamiento deducido y por qué se comentó en vez de refactorizar.
