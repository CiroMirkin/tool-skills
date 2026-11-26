---
name: code:dev-work
description: Principios de trabajo para escribir o cambiar código (rama propia, que funcione, que esté bien, evidencia). Usar al implementar una feature, arreglar un bug o refactorizar, o cuando el usuario escriba "/code:dev-work".
---

# Dev work

Cada cambio pasa en orden por **que funcione**, **que esté bien** y **la práctica**. Aplicar de cada principio lo que el cambio pida, dentro del alcance del usuario y de las instrucciones del repo: un cambio de comportamiento pide una corrida, y un typo pide revisar el documento.

## Rama propia

Todo cambio vive en una **rama de trabajo**. Antes de la primera edición, mirar la rama actual; si es la principal (`main`, `master` o la rama por defecto del remoto), crear una rama de trabajo y seguir ahí. El único push es el de la rama de trabajo, y los cambios llegan a la principal por pull request. Esta regla vale para todo cambio, por chico que sea.

## Primero, que funcione

### Pereza

- Cada decisión vive en un solo lugar.
- Entregar la edición más chica que resuelve el problema.

### Bases

- Definir bien la forma de los datos antes de escribir la lógica.
- Hacer primero lo que ayuda a todas las fases siguientes.
- Si un escritor concurrente importaría, no compartir estado.

### TDD

Test en rojo antes del código. Invocar `code:test-review` al planear los tests y al terminarlos.

### Rediseñar desde cero

Ante un requisito nuevo, pensar qué se habría construido si hubiera estado desde el principio, y entregar ese diseño por partes.

### Atacar la premisa

Cuando dos arreglos que comparten una premisa fallan en el mismo control, escribir la premisa en una oración, contar qué actores cargan el desbalance y quitar esa asignación. Recién después probar otro arreglo.

### Restar antes de sumar

Sacar complejidad antes de agregar algo.

### Resultado verificable

- Apuntar a un estado final que se pueda comprobar.
- Una rotura intermedia vale si está planeada y se puede deshacer.

### Construir la palanca

Si el trabajo no es obvio a simple vista, hacer una unidad a mano y después construir la herramienta que la reproduce.

### Arquitectura

- **Modelar el dominio**: una estructura que haga imposibles los estados ilegales, y un glosario de términos. Si el código ya es claro y local, dejarlo como está.
- **Límites**: validar los datos donde entran y confiar en ellos adentro. La lógica de negocio va en funciones puras.
- **Tipos**: hacer imposible escribir el valor ilegal. Parsear los datos externos una sola vez, donde entran. Resolver lo que marca el compilador en vez de silenciarlo.
- **Idempotencia**: correr dos veces, o volver a correr tras un corte a la mitad, termina en el mismo estado.
- **Separar antes de serializar**: si dos partes no necesitan el mismo estado mutable, cada una tiene el suyo. Si lo necesitan, la estructura impone un solo escritor.

## Después, que esté bien

### Causa raíz

En un bug, reproducir el comportamiento reportado antes de arreglarlo, arreglar la causa (una guarda que solo esconde el error no es un arreglo) y repetir los mismos pasos después del cambio. Si la reproducción está bloqueada, reportar qué acceso, entrada o entorno falta y qué queda en duda.

### Unidades verificables

Terminar una unidad chica y comprobarla antes de empezar la siguiente.

### Dryer

Usar la herramienta [dryer](https://github.com/unclebob/dryer) para eliminar la duplicación con puntaje 0.8 o más. Si no está disponible, pedir aprobación antes de instalarla.

### Confiar en la evidencia

- Ejercitar la interfaz de la que depende el usuario: UI, API, CLI o el flujo en el dispositivo. Un build que pasa no prueba el comportamiento en ejecución.
- La evidencia tiene que corresponder a lo que se afirma. Una captura muestra apariencia; una interacción pide la secuencia ejercitada; el rendimiento pide mediciones, trazas o perfiles comparables.
- Revisar por separado la corrección y la calidad. Que el flujo pase no dice que la implementación sea mantenible o eficiente.

### Verificación repetible

En las features, cuando la tarea lo justifique, convertir los chequeos manuales recurrentes en procedimientos reutilizables con preparación, entradas, resultado esperado, dónde queda la evidencia y limpieza. Actualizar los afectados cuando cambia el producto.

## La práctica

### El código y la historia son memoria

Los agentes aprenden de los ejemplos que encuentran: el atajo de hoy puede ser la convención de mañana.

- Antes de implementar, leer el código cercano y las convenciones documentadas. Si no se entiende el porqué de un patrón, mirar su historia.
- Validar un patrón antes de copiarlo: que sea frecuente no vuelve correcto un workaround viejo.
- Quitar el andamiaje temporal propio. Conservar las explicaciones útiles de restricciones que no son obvias. Una observación puntual de una revisión se resuelve ahí, sin volverse comentario permanente ni regla universal.

### Convertir correcciones en restricciones

Cuando un error puede repetirse, mejorar el entorno que lo permite, con el mecanismo efectivo más chico:

| Falla | Respuesta útil |
|---|---|
| Un estado o dependencia inválidos se pueden eliminar por diseño | Restringir la arquitectura, la API o el modelo de datos. |
| Un mal patrón se detecta mecánicamente | Agregar o reusar un chequeo de tipos, lint, compilador o CI. |
| La decisión pide contexto y criterio | Escribir una regla de proyecto o un criterio de revisión, corto. |
| Al agente le falta un procedimiento repetible | Capturar el flujo en una skill y evaluar su comportamiento. |

- Preferir restricciones que se hagan cumplir solas cuando se pueda: las reglas escritas y la revisión automática también fallan.
- Comprobar que un chequeo nuevo rechaza el caso malo y deja pasar uno válido.
- Anotar el principio general y cuándo aplica, sin los nombres ni la historia del incidente. Extender las instrucciones que ya existen en vez de sumar duplicados.
- Un cambio de arquitectura que excede la tarea queda como seguimiento acotado.

### Trabajar en pareja con el humano

El trabajo se tiene que entender lo suficiente para revisarlo y mantenerlo.

- Explicar las decisiones con consecuencias usando el código relevante y el comportamiento observado, con contexto suficiente para juzgar el resultado sin reconstruir la sesión.
- Mantener separables los cambios independientes.

### Registro

Anotar cada acción y su motivo, y entregar ese registro al terminar.

### Cuidar el contexto

Mantener chico el hilo principal: mandar el volumen afuera y quedarse con el resumen.

### Limpiar worktrees

Buscar lo que se puede borrar, confirmar que nada en uso lo necesita y recién entonces liberar el disco. El trabajo sin commitear espera una decisión del usuario.

### Commits y push

- Commits chicos, frecuentes y ordenados, con el formato de mensaje del usuario y del repo.
- El commit o el pull request explica por qué cambió el comportamiento, qué cambió y cómo se probó, para que la historia sirva al investigar o revertir. Si el formato del mensaje no deja lugar, va en el pull request.
- Al terminar, push de la rama de trabajo (ver **Rama propia**).
