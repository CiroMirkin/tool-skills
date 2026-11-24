---
name: code:cuestioname
description: Sortea al azar un concepto, feature o parte del sistema del proyecto y arma un cuestionario HTML de 4 preguntas sobre su funcionamiento e implementación; cada error se explica y se vuelve a preguntar con otros datos hasta acertar. Usar cuando el usuario escriba "/code:cuestioname", o pida que lo cuestionen, que le tomen examen del código o comprobar que entiende el sistema en el que trabaja.
---

# Cuestioname

El resultado es **un `.html`**: una página de contexto breve y un cuestionario de cuatro preguntas sobre **una** parte real del proyecto, elegida por sorteo. Quien responde queda con la prueba de que entiende cómo funciona y cómo está implementada esa parte. Un error no cierra la pregunta: se **explica** y se **vuelve a preguntar** con otros datos hasta acertar.

La mecánica de preguntas (opciones, una correcta, explicación por opción, color solo en la elegida y la correcta) es la del quiz de `roadmap-arduino-site`. La prosa sigue la claridad de Martin Kleppmann: del problema al mecanismo, con ejemplos de juguete. Se escribe en el idioma del usuario.

## Pasos

1. **Listar candidatos.** Recorrer el proyecto (el directorio actual o el que nombre el usuario) y anotar entre 8 y 15 partes con comportamiento propio: un módulo, una feature, un flujo, una regla de negocio, una estructura de datos. Si el usuario nombró un área, el sorteo es dentro de ella. Hecho cuando cada candidato tiene un archivo de entrada y una frase de qué hace.
2. **Sortear.** Elegir con `shuf -n1` sobre la lista, sin criterio propio: el azar evita que siempre salga lo más vistoso. Si el sorteo cae en algo trivial (un alias, una constante), resortear.
3. **Leer a fondo la parte sorteada.** Seguir el código desde la entrada hasta el último efecto: llamadores, llamados, casos de error, tests. Hecho cuando se puede contar el recorrido de un dato de ejemplo concreto de punta a punta y se conocen las razones de al menos dos decisiones de diseño.
4. **Escribir las cuatro preguntas.** Cada una prueba una cosa distinta, en este reparto: (a) el recorrido o el flujo, (b) un caso borde o de error, (c) el porqué de una decisión de diseño, (d) qué pasa si se cambia algo. Dificultad media: para acertar hay que haber entendido el mecanismo, nunca un detalle arbitrario ni una trampa de redacción.
   - Cada **variante** lleva 4 opciones, una correcta, y una explicación (`porque`) para cada opción, con el motivo de por qué esa distractora tienta.
   - Cada pregunta lleva **dos variantes o más**: la primera es la pregunta; las siguientes ponen a prueba el mismo punto con otros datos o en otro caso (otro valor, otro archivo, otro estado), de modo que acertar la repregunta exige haber entendido, no recordado la letra.
   - Cada pregunta lleva un **repaso**: la explicación del mecanismo con el fragmento real (`archivo:línea`) en `<pre><code>`. Es lo que se muestra tras fallar.
   - Hecho cuando cada respuesta correcta tiene su **dueño** (una línea de código leída o un comando ejecutado) y ninguna distractora es absurda: cada una describe un malentendido plausible.
5. **Escribir el contexto.** Una página como máximo, dentro de `<details class="fondo">` si es fondo para principiantes: el problema que resuelve la parte, su mecanismo y un diagrama HTML con datos de ejemplo. Las respuestas no aparecen literales acá.
6. **Armar el HTML** copiando [`plantilla.html`](plantilla.html) y llenando sus marcadores `{{...}}`; el JavaScript de la plantilla ya sortea el orden de las opciones, revela las explicaciones, repregunta y cierra, así que solo se completa `PREGUNTAS`. Guardar en `/tmp/AAAA-MM-DD-cuestioname-<slug>.html` (fecha de hoy; fuera del repo, para que no entre al control de versiones).
7. **Verificar y abrir.** Revisar que el archivo no tenga marcadores `{{` sin llenar, que todo bloque de código sea `<pre>` y que el JS no dé error (`node --check` sobre el `<script>` extraído). Abrir con `xdg-open`. Hecho cuando las cuatro preguntas se pueden recorrer, también la ruta de error y repregunta.
8. **Informar** al usuario la ruta, qué parte salió sorteada y de qué archivos salen las preguntas.

## Reglas de la interfaz

- Sin separador "·" y sin mayúsculas sostenidas ni `text-transform: uppercase`: mayúscula inicial normal y coma, barra o salto de línea para separar.
- Un solo archivo con CSS y JS inline, una página larga con índice, legible en celular. Los diagramas son HTML (`.diagrama`, `.caja`, `.flecha`), nunca texto ASCII.
- Las notas importantes (definiciones, casos borde) van en `.callout`.
