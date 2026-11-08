---
name: tool:a3
description: Escribe un A3 al estilo Toyota (una sola página con problema, causa, contramedida, plan y seguimiento) a partir de la conversación y el código, como alternativa corta y humana a un spec. Usar cuando el usuario pida un A3, o quiera dejar por escrito un problema o un cambio antes de implementarlo sin escribir un spec completo.
---

# A3

Un A3 es la **historia de un problema contada en una página**: qué pasa, por qué pasa, qué se va a hacer y cómo se va a saber que funcionó. Viene de Toyota, que lo escribe en una hoja A3 justamente porque el espacio no alcanza para todo: obliga a **sintetizar**, y lo que no entra probablemente no se entendió. Reemplaza al spec cuando alcanza con que alguien (una persona o un agente) entienda el problema y la decisión; no lista historias de usuario ni contratos.

Se escribe como lo contaría el dueño a un compañero: frases cortas, en el vocabulario del proyecto, con los números y nombres concretos que salieron de mirar el código o los datos. Cada casillero responde **una pregunta**; si la respuesta no está, va la pregunta abierta, no una suposición.

## Pasos

1. **Juntar los hechos.** El gemba de un proyecto de software es el código, los logs, los tests y el comportamiento real: leer lo que el problema toca y reproducirlo si se puede, en vez de describirlo de memoria. Si el pedido es una solución ("agregar caché"), buscar el problema que la motiva. Hecho cuando cada afirmación de la situación actual sale de algo visto (un archivo, una medición, un error) y la brecha entre lo que pasa y lo que debería pasar se puede decir con un número o un caso concreto.

2. **Escribir el A3** con el formato de abajo, en `docs/a3/<slug>.md` (o donde el proyecto ya guarde sus A3). Primero la columna izquierda entera; recién con la causa escrita se pasa a las contramedidas. Hecho cuando cada casillero tiene su respuesta o su pregunta abierta y el documento entra en una pantalla y media.

3. **Leerlo al revés**, de abajo hacia arriba: ¿el seguimiento mide el objetivo? ¿el plan aplica la contramedida elegida? ¿la contramedida ataca la causa del análisis? ¿esa causa explica la brecha de la situación actual? Y el análisis de arriba hacia abajo: cada "¿por qué?" baja un nivel y, leído hacia arriba, "por lo tanto" encadena. Hecho cuando cada eslabón se sostiene; uno que no, se corrige o queda como pregunta abierta.

4. **Compartirlo** con el usuario: la ruta, la historia en tres líneas (brecha, causa, contramedida) y las preguntas abiertas. El A3 se reescribe con lo que responda; es un borrador vivo, no un entregable cerrado.

## Formato

```markdown
# <Título: el cambio o la mejora, en pocas palabras>

<Dueño> · <fecha>

## 1. Contexto
<Por qué importa esto ahora y a quién afecta. Dos o tres líneas.>

## 2. Situación actual
<Qué pasa hoy, con hechos: el caso, el número, dónde ocurre. Un diagrama o una tabla chica si se entiende mejor visto.>

## 3. Objetivo
<Qué resultado concreto se busca, cuánto y para cuándo. Un resultado, nunca una solución: "el import de 10k filas tarda menos de 5 s", no "agregar un worker".>

## 4. Análisis
<Por qué existe la brecha. Una cadena de porqués hasta la causa que se puede atacar, cada eslabón con su evidencia.>

## 5. Contramedidas
<Dos o tres alternativas, una línea cada una con su costo y su riesgo, y cuál se elige y por qué. La elegida dice qué causa del análisis ataca.>

## 6. Plan
<Qué se hace, en qué orden y quién lo hace (persona o agente). Pasos que se puedan tachar.>

## 7. Seguimiento
<Cómo se va a saber que funcionó: el test, la medición o el caso que se vuelve a mirar, y cuándo. Qué efecto colateral vigilar.>

## Preguntas abiertas
<Solo si quedan. Cada una dice a qué casillero afecta.>
```

- Los casilleros 1 a 4 son el problema; 5 a 7, la respuesta. Un casillero de más de seis líneas está diciendo algo que no hace falta o mezclando dos ideas.
- Contramedida y no solución: es la mejor respuesta conocida hoy a esta causa, y el seguimiento dice si hay que cambiarla.
- Un problema que se resuelve mirando y corrigiendo en el momento no necesita A3: decirlo y proponer arreglarlo directo. Uno demasiado grande para un ciclo se parte, y el A3 cubre la primera parte.
