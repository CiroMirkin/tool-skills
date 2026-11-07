---
name: tool:doc-estudio
description: Escribe un .md que enseña un tema desde lo básico hasta la profundidad, como una lección del roadmap de Arduino, con código compilado y probado, diagramas si ayudan, ejercicio, quiz y fuentes. Usar cuando el usuario pida un doc de estudio, una lección o aprender un tema a fondo.
---

# Doc de estudio

El resultado es una **lección**: un solo `.md` con el que alguien que no conoce el tema llega a entenderlo a fondo sin abrir otro documento. Se escribe en el idioma y el registro del usuario. Cada paso de la lección se apoya en los anteriores, y cada dato concreto lleva la fuente que lo respalda.

## Pasos

1. **Leer el pedido.** Sacar de él el tema, el lector y lo que ya sabe, las fuentes que pasa el usuario, el proyecto de ejemplo si nombra uno y el destino. Sin destino pedido, va donde el proyecto guarda sus lecciones; si no hay ninguna, a `doc-estudio-<tema>.md` en el directorio actual.

   Si el destino ya tiene lecciones, como `roadmap-arduino-site`, leer su documentación (`README.md`, `CLAUDE.md`, `CONTEXT.md`) y dos lecciones del mismo nivel. Su formato, sus reglas y sus herramientas mandan sobre las de esta skill; las exigencias de los pasos 3, 4 y 8 se mantienen.

   Si el tema no entra en una lección, proponer el recorte o la lista de lecciones antes de seguir. Crear la **carpeta de trabajo** `<tema>-trabajo/` junto a la lección, con `codigo/` adentro; si el destino está en un repo, ponerla donde git la ignore. Todo lo intermedio vive ahí, para que sobreviva a una pausa. Hecho cuando están anotados tema, lector, destino y formato, y la carpeta existe.

2. **Elegir el caso**: el sistema concreto del que salen todos los ejemplos.
   - Si el usuario nombra un proyecto, o el tema aparece en el proyecto actual, usar ese, salvo que sus documentos pidan otro ejemplo o prohíban citarlo.
   - Si no, inventar el sistema más chico donde el tema importe, y anotar sus nombres, pines y números para repetirlos iguales en toda la lección.

   Hecho cuando el caso explica por qué alguien necesitaría este tema, con una situación que se rompe sin él.

3. **Investigar.** Reunir, en este orden:
   - todas las fuentes del usuario y el `RESOURCES.md` del proyecto si existe;
   - las skills del tema, en `.claude/skills` del proyecto o las globales (por ejemplo `cpp-reviewer` para firmware), que aportan criterio pero no se citan como fuente;
   - fuentes propias, buscadas siempre aunque las del usuario parezcan alcanzar: documentación oficial, specs, hojas de datos, el repo del proyecto. Un artículo secundario entra solo si explica algo que la fuente primaria no explica.

   Llevar cada dato concreto (un límite, un valor por defecto, un comportamiento) hasta su **dueño**: la fuente que lo define, en la versión que usa la lección, enlazada a la sección exacta. Armar con esto la **escalera**: los conceptos ordenados por dependencia, desde lo que entiende alguien que recién llega hasta los límites, lo que hay debajo, los modos de falla y las alternativas.

   Hecho cuando cada peldaño tiene su dueño, cada fuente del usuario está usada o anotada como "no aportó" con el motivo, y al menos una fuente propia sostiene algo de la lección.

4. **Escribir el código antes que la prosa.** Cada ejemplo vive como archivo real en `codigo/` y se queda ahí al terminar. Un bloque llega a dos estados:
   - **Verificado**: compila o pasa el analizador con la herramienta real, para la placa o versión que la lección nombra, sin errores ni advertencias propias.
   - **Validado**: se ejecutó y su salida coincide con lo que la lección dice que pasa.

   Aplicar estas reglas a cada bloque:
   - Un fragmento se copia textual de un programa completo que está verificado.
   - Un ejemplo de lo que está mal se comprueba igual: tiene que dar el error o el síntoma que la lección describe.
   - Si hace falta hardware, probar la lógica pura en la máquina (por ejemplo con `g++`) y dejar el resto como verificado, sin validar. Cargar una placa conectada solo con el permiso del usuario.
   - Si falta la herramienta, pedir permiso para instalarla. Un bloque que no llega a verificado se reescribe o se saca.
   - Pasar el código por las skills de revisión del tema, si las hay.

   Hecho cuando cada bloque tiene su estado, su comando y la versión de la herramienta anotados, y las salidas quedaron guardadas en la carpeta de trabajo.

5. **Diseñar los diagramas.** Un diagrama entra donde el lector tendría que armarse el dibujo en la cabeza: un recorrido de datos, una secuencia entre partes, estados, capas. Si una tabla o un párrafo ya lo muestra igual de bien, queda uno solo de los dos. Elegir pocas familias de diagrama que se repitan, con los datos de ejemplo del caso y los mismos nombres que el texto.

   Invocar la skill `diagram-design` para cada uno, comprobar el HTML con su `self_check.py` y exportarlo con `export_svg.py --system-fonts`. El SVG va en la carpeta de imágenes del proyecto o en `diagramas/` junto a la lección, con el HTML fuente al lado. Se inserta con `![qué muestra el diagrama](ruta.svg)`, justo después del párrafo que lo introduce.

   Convertir cada SVG a imagen y mirarla:

   ```bash
   uv run --with pymupdf python -c "import pymupdf; pymupdf.open('d.svg')[0].get_pixmap(dpi=100).save('d.png')"
   ```

   Hecho cuando cada diagrama pasó el chequeo y en su imagen cada rótulo queda dentro de su forma y cada flecha llega a destino.

6. **Redactar** en `<tema>-trabajo/leccion.fuente.md`, con el formato de abajo, recorriendo la escalera en orden. Escribir con la claridad de Martin Kleppmann, en estilo clásico: le mostrás al lector algo que podés ver y la transición de cada sección sale de la anterior. Un programa completo se inserta con una línea `@@carpeta/archivo@@` dentro de su bloque de código, relativa a `codigo/`. Armar la lección con:

   ```bash
   python3 ~/.claude/skills/tool:doc-estudio/scripts/leccion.py armar leccion.fuente.md ../<tema>.md --codigo codigo
   ```

   Después, hacer el **glosario de control** en la carpeta de trabajo: cada término técnico de la lección, en orden de aparición, con la línea donde se define, contando títulos, diagramas, código y quiz. El lector tiene que encontrar la definición antes del primer uso. Una palabra usada con dos sentidos se aclara o se cambia, y lo que se define en una sección que se puede saltear entra en la condición para saltearla.

   Hecho cuando cada peldaño de la escalera está en la lección, cada dato concreto tiene su enlace y cada término del glosario tiene su línea de definición.

7. **Editar** `leccion.fuente.md`. Seguir [`edicion.md`](edicion.md) y después invocar `humanizer:humanizer` sobre la prosa, dejando intactos el código, los comandos y los enlaces. Luego pedir una segunda pasada con ese mismo archivo: con `codex` o `gemini` si están instalados, y si no con un subagente que reciba solo la lección, `edicion.md` y quién es el lector. Revisar cada cambio contra el original antes de aceptarlo. Hecho cuando las dos pasadas terminaron, ningún dato cambió de sentido y la lección está armada de nuevo.

8. **Comprobar el archivo final.** Las ediciones pueden tocar lo ya revisado, así que todo se comprueba sobre el `.md` terminado:

   ```bash
   python3 ~/.claude/skills/tool:doc-estudio/scripts/leccion.py comprobar ../<tema>.md --codigo codigo
   ```

   El script revisa que cada bloque de código esté en un archivo de `codigo/`, las imágenes, los enlaces y sus anclas, las rayas largas, los marcadores y el largo de las opciones del quiz. Después:
   - Si cambió un archivo de `codigo/` después de verificarlo, compilarlo y ejecutarlo de nuevo.
   - Corregir o quitar los enlaces rotos. Si un sitio rechaza a `curl`, confirmar la página de otra forma.
   - Resolver el quiz leyendo solo la lección: cada respuesta tiene que salir del texto.
   - Correr las herramientas de verificación del destino, si tiene.

   Hecho cuando el script termina sin problemas y lo demás pasa, o lo que quedó sin pasar está anotado con el motivo.

9. **Entregar.** Informar el archivo y sus diagramas, el caso elegido, qué bloques quedaron verificados y cuáles validados, las fuentes del usuario que no aportaron, y qué herramienta hizo la segunda pasada.

## Formato

```markdown
# <Tema>

<Párrafo con la idea central: qué es, en palabras de quien recién llega.>

## Por qué te importa
<La situación del caso que se rompe sin este tema, con sus síntomas.>

## Antes de empezar
<Lo que hace falta saber para seguir. Avisar que se puede saltear si ya se conoce.>

## La idea
<La intuición con datos de juguete y un diagrama. La esencia, sin todos los detalles.>

## Paso a paso
### 1. <Concepto>
<Un concepto por paso, con un fragmento chico, de lo básico a lo específico.>

## Ejemplos
### Ejemplo 1. <Mínimo>
<Qué hace, el programa completo y qué observar al correrlo. Siguen uno típico y uno aplicado al caso.>

## En profundidad
<Lo que hay debajo, los límites con sus números, los modos de falla, y cuándo conviene otra alternativa.>

## Errores comunes
### <Error>
<Síntoma, código `// Mal`, código `// Bien` y por qué.>

## Ejercicio
<Enunciado sobre el caso, resoluble con lo visto.>
<details><summary>Pista</summary>...</details>
<details><summary>Ver solución</summary>...</details>

## Quiz
**1. <Pregunta>**
- <Opción>
<details><summary>Ver respuesta</summary>La correcta es la <primera, segunda, tercera o cuarta>. <Por qué, y por qué cada otra no.></details>

## Resumen
<De 4 a 6 viñetas.>

## Código verificado
<Tabla: bloque, herramienta y versión, placa o entorno, verificado, validado, fecha. Si algo no se probó en hardware, decirlo.>

## Fuentes
- [<Sitio: página>](<url de la sección>). <Qué se tomó de ella.>
```

- **Bloques de código**: llevan lenguaje y, si son un archivo, su nombre (` ```cpp sensor.ino `).
- **Figuras**: los esquemas van como diagrama SVG, nunca en ASCII. Las listas y tablas se escriben en Markdown.
- **Conceptos clave**: las definiciones y los casos borde importantes van en una cita (`> `).
- **Quiz**: de 4 a 5 preguntas de dificultad media, que exijan entender el tema, sin trampas. Con código, al menos una de "¿qué imprime?" y una de "¿dónde está el bug?". Cada pregunta tiene 4 opciones, con la correcta en distinta posición, y al menos dos desarrolladas por igual: la correcta nunca se nota por ser la más larga.
- **Fuentes**: es la última sección e incluye cada fuente usada, propia o del usuario.
