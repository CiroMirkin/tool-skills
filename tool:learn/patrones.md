# Patrones de marcado

Los componentes que `plantilla.html` ya estiliza. Cada sección de la lección se arma con ellos. Todo el texto va en mayúscula inicial normal, sin "·" ni rayas largas.

## Código y diagramas

Una línea sola, sin nada más, que `leccion.py armar` reemplaza:

```text
@@proyecto:src/actions/save-ingreso.ts:30-58@@
@@ejemplo:turnos.py:1-25@@
@@svg:flujo-transaccion.svg@@
@@svg:secuencia-rollback.svg@@
```

El código se copia del archivo, nunca se tipea. Un diagrama se llama `flujo-…` o `secuencia-…`: el nombre le dice al comprobador de qué tipo es.

## Un modelo resuelto

Dentro de cada escalón de `practica`, arriba de la consigna. Muestra la pieza ya escrita, con el idioma de la tecnología, y una nota que lo señala.

```html
<h4>Antes de empezar, el modelo: una transacción de dos operaciones</h4>
<p>Una frase: qué hace este código. Es otra operación que la del escalón, escrita igual.</p>
@@ejemplo:modelo/01-transferir.ts:1-18@@
<ul>
  <li>Línea 4: <code>tx</code> y no <code>prisma</code>. Solo lo que pasa por <code>tx</code> queda dentro de la transacción.</li>
  <li>Línea 5: <code>findUniqueOrThrow</code> corta la transacción si no existe la fila, sin un chequeo de <code>null</code> aparte.</li>
</ul>
```

## Leer un fragmento del proyecto

```html
<h3>Guardar un ingreso</h3>
<p>Una frase de contexto: qué hace este código y quién lo llama.</p>
@@proyecto:src/actions/save-ingreso.ts:30-58@@
<div class="pregunta">
  <p><strong>Antes de seguir, leelo vos.</strong> Respondé en voz alta:</p>
  <ul><li>¿Qué pasa con lo ya escrito si falla la línea 41?</li></ul>
</div>
<details><summary>Ver la explicación</summary>
  <p>Línea 31: …</p>
</details>
```

## Un escalón de práctica

Abre la sección `practica` una tabla pieza a escalón (qué pieza practica cada escalón; los fragmentos del proyecto la usan para declarar `Piezas que usa`). La clase va en la etiqueta: `Ejecutar`, `Completar` o `Escribir`. El dominio va en `data-dominio`: `proyecto` (recorte del dominio real) o `ficticio`.

```html
<div class="escalon" id="escalon-1" data-dominio="proyecto">
  <h3><label><input type="checkbox"> Escalón 1, una transacción de dos operaciones</label></h3>
  <p><span class="etiqueta">Completar</span> Pieza nueva: leer y escribir en la misma transacción.</p>
  <p>Qué hacer, en una o dos frases, y en qué archivo (<code>practica/01-stock-simple/stock.ts</code>).</p>
  <p class="comprobacion">Comprobá con <code>npx vitest run practica/01-stock-simple</code>. Al empezar está en red: <code>esperaba 7, recibió 10</code>.</p>
  <details class="pista"><summary>Ayuda 1: releé</summary>
    <p>Releé <a href="#concepto">el concepto</a>, el peldaño de la transacción interactiva.</p>
  </details>
  <details class="pista"><summary>Ayuda 2: preguntate</summary>
    <p>¿Con qué cliente se tiene que hacer la segunda operación para quedar dentro de la transacción?</p>
  </details>
</div>
```

En `codigo-proyecto`, cada fragmento abre con las piezas y los escalones que las practicaron:

```html
<p class="piezas">Piezas que usa: <a href="#escalon-1">leer y escribir juntos</a>, <a href="#escalon-3">validar dentro de la transacción</a>.</p>
```

## Un ejercicio de error

El tipo va en la etiqueta: `Error` (da un resultado incorrecto), `Mala práctica` (funciona pero cuesta) o `Anti-patrón` (solo si una fuente lo define con ese nombre).

```html
<div class="ejercicio" id="bug-1">
  <h3>Ejercicio 1</h3>
  <p>Contexto de una o dos frases.</p>
  @@ejemplo:cobros.py:10-30@@
  <div class="pregunta"><p>¿Qué está mal? Si lo ejecutás con dos cobros a la vez, ¿qué esperás que quede en la cuenta?</p></div>
  <details class="respuesta"><summary>Ver la respuesta</summary>
    <p><span class="etiqueta">Error</span></p>
    <p>Qué falla y en qué línea.</p>
    <p>Lo que se ve al ejecutarlo: <code>saldo = 70, esperado 40</code>.</p>
    <p>Por qué ocurre, con enlace a la fuente. Qué sección releer para evitarlo.</p>
  </details>
</div>
```

## Una tarea con ayuda

Cada paso tiene un resultado que se puede comprobar. Las ayudas van de la más suave a la más concreta, y ninguna lleva código de la solución. Una ayuda manda a releer una sección o hace una pregunta.

```html
<ol class="pasos">
  <li>
    <label><input type="checkbox" class="hecho"> <strong>Reproducí el error.</strong></label>
    <p>Qué hacer, en el repo del usuario, y qué tiene que ver al terminar.</p>
    <details class="pista"><summary>Ayuda 1: releé</summary>
      <p>Releé <a href="#codigo-proyecto">el código del proyecto</a>, el fragmento del ingreso.</p>
    </details>
    <details class="pista"><summary>Ayuda 2: preguntate</summary>
      <p>¿Qué valor tendría que tener X antes de la línea 41?</p>
    </details>
    <details class="pista"><summary>Ayuda 3: si seguís trabado</summary>
      <p>Mirá <code>src/actions/save-ingreso.ts:41</code> y compará con el ejercicio 2.</p>
    </details>
  </li>
</ol>
```

Antes de la lista van el contexto, el objetivo observable y la rama donde trabajar. Después, `<h3>Cómo saber que terminaste</h3>` con el comando o la observación exacta.

## Fuentes y verificación

```html
<h3>Fuentes</h3>
<ul><li><a href="https://…">Nombre del documento, sección exacta</a>: qué dato respalda.</li></ul>
<h3>Qué se ejecutó</h3>
<table>
  <tr><th>Qué</th><th>Comando y versión</th><th>Resultado</th></tr>
  <tr><td>turnos.ts</td><td><code>npx tsx turnos.ts</code>, Node 24.22.1</td><td>imprime 2 filas, como dice la lección</td></tr>
</table>
```

## Otros

- Nota: `<div class="nota"><p>…</p></div>`. Aviso de algo que sorprende: `<div class="ojo">`.
- Un diagrama sale dentro de un `<figure class="diagrama">` que arma el script; el texto que lo introduce va antes.
