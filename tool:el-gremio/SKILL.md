---
name: tool:el-gremio
description: Somete una decisión a un gremio de 5 asesores (sub-agentes) que la analizan por separado, se revisan a ciegas y cierran con el veredicto de un presidente. Usar cuando el usuario escriba "/el-gremio", o traiga una decisión real con varias opciones y riesgo y pida perspectivas o validación ("¿X o Y?", "¿qué harías?", "¿es la decisión correcta?").
---

# El Gremio

Una pregunta, cinco **asesores** que piensan desde ángulos en tensión, una revisión **a ciegas** entre ellos y un **presidente** que sintetiza y decide. Es para decisiones con incertidumbre genuina donde equivocarse sale caro. Si la pregunta tiene una sola respuesta correcta, o es una tarea de crear o procesar (escribir un tweet, resumir un artículo), respondela directamente.

Todo sale en español: los sub-agentes, el reporte y la transcripción.

## Pasos

1. **Juntar contexto.** Leer el `CLAUDE.md` del proyecto, la carpeta de memoria, los archivos que nombró el usuario, las `transcripcion-gremio-*.md` previas del directorio de trabajo, y lo que toque la pregunta en concreto (si es de precios, datos de ingresos o lanzamientos pasados). Hecho cuando tenés los 2 o 3 archivos que más cambian el consejo: es una pasada rápida, no un relevamiento. Si la pregunta es tan vaga que no se puede encuadrar, hacé una sola pregunta aclaratoria y seguí.
2. **Encuadrar.** Escribir el **encuadre**, el texto que reciben los cinco. Hecho cuando contiene la decisión central, el contexto del mensaje, el contexto de los archivos (etapa, audiencia, restricciones, resultados previos, números) y qué está en juego, y describe las opciones sin inclinarse por ninguna.
3. **Convocar.** Lanzar los 5 asesores como sub-agentes en un solo mensaje, con la plantilla de asesor. En paralelo, para que ninguno lea a otro. Hecho cuando están las 5 respuestas.
4. **Revisar a ciegas.** Asignar al azar las letras A–E a las respuestas y anotar el mapeo. Lanzar 5 revisores nuevos en un solo mensaje, uno por ángulo, con la plantilla de revisor. Las letras ocultan quién dijo qué, así se juzga el argumento y no el estilo. Hecho cuando están las 5 revisiones.
5. **Sintetizar.** Lanzar un sub-agente presidente con la plantilla de presidente, ya con los nombres reales. Hecho cuando el veredicto tiene las cinco secciones y una sola recomendación.
6. **Reporte.** Escribir `reporte-gremio-<AAAAMMDD-HHMM>.html` en el directorio de trabajo y abrirlo. Un solo archivo con CSS inline, con aspecto de documento de briefing: fondo blanco, bordes sutiles, system font stack, un color de acento suave por asesor. Contenido, en orden:
   - la pregunta;
   - el veredicto del presidente, prominente (es lo que la mayoría lee);
   - un visual de acuerdo/desacuerdo: grilla o espectro con la posición de cada asesor;
   - la respuesta completa de cada asesor en un `<details>` cerrado;
   - lo más destacado de las revisiones en un `<details>` cerrado;
   - pie con fecha, hora y lo que se sometió al gremio.
7. **Transcripción.** Escribir `transcripcion-gremio-<mismo timestamp>.md` al lado del reporte: pregunta original, encuadre, las 5 respuestas, las 5 revisiones con el mapeo de letras revelado y el veredicto completo. Es lo que lee el paso 1 cuando se vuelve a convocar al gremio sobre la misma pregunta.

## Los asesores

Son estilos de pensamiento, no personajes. Las tensiones son a propósito: Contrario contra Expansionista (riesgo contra potencial), Primeros Principios contra Ejecutor (repensar todo contra hacerlo ya), y el Externo en el medio con ojos frescos.

- **El Contrario**: asume que la idea tiene un defecto fatal y lo busca; si todo se ve sólido, cava más hondo. Es el amigo que hace las preguntas que el usuario está evitando.
- **El Pensador de Primeros Principios**: se pregunta qué se está tratando de resolver en realidad, despoja los supuestos y reconstruye el problema desde cero. A veces su aporte es "estás haciendo la pregunta equivocada".
- **El Expansionista**: busca el potencial que los demás pasan por alto: qué podría ser más grande, qué oportunidad adyacente hay, qué se está subvalorando. Mira qué pasa si esto sale mejor de lo esperado; el riesgo es cosa del Contrario.
- **El Externo**: responde solo a lo que tiene enfrente, sin contexto del usuario ni de su rubro. Detecta la maldición del conocimiento: lo que es obvio para el usuario y confuso para cualquier otro.
- **El Ejecutor**: mira cada idea con la pregunta "¿qué hago el lunes a la mañana?". Le importa si se puede hacer y cuál es el camino más rápido; si una idea no tiene un primer paso claro, lo dice.

## Plantillas

Asesor:

```
Sos <asesor> en El Gremio.

Tu forma de pensar: <su descripción>

Pregunta traída al gremio:
---
<encuadre>
---

Respondé en español, desde tu ángulo y solo desde él, con toda la fuerza que tenga. Si ves un defecto fatal o un potencial enorme, decilo de frente. Los otros asesores cubren los demás ángulos y el equilibrio lo pone la síntesis después.

Entre 150 y 300 palabras. Empezá directo por el análisis.
```

Revisor:

```
Revisás los resultados de El Gremio desde el ángulo de <asesor>: <su descripción>

Cinco asesores respondieron por separado esta pregunta:
---
<encuadre>
---

**Respuesta A:** <respuesta>
**Respuesta B:** <respuesta>
**Respuesta C:** <respuesta>
**Respuesta D:** <respuesta>
**Respuesta E:** <respuesta>

Respondé en español, citando las respuestas por letra:
1. ¿Cuál es la más sólida y por qué? Elegí una.
2. ¿Cuál tiene el punto ciego más grande, y qué le falta?
3. ¿Qué se les pasó a las cinco que el gremio debería considerar?

Menos de 200 palabras.
```

Presidente:

```
Sos el Presidente de El Gremio. Sintetizá a los 5 asesores y sus revisiones en un veredicto final.

Pregunta traída al gremio:
---
<encuadre>
---

RESPUESTAS DE LOS ASESORES:
**El Contrario:** <respuesta>
**El Pensador de Primeros Principios:** <respuesta>
**El Expansionista:** <respuesta>
**El Externo:** <respuesta>
**El Ejecutor:** <respuesta>

REVISIONES ENTRE PARES (letras: <mapeo>):
<las 5 revisiones>

Escribí el veredicto en español con esta estructura exacta:

## Donde Coincide el Gremio
Lo que varios asesores dijeron por separado: señales de alta confianza.

## Donde Choca el Gremio
Los desacuerdos genuinos, con los dos lados y por qué asesores razonables difieren.

## Puntos Ciegos que el Gremio Detectó
Lo que solo apareció en la revisión entre pares.

## La Recomendación
Una respuesta concreta, comprometida, con su razonamiento. Si el disidente tiene el argumento más sólido, alineate con él aunque la mayoría opine otra cosa, y explicá por qué.

## Lo Primero que Deberías Hacer
Un único paso concreto.
```
