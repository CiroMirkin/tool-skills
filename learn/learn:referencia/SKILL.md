---
name: learn:referencia
description: Agrega un repo o un sitio a la base de referencias de desarrollo que consultan learn:roadmap, learn:learn y learn:doc-estudio. Usar con /learn:referencia <url> o /learn:referencia --docs <ruta>, o cuando el usuario pida sumar, guardar o quitar una referencia.
---

# Referencia

La base es [`referencias.md`](../learn:referencias-base/referencias.md): una entrada por repo o sitio, agrupadas por sección. Esta skill suma entradas; se escriben en el idioma del archivo (español) y en su formato.

## Pasos

1. **Tomar las URLs.** Salen de los argumentos. Sin URL, preguntar cuál. Hecho cuando hay una lista de URLs.

2. **Leer cada una** con `fetch_content` de TinyFish (`WebFetch` si no está). Para un repo de GitHub, leer su README; para un sitio, la portada y la página de su currículo o índice. Anotar qué es, qué cubre (los temas concretos, entre paréntesis) y para qué sirve como referencia. Hecho cuando la descripción sale de lo que se leyó.

3. **Ubicar.** Buscar la URL en `referencias.md`: si ya está, informarlo y saltar al paso 5 sin escribir. Si no, elegir la sección que mejor la contiene; si ninguna calza, crear una nueva con título en sentence case. Un repo y un sitio del mismo tema van en la misma sección salvo que sea un sitio de aprendizaje: esos van en "Sitios de aprendizaje".

4. **Escribir** una entrada, un párrafo suelto como las vecinas:
   - repo: `[owner/repo](url): descripción (temas).`
   - sitio: `[Nombre](url): descripción (temas).` Con rutas o cursos propios, se enlazan dentro de la misma entrada.

   La URL apunta a la raíz del repo o a la página índice del sitio, no a una lección: la sección exacta se enlaza cada vez que una skill la consulta. Una sola oración, sin "·" ni mayúsculas forzadas. Hecho cuando la entrada está en su sección.

5. **Verificar** que la URL responde (`curl -sIL -o /dev/null -w '%{http_code}' <url>`). Si no da 200, avisarlo y preguntar si queda igual. Informar al usuario la sección elegida y la línea escrita, sin commitear.

## Documentos personales

Con `--docs <ruta>` (o si el usuario pide sumar su carpeta de libros o apuntes) no se escribe en `referencias.md`: la ruta va en `documentos-locales.md`, en la carpeta de `learn:referencias-base`, una por línea.

1. Verificar que la ruta existe y es un directorio (`test -d`). Si no, avisar y preguntar de nuevo.
2. Si `documentos-locales.md` no existe, crearlo; si la ruta ya está, informarlo y no repetirla. Agregar la ruta tal cual la dio el usuario.
3. Confirmar que `documentos-locales.md` está en el `.gitignore` del repo; si falta, agregarlo. Esa ruta es privada y no se commitea.
4. Informar la ruta guardada. No leer ni listar su contenido: las skills que consultan las referencias eligen y leen lo que necesitan (ver la sección "Documentos personales" de `referencias.md`).

## Quitar

Si el usuario pide quitar una referencia, borrar su entrada y informar cuál. Para quitar una carpeta de documentos personales, borrar su línea de `documentos-locales.md`.
