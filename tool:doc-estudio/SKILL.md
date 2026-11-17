---
name: tool:doc-estudio
description: Escribe dos .md complementarios que enseñan un tema desde cero, fundamentos (conceptos explicados, diagramas, escenarios) y avanzado (implementación, mantenimiento, testing, medición), con un repo de pruebas, tres tareas con tests por doc, quiz y fuentes. Usar cuando el usuario pida un doc de estudio, una lección o aprender un tema a fondo.
---

# Doc de estudio

El resultado es un **par de lecciones**, dos `.md` que se complementan, y un repo de pruebas junto a ellos. Se escribe en el idioma y el registro del usuario.

- `<tema>-fundamentos.md` enseña **qué es cada cosa, dónde está y qué responsabilidad tiene**: conceptos, decisiones, escenarios, problemáticas, ejemplos prácticos, buenas y malas prácticas. Casi sin código; se apoya en diagramas.
- `<tema>-avanzado.md` **lo construye**: implementación completa, mantenimiento, testing, medición, seguimiento y trazabilidad. Da por leído fundamentos y enlaza a él en vez de repetirlo.
- `<tema>-pruebas/` guarda el código de ambos y los tests de sus tareas.

Quien lee no conoce el tema. Cada término se **explica**, no se describe: después de leerlo el lector puede decir con sus palabras qué es, para qué sirve, cómo funciona y qué pasa sin él. Cada dato concreto lleva la fuente que lo respalda.

## Pasos

1. **Leer el pedido y medir al lector.** Sacar de él el tema, las fuentes que pasa el usuario, el proyecto de ejemplo si nombra uno y el destino. Antes de investigar, preguntar con `AskUserQuestion` cuánto sabe el usuario del tema y de cada tecnología de la que depende (hasta tres ejes; para un MCP en Next: MCP, APIs, Next). Cada eje ofrece **tres niveles, cada uno con un ejemplo de lo que esa persona sabe hacer**, para que pueda dimensionarse:

   - API, nivel 1: "nunca llamé a una". Nivel 2: "llamé a una con `fetch` y leí su JSON". Nivel 3: "diseñé una con autenticación y versiones".

   El nivel decide el piso de cada doc: lo que cae por encima del nivel del lector se explica completo, lo que cae por debajo se nombra y se enlaza.

   Sin destino pedido, las lecciones van donde el proyecto guarda las suyas; si no hay ninguna, al directorio actual. Si el destino ya tiene lecciones, como `roadmap-arduino-site`, leer su documentación (`README.md`, `CLAUDE.md`, `CONTEXT.md`) y dos lecciones del mismo nivel: su formato, sus reglas y sus herramientas mandan sobre las de esta skill; las exigencias de los pasos 3, 4 y 8 se mantienen.

   Si el tema no entra en un par de lecciones, proponer el recorte o la lista de pares antes de seguir. Crear junto a los docs dos carpetas:
   - `<tema>-pruebas/`, con `README.md` de set-up. Se entrega y vive con los docs.
   - `<tema>-trabajo/`, con lo intermedio (fuentes, glosario, salidas). Si el destino está en un repo, ponerla donde git la ignore.

   Hecho cuando están anotados tema, lector con su nivel en cada eje, destino y formato, y las dos carpetas existen.

2. **Elegir el caso**: el sistema concreto del que salen todos los ejemplos.
   - Si el usuario nombra un proyecto, o el tema aparece en el proyecto actual, usar ese, salvo que sus documentos pidan otro ejemplo o prohíban citarlo.
   - Si no, inventar el sistema más chico donde el tema importe, y anotar sus nombres, pines y números para repetirlos iguales en toda la lección.

   Cada actor del caso es una cosa real y nombrada (no "un agente de IA", sino Claude Desktop; no "un proveedor", sino el que el lector conocería). Hecho cuando el caso explica por qué alguien necesitaría este tema, con una situación que se rompe sin él, y cada actor tiene su ejemplo concreto.

3. **Investigar.** Reunir, en este orden:
   - todas las fuentes del usuario y el `RESOURCES.md` del proyecto si existe;
   - las skills del tema, en `.claude/skills` del proyecto o las globales (por ejemplo `cpp-reviewer` para firmware), que aportan criterio pero no se citan como fuente;
   - fuentes propias, buscadas siempre aunque las del usuario parezcan alcanzar: documentación oficial, specs, hojas de datos, el repo del proyecto. Un artículo secundario entra solo si explica algo que la fuente primaria no explica.

   Llevar cada dato concreto (un límite, un valor por defecto, un comportamiento) hasta su **dueño**: la fuente que lo define, en la versión que usa la lección, enlazada a la sección exacta. Armar con esto la **escalera**: los conceptos ordenados por dependencia, desde lo que entiende alguien que recién llega hasta los límites, lo que hay debajo, los modos de falla y las alternativas. Repartirla: los peldaños que son concepto, decisión o responsabilidad van a fundamentos; los que son construir, mantener, probar o medir van a avanzado.

   De cada fuente que la lección va a nombrar (una empresa, un estándar, un producto usado como ejemplo) anotar **qué es y por qué se la usa acá**, porque la lección lo explica antes del nombre.

   Hecho cuando cada peldaño tiene su dueño y su doc, cada fuente del usuario está usada o anotada como "no aportó" con el motivo, y al menos una fuente propia sostiene algo de la lección.

4. **Escribir el código y las tareas antes que la prosa.** Cada ejemplo vive como archivo real en `<tema>-pruebas/` y se queda ahí. Un bloque llega a dos estados:
   - **Verificado**: compila o pasa el analizador con la herramienta real, para la placa o versión que la lección nombra, sin errores ni advertencias propias.
   - **Validado**: se ejecutó y su salida coincide con lo que la lección dice que pasa.

   Aplicar estas reglas a cada bloque:
   - Un fragmento se copia textual de un programa completo que está verificado.
   - Un ejemplo de lo que está mal se comprueba igual: tiene que dar el error o el síntoma que la lección describe.
   - Si hace falta hardware, probar la lógica pura en la máquina (por ejemplo con `g++`) y dejar el resto como verificado, sin validar. Cargar una placa conectada solo con el permiso del usuario.
   - Si falta la herramienta, pedir permiso para instalarla. Un bloque que no llega a verificado se reescribe o se saca.
   - Pasar el código por las skills de revisión del tema, si las hay.

   Después, las **tareas**: tres por doc, en `<tema>-pruebas/tareas/<doc>-N/`, cada una con el esqueleto a completar, su test y su solución aparte. Son concretas, se hacen en menos de 20 minutos y suben de nivel: la 1 es básica y la 3 trabaja el concepto más avanzado de ese doc. Cada test falla con el esqueleto y pasa con la solución.

   Cuando todo está verificado, borrar las dependencias instaladas (`node_modules`, `.venv`, `target`) y dejar el lockfile y el `README.md` con el set-up: qué instalar, con qué comando y cómo correr los ejemplos y los tests. El repo entregado pesa lo que pesa su código.

   Hecho cuando cada bloque tiene su estado, su comando y la versión de la herramienta anotados, las salidas quedaron en la carpeta de trabajo, cada tarea falla y pasa como se espera, y el repo no trae dependencias.

5. **Diseñar los diagramas.** Un diagrama entra donde el lector tendría que armarse el dibujo en la cabeza. Si una tabla o un párrafo ya lo muestra igual de bien, queda uno solo de los dos. Los nombres y los datos de ejemplo son los del caso y los mismos que usa el texto.

   Fundamentos se apoya en los diagramas más que en el código: **contexto de sistema** siempre (cada actor con su ejemplo concreto y su responsabilidad, para saber dónde está cada cosa), y según el tema flujo, secuencia, estados, casos de uso y C4. Avanzado dibuja lo que la implementación necesita (secuencias, estados, despliegue).

   Invocar la skill `diagram-design` para cada uno, comprobar el HTML con su `self_check.py` y exportarlo con `export_svg.py --system-fonts`. El SVG va en la carpeta de imágenes del proyecto o en `diagramas/` junto a las lecciones, con el HTML fuente al lado. Se inserta con `![qué muestra el diagrama](ruta.svg)`, justo después del párrafo que lo introduce.

   Convertir cada SVG a imagen y mirarla:

   ```bash
   uv run --with pymupdf python -c "import pymupdf; pymupdf.open('d.svg')[0].get_pixmap(dpi=100).save('d.png')"
   ```

   Hecho cuando cada diagrama pasó el chequeo y en su imagen cada rótulo queda dentro de su forma y cada flecha llega a destino.

6. **Redactar** `<tema>-trabajo/fundamentos.fuente.md` y `avanzado.fuente.md` con el formato de abajo, recorriendo la escalera en orden. Escribir con la claridad de Martin Kleppmann, en estilo clásico: le mostrás al lector algo que podés ver y la transición de cada sección sale de la anterior. Un programa completo se inserta con una línea `@@carpeta/archivo@@` dentro de su bloque de código, relativa a `<tema>-pruebas/`. Armar cada lección con:

   ```bash
   python3 ~/.claude/skills/tool:doc-estudio/scripts/leccion.py armar fundamentos.fuente.md ../<tema>-fundamentos.md --codigo ../<tema>-pruebas
   ```

   Reglas de explicación:
   - **Explicar un término** es decir qué es, para qué sirve, cómo funciona con un caso del lector y qué se rompe sin él. Una definición de una línea queda en descripción.
   - **Presentar antes de nombrar.** Una fuente, un estándar o una empresa recibe, en un párrafo previo y propio, qué es y por qué la lección se apoya en ella; recién después se la nombra.
   - Fundamentos lleva solo el fragmento de código sin el cual el concepto no se ve (la forma de un mensaje, una cabecera, una línea de configuración): hasta 5, de hasta 15 líneas. Todo lo demás es diagrama, tabla, escenario o ejemplo en prosa.

   Después, hacer el **glosario de control** en la carpeta de trabajo: cada término técnico de las dos lecciones, en orden de aparición, con la línea donde se define, contando títulos, diagramas, código y quiz. El lector tiene que encontrar la definición antes del primer uso; avanzado reutiliza fundamentos con un enlace a la sección que lo explica. Una palabra usada con dos sentidos se aclara o se cambia, y lo que se define en una sección que se puede saltear entra en la condición para saltearla.

   Hecho cuando cada peldaño de la escalera está en su doc, cada dato concreto tiene su enlace y cada término del glosario tiene su línea de definición.

7. **Editar** cada `.fuente.md`. Seguir [`edicion.md`](edicion.md) y después invocar `humanizer:humanizer` sobre la prosa, dejando intactos el código, los comandos y los enlaces. Luego pedir una segunda pasada con ese mismo archivo: con `codex` o `gemini` si están instalados, y si no con un subagente que reciba solo la lección, `edicion.md` y quién es el lector con su nivel. Revisar cada cambio contra el original antes de aceptarlo. Hecho cuando las dos pasadas terminaron en ambos docs, ningún dato cambió de sentido y las lecciones están armadas de nuevo.

8. **Comprobar los archivos finales.** Las ediciones pueden tocar lo ya revisado, así que todo se comprueba sobre los `.md` terminados:

   ```bash
   python3 ~/.claude/skills/tool:doc-estudio/scripts/leccion.py comprobar ../<tema>-fundamentos.md --codigo ../<tema>-pruebas --fundamentos
   python3 ~/.claude/skills/tool:doc-estudio/scripts/leccion.py comprobar ../<tema>-avanzado.md --codigo ../<tema>-pruebas
   ```

   El script revisa que cada bloque de código esté en un archivo de las pruebas, que el repo tenga README y ninguna dependencia instalada, las imágenes, los enlaces y sus anclas, las rayas largas, los marcadores, el largo de las opciones del quiz, que cada respuesta ocupe una línea, que haya tres tareas, y con `--fundamentos` el tope de fragmentos. Después:
   - Si cambió un archivo de las pruebas después de verificarlo, compilarlo y ejecutarlo de nuevo.
   - Corregir o quitar los enlaces rotos. Si un sitio rechaza a `curl`, confirmar la página de otra forma.
   - Resolver el quiz leyendo solo la lección: cada respuesta tiene que salir del texto.
   - Hacer una lectura final de fundamentos como el lector del nivel más bajo elegido: cada término que no entienda sin salir del doc es un hueco a explicar.
   - Correr las herramientas de verificación del destino, si tiene.

   Hecho cuando el script termina sin problemas en los dos docs y lo demás pasa, o lo que quedó sin pasar está anotado con el motivo.

9. **Entregar.** Informar los archivos y sus diagramas, el caso elegido, el nivel del lector, qué bloques quedaron verificados y cuáles validados, las tareas con su tiempo estimado, las fuentes del usuario que no aportaron, y qué herramienta hizo la segunda pasada.

## Formato

Los dos docs comparten el quiz, las tareas, el resumen y las fuentes; lo demás cambia.

**Fundamentos**

```markdown
# <Tema>: fundamentos

<Párrafo con la idea central: qué es, en palabras de quien recién llega.>

## Por qué te importa
<La situación del caso que se rompe sin este tema, con sus síntomas.>

## Antes de empezar
<Lo que hace falta saber según el nivel elegido. Avisar qué se puede saltear.>

## El sistema y sus actores
<Diagrama de contexto de sistema. Después, cada actor con su ejemplo concreto y su responsabilidad.>

## Conceptos
### <Concepto>
<Explicado: qué es, para qué sirve, cómo funciona con el caso, qué se rompe sin él. Diagrama donde ayude.>

## Escenarios y decisiones
<Casos concretos del sistema, qué opción conviene en cada uno y por qué.>

## Buenas y malas prácticas
<Cada práctica con el escenario donde se ve y la razón.>

## Tareas
## Quiz
## Resumen
## Fuentes
```

**Avanzado**

```markdown
# <Tema>: avanzado

<Párrafo: qué se construye y qué de fundamentos se da por sabido, con enlace.>

## Implementación
### <Pieza>
<Qué hace, el programa completo y qué observar al correrlo. Un ejemplo mínimo, uno típico y uno aplicado al caso.>

## Mantenimiento
<Versiones, cambios del proveedor, qué revisar y cada cuánto.>

## Testing
<Qué se prueba, cómo y qué tests protegen cada riesgo.>

## Medición, seguimiento y trazabilidad
<Qué medir, qué registrar para reconstruir un caso y cómo seguirlo.>

## En profundidad
<Lo que hay debajo, los límites con sus números, los modos de falla, y cuándo conviene otra alternativa.>

## Errores comunes
### <Error>
<Síntoma, código `// Mal`, código `// Bien` y por qué.>

## Tareas
## Quiz
## Resumen
## Código verificado
<Tabla: bloque, herramienta y versión, entorno, verificado, validado, fecha. Si algo no se probó en hardware, decirlo.>

## Fuentes
```

- **Bloques de código**: llevan lenguaje y, si son un archivo, su nombre (` ```cpp sensor.ino `).
- **Figuras**: los esquemas van como diagrama SVG, nunca en ASCII. Las listas y tablas se escriben en Markdown.
- **Conceptos clave**: las definiciones y los casos borde importantes van en una cita (`> `).
- **Tareas**: exactamente tres, `### Tarea N. <Nombre>`, al final del doc. Cada una dice qué hacer en el repo de pruebas, el comando que corre su test, el tiempo estimado (menos de 20 minutos) y qué concepto trabaja. La 1 es básica y la 3 es la del concepto más avanzado del doc. El enunciado se resuelve con lo visto en ese doc. La solución vive en el repo, aparte.
- **Quiz**: de 4 a 5 preguntas de dificultad media, que exijan entender el tema, sin trampas. Con código, al menos una de "¿qué imprime?" y una de "¿dónde está el bug?". Cada pregunta tiene 4 opciones, con la correcta en distinta posición, y al menos dos desarrolladas por igual: la correcta nunca se nota por ser la más larga. La respuesta va en **una sola línea**: `<details><summary>Ver respuesta</summary>La correcta es la <primera, segunda, tercera o cuarta>. <Por qué, y por qué cada otra no.></details>`. En el PDF (`tool:pdf`) sale boca abajo, para leerla dando vuelta la página.
- **Fuentes**: es la última sección e incluye cada fuente usada, propia o del usuario.
