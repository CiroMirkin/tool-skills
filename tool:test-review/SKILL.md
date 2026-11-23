---
name: tool:test-review
description: Revisa tests al planearlos, antes de escribirlos, y al terminar de escribir o editar cualquier test. Asegura TDD (rojo primero), FIRST, que cubran las reglas de negocio y corrige los que no protegen nada, están atados al cómo, abusan de mocks o tienen nombre técnico.
---

# Revisar tests (fast)

Un test se gana su lugar cuando existe un **cambio plausible y dañino** que lo pone **rojo**. Pasar en verde no prueba nada: solo dice que hoy el código hace lo que el test mira. La vara: ¿un ingeniero independiente, construyendo esto para sí mismo, escribiría este test porque protege algo que le importa? El valor se mide por lo que costaría que se rompa (plata, permisos, datos, lo que usuarios y otros sistemas usan). Un porcentaje de cobertura nunca es argumento.

Un test **honesto** ejercita el comportamiento observable y se pone rojo si la función no hiciera nada. El **deshonesto** pasa sin verificar nada real (asserts triviales, mocks que nunca fallan, atado a la implementación interna), aunque infle la cobertura. Si un test honesto es impracticable, no se escribe uno deshonesto en su lugar: la regla queda sin test y se dice en el reporte.

Los tests dejan **refactorizar**: mientras el sistema se siga comportando bien, cambiar el diseño del código los deja en verde. Un test bueno se pone rojo cuando el comportamiento se rompe y sigue verde cuando solo cambia el diseño.

Esta revisión es *fast*: corre solo los tests del diff (los agregados o tocados, sin sus vecinos ni la suite completa), con mutantes a mano y sin herramienta de mutación, y no busca huecos fuera de las reglas del alcance. Eso es `tool:test-audit`.

## Pasos

Dos momentos, mismas categorías: **al planear** (antes de escribir el test, para que nazca bien) y **al terminar** (para revisar lo escrito). Si el test ya existe, se salta al paso 4. El **alcance** son los tests del diff sin commitear; si está limpio, los del último commit. Todo lo que se corre es solo eso.

1. **Reglas de negocio** del alcance, buscadas en casos de uso, `GLOSSARY.md`, ADRs y specs. Si la regla no está escrita, una sola pregunta al usuario: el código muestra lo que el sistema hace, y la regla la confirma él. Hecho cuando hay lista de reglas, cada una con su fuente o la respuesta del usuario.
2. **Planear cada test** antes de escribirlo, en una línea: la regla que protege, su nombre en lenguaje de negocio, el cambio dañino que lo pone rojo, y qué lo vuelve *Independiente* y *Repetible* (fijar reloj, red, azar; preparar lo suyo). Hecho cuando cada regla del alcance tiene su test honesto planeado, o queda dicho por qué es impracticable.
3. **Rojo primero** (*Timely*): escribir el test y correrlo antes del código, comprobando que falla por la razón correcta, no por un error de sintaxis o de import. Después, el cambio más pequeño que lo pone en verde. Hecho cuando cada test nuevo se vio rojo y después verde con ese cambio mínimo.
4. **Clasificar cada test** del alcance con las categorías de abajo, leyéndolo junto al código que protege; un test puede caer en más de una. Para cada candidato a *Inútil*, buscar el mejor motivo para quedárselo (¿es regresión de un incidente?). Hecho cuando cada test tiene categoría.
5. **Mutar**: por test, un cambio chico, plausible y dañino en el código que protege (invertir una comparación, correr un borde, quitar un chequeo de null), aplicado de verdad y corriendo solo los tests del diff. Antes de mutar, guardar una copia del archivo en el scratchpad y restaurarla apenas termina cada mutante, para no pisar cambios sin commitear. Un test que no se pone rojo es *Inútil* o hay que fortalecerlo. En tests con mocks, además, borrar el código de producción, total o parcialmente: el test tiene que fallar. Hecho cuando cada test mató al menos un mutante o quedó clasificado, y los archivos quedaron restaurados.
6. **Cubrir las reglas**: cada regla de la lista del paso 1 tiene al menos un test que se pondría rojo si se rompe. Una regla sin test se agrega ahora, con el mismo plan y rojo primero. Hecho cuando cada regla del alcance apunta a un `archivo:línea` de test.
7. **Corregir** los hallazgos de los tests de este turno y correr esos tests hasta verde. Los tests anteriores al turno se listan sin tocar. Hecho cuando no queda hallazgo propio sin corregir y los tests tocados están en verde.
8. **Reportar** en pocas líneas: reglas cubiertas (regla → `archivo:línea`), qué se corrigió, o "sin hallazgos". Si apareció algo que pide profundidad (herramienta de mutación sobre todo el módulo, huecos de ramas y errores, orden de ejecución), mencionar `tool:test-audit` una vez.

## Categorías

- **Inútil** → borrar: no puede fallar de forma útil.
  - *Tautología*: no hay cambio del código que lo ponga rojo (`expect(fn).toBeDefined()` como único assert).
  - *Copia la fórmula*: el valor esperado se calcula con la misma lógica que el código, así que un bug cae en los dos lados.
  - *Duplicado*: falla exactamente con los mismos bugs que otro. Citar el que se queda.
  - *Prueba ajena*: comprueba el lenguaje, el framework o una librería.
  - *Anémico*: getter, setter o constructor que solo asigna. Si calcula, valida o deriva, ya tiene lógica y se queda.
  - *Forma sin consumidor*: comprueba claves, parámetros o cantidad de campos porque un plan lo pidió. Si la forma es el contrato (API pública, formato de archivo, migración) y algo de afuera se rompería al cambiarla, se queda.
- **Frágil** → reescribir: protege algo real pero está atado al *cómo*, entonces impide refactorizar. Decir a qué está atado y qué comportamiento comprobar en su lugar.
  - *Mock sobreespecificado*: exige secuencia, cantidad o argumentos de llamadas internas en vez del resultado.
  - *Snapshot ruidoso*: casi todo el diff es ruido y lo que importa queda enterrado.
  - *Interno*: entra por métodos o estado privados en vez de la interfaz pública.
  - *Texto exacto*: compara un log o mensaje que nadie parsea. Si es contrato documentado, el texto exacto es correcto.
- **Uso incorrecto de mocks** → reescribir: el test crea los mocks, los inyecta en el código bajo prueba y al final les consulta si todo fue como se esperaba. Quien los ejecuta es el código de producción.
  - *Invocado por el test*: el test llama directamente a una función del mock.
  - *Mock contra sí mismo*: configura el mock para devolver X y comprueba que salió X, sin que el código haga nada con X.
  - *Verde sin el código*: seguiría en verde con el código de producción borrado. No prueba nada, y el test también tiene que garantizar que el código funciona.
- **Test complejo** → simplificar: el cuerpo de un test es lineal y explícito, porque un test no tiene tests que lo protejan y cada rama suya es un lugar más donde equivocarse. Muchas líneas y detalles no son un problema. La simplificación se hace manteniendo el verde todo el tiempo.
  - *Condicional*: un `if` o ternario dentro del test. Casi nunca se justifica, y suele esconder dos casos que van en dos tests.
  - *Bucle*: recorre una lista corta en vez de acceder directo a sus índices con más sentencias.
  - *Indirección prematura*: un método de apoyo con lógica propia, o que esconde lo que se está probando. Los métodos de apoyo se extraen en la fase de refactor, con los tests ya escritos y en verde.
  - *Helper con lógica*: un método de apoyo solo lleva condicionales o bucles cuando lee o escribe algo que no se puede tocar de otra forma (recorrer una hoja de Excel) y no hay manera de evitarlo. Como esa lógica también puede fallar, lleva su propio test. Si no cumple las dos cosas, es hallazgo.
- **No cumple FIRST** → corregir: cada test es *Fast*, *Independent*, *Repeatable*, *Self-validated* y *Timely*.
  - *Lento*: tarda mucho más que sus vecinos sin que lo justifique lo que protege (se mide en `tool:test-audit`).
  - *Dependiente*: su resultado depende de que otro test corra antes o de lo que deja (estado global, archivo o base de datos compartidos). Cada test prepara lo suyo y corre solo.
  - *No repetible*: depende del reloj real, la red, la zona horaria o el azar, así que hoy pasa y mañana no. Fijar esa entrada.
  - *Sin autovalidar*: hay que mirar un log o una salida para saber si pasó. Termina en un assert que decide solo.
  - *Tardío*: el mejor momento para escribir un test es antes que el código, porque así se lo ve rojo. Hay evidencia cuando `git log` muestra el test en un commit posterior al código, o un fix sin su test de regresión. Si entraron en el mismo commit no se puede saber y no es hallazgo.
- **Nombre técnico** → renombrar: el nombre de un test es una afirmación clara, en lenguaje de negocio, sobre el comportamiento del sistema. Los nombres juntos se leen como el manual de instrucciones: alguien entiende qué hace el sistema solo con leerlos, y los detalles concretos se ven dentro del test. Proponer el nombre nuevo cuando el actual:
  - Repite el dato de entrada o de salida, que ya se lee en el cuerpo: `Returns 4 when the input is 2`, `Empty String`, `Returns null`.
  - Nombra un detalle de implementación que puede cambiar: `Throws exception if empty` pasa a `Does not allow for blanks`, que sigue valiendo si mañana deja de ser una excepción.
  - Habla de funciones, claves o mecanismos: `getAll construye objeto con claves explícitas`.

  Nombres que cumplen: `Removes duplicated items from the collection`, `Counts characters in the document`, `Registers a failure in the communication`, `Calculates the net pay`, `Finds patients by surname`, `Is case insensitive`, `Requires at least one number`.
