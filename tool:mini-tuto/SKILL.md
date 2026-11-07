---
name: tool:mini-tuto
description: Propone una actividad práctica corta para empezar a entender una tecnología (ej. ajustar una grilla en un sitio web) y guía al usuario paso a paso mientras hace los cambios. Usar cuando el usuario pida un mini tuto o una tarea para aprender o probar una tecnología.
---

# Mini tuto

Un mini tuto es **una sola idea** de una tecnología, aprendida con **las manos del usuario en el teclado**: el usuario escribe cada cambio y ve qué provoca, el agente señala dónde tocar, explica por qué y revisa. El agente escribe cambios del tuto solo si el usuario desiste. Se escribe en el idioma y el registro del usuario.

## Pasos

1. **Elegir la actividad.** Sacar del pedido la tecnología y la tarea. El terreno es siempre el proyecto existente: el del directorio actual o el que nombre el usuario. Leer su código y elegir una tarea sobre lo que ya tiene; si solo nombra la tecnología, la más chica que muestre su idea central. Si el directorio no tiene proyecto o la tecnología no aparece en él, preguntar en qué proyecto hacerlo. Si no tiene ninguno, proponer un proyecto mínimo en un directorio nuevo, con lo justo para que corra y la tarea tenga dónde hacerse, y crearlo cuando el usuario acepte. Hecho cuando la tarea se resuelve en 3 a 5 pasos sobre archivos reales del proyecto, cada uno con un efecto visible.

2. **Preparar el punto de partida.** Ubicar los archivos que la tarea toca, averiguar cómo se levanta el proyecto y mirar `git status` para distinguir después lo que ya estaba sin commitear. Si la tarea choca con esos cambios, avisar antes de empezar. Comprobar que el proyecto arranca y dejarlo como estaba: lo levanta el usuario con el comando que le da el agente. Si no arranca, decir qué falta y pedir permiso antes de instalar o configurar algo; si no tiene arreglo, proponer otra tarea u otro proyecto. Hecho cuando el arranque está comprobado, no quedó nada corriendo que no estuviera antes y hay un comando o una URL para ver el resultado.

3. **Presentar el mini tuto** en un mensaje corto: la tarea, la idea que se lleva el usuario, qué va a ver al final, cómo levantarlo y abrirlo, y el primer paso.

4. **Guiar de a un paso por mensaje**, con el formato de abajo, y esperar al usuario. Cuando avisa que terminó, leer el archivo y correr lo que se pueda:
   - Si está bien, confirmar en una línea qué demostró ese cambio y dar el paso siguiente.
   - Si está mal, dar una pista que señale la línea y el síntoma. La solución va cuando el usuario la pide o cuando la pista no alcanzó.
   - Si pregunta algo, responder y retomar el paso en curso.
   - Si pide que el agente lo haga, darle la solución para que la escriba y preguntarle si prefiere desistir.
   - Si desiste o quiere cortar, preguntar si el agente termina los pasos que faltan, explicando cada uno, o si queda como está, y pasar al cierre.

   Uno de los pasos lleva un valor al extremo o rompe algo a propósito, para que se vea el límite de la idea, y termina con el usuario volviéndolo a su valor. Hecho cuando cada paso está en el archivo y revisado por el agente, o cuando el usuario desistió o cortó.

5. **Cerrar** con la idea en dos o tres líneas, los archivos que cambiaron, cómo descartar solo lo del tuto si fue para practicar, y un desafío en otra parte del proyecto para resolver sin guía, con el concepto o la doc oficial por donde empezar. Si el tuto quedó a medias, el cierre son solo los archivos tocados y cómo descartarlos.

   Para descartar, según el archivo:
   - Sin cambios previos: `git restore <archivo>`.
   - Con cambios sin commitear de antes del tuto, o fuera de git: las líneas exactas a revertir a mano, porque `git restore` se llevaría también el trabajo previo.
   - Creado durante el tuto: borrarlo. Si es el proyecto mínimo, borrar su directorio.

## Formato de un paso

**Paso 2 de 4: que las columnas se acomoden solas**

**Qué tocar:** `estilos.css:12`, la regla `.grilla`, que hoy dice `grid-template-columns: 200px 200px 200px`.

**Qué cambiar:** reemplazar ese valor por `repeat(auto-fit, minmax(200px, 1fr))`.

**Tené en cuenta:** `minmax` fija el ancho mínimo de cada columna y `1fr` reparte el espacio que sobra. `auto-fit` decide cuántas columnas entran, así que ya no hace falta un media query para esto.

**Qué deberías ver:** al angostar la ventana, las tarjetas bajan de fila y nunca quedan por debajo de 200px.

Avisame cuando lo tengas.
