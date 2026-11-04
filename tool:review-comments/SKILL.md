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

   Si la propuesta es borrar, el bloque lleva solo el comentario actual y abajo dice *borrar*. En un hueco, el bloque lleva el código y, abajo, el comentario nuevo o la pregunta. El código entra en el bloque solo cuando también cambia (ej. un nombre mejor en vez de un eco). Aplicar los cambios recién cuando el usuario los apruebe.

## Categorías

- **Se queda**: cuenta algo invisible (ver la lista de abajo).
- **Eco** → borrar: repite el nombre de la función, variable, clase o método, o narra lo que la línea ya dice (`# incrementa el contador`). También es eco el ruido: código comentado (para eso está git), separadores decorativos, `// fin del if`, autor y fecha, historial de cambios. Si el eco existe porque el nombre es malo, proponer el nombre mejor en vez del comentario.
- **Mezcla** → reescribir: tiene algo invisible enterrado entre eco. Quedarse solo con lo invisible.
- **Mentira** → corregir o borrar: contradice al código actual (desfasado, TODO ya resuelto, parámetro que ya no existe). Es peor que no tener comentario.
- **Hueco** → agregar: salió del paso 2.
- **Confuso** → partir: cuenta algo invisible pero pega ideas con `;` (ver *Cómo se escribe*).

## Cómo se escribe

Una idea por oración, sin `;`. El punto y coma pega dos ideas sin decir qué relación tienen, y el lector tiene que adivinar si la segunda es causa, consecuencia o algo aparte:

- Si las ideas son independientes, cada una va en su oración, en su propia línea.
- Si una depende de la otra, el conector dice la relación: *porque*, *así que*, *para que*, *pero*.

Ideas independientes:

```python
# Antes
# Es el único que decide qué póster se muestra; db.reasignar y la fusión solo mueven filas de posters.
# Después
# Es el único que decide qué póster se muestra.
# db.reasignar y la fusión solo mueven filas de posters.
```

Ideas que dependen:

```python
# Antes
# Puede haber más de uno por bajadas a rutas viejas; sorted para que la elección no dependa del orden del set.
# Después
# Puede haber más de uno por bajadas a rutas viejas, así que se ordenan para que la elección no dependa del orden del set.
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
