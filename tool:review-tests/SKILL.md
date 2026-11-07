---
name: tool:review-tests
description: Audita tests y señala cuáles no protegen nada, cuáles son frágiles, cuáles no notarían una regresión y qué comportamiento quedó sin test. Usar cuando el usuario pida revisar, limpiar o podar tests, pregunte si detectan bugs o cuáles faltan, o quiera revisar un lote de tests escritos por una IA.
---

# Revisar tests

> **En etapa de prueba.** El reporte lo aclara en su primera línea, para que sus hallazgos se revisen con más cuidado.

Un test se gana su lugar cuando existe un **cambio plausible y dañino** que lo pone **rojo**. Pasar en verde no prueba nada: solo dice que hoy el código hace lo que el test mira. La vara para cada test es esta: ¿un ingeniero independiente, construyendo esto para sí mismo, escribiría este test porque protege algo que le importa?

Los tests priorizan las **reglas de negocio**. El valor se mide por lo que costaría que se rompa (plata, permisos, datos, lo que usuarios y otros sistemas usan). Un porcentaje de cobertura nunca es argumento para quedarse con un test ni para pedir uno.

Los tests dejan **refactorizar**: mientras el sistema se siga comportando bien, cambiar el diseño del código los deja en verde. Un test bueno pasa las dos pruebas, se pone rojo cuando el comportamiento se rompe y sigue verde cuando solo cambia el diseño.

## Alcance

Lo que el usuario nombre (carpeta, módulo, archivos, rama, PR). Si no nombra nada, los tests del diff sin commitear; si está limpio, los del último commit; si ahí tampoco hay tests, preguntar.

## Pasos

1. **Correr la suite** en una copia del proyecto en el scratchpad, con sus dependencias instaladas de forma normal, para que el árbol del usuario no se toque; todos los pasos que corren algo usan esa copia. Un rojo acá se diagnostica antes de seguir: si es del entorno se arregla o se anota lo que queda afuera. Corridas: normal (anotando los tests más lentos), en orden aleatorio (`vitest --sequence.shuffle`, `pytest --random-order`), cada archivo por separado, en paralelo forzado con más workers que núcleos (`--maxWorkers=4`, `pytest -n 4`, porque el valor por defecto depende de la máquina y puede esconder el choque), y con el reloj de todo el proceso adelantado dos y tres años. Lo que cambia de resultado entre corridas va a *No cumple FIRST*, citando la corrida. Hecho cuando hay línea base en verde y las cinco corridas tienen resultado, o quedó anotado por qué no se pudo correr (entonces los mutantes se razonan leyendo y el reporte lo dice).
2. **Ubicar las reglas de negocio** del alcance en casos de uso, `GLOSSARY.md`, ADRs y specs. Si no están definidas, armar un cuestionario con las skills `matt:grilling` y `matt:domain-modeling` (el equivalente a `matt:grill-with-docs`, que solo se dispara a mano) y responderlo con el usuario antes de seguir. El código muestra lo que el sistema hace, y la regla la confirma el usuario. Hecho cuando hay una lista de reglas, cada una con su fuente o la respuesta del usuario.
3. **Leer cada test junto al código que protege** y clasificarlo con las categorías de abajo; un test puede caer en más de una. Para cada candidato a *Inútil*, buscar también el mejor motivo para quedárselo (`git log` del test: ¿es regresión de un incidente?) y decirlo si existe. Hecho cuando cada test del alcance tiene categoría.
4. **Mutar** primero el código que aplica las reglas de negocio: un cambio chico, plausible y equivocado (invertir una comparación, correr un borde, cambiar una rama, quitar un chequeo de null), y correr la suite. En los tests con mocks, además, borrar el código de producción, total o parcialmente: el test tiene que fallar. Si hay herramienta de mutación configurada, correrla sobre el alcance; si no, nombrar una vez en el reporte la que encaja con el stack (Stryker en JS/TS, mutmut en Python, PITest en JVM, cargo-mutants en Rust, Infection en PHP) sin instalarla. Si el mutante se corre con un script, primero va un control sin mutar en verde, y una salida ilegible es un error y no una muerte. Un **muerto** cita el test que lo mató. Un **vivo** se clasifica: **equivalente** si ninguna entrada real muestra la diferencia, y se descarta; *Mentiroso* si hay un test que promete eso; *Hueco* si ninguno lo mira. Si un nivel de la suite no se corrió, el vivo lo dice. Hecho cuando cada módulo de valor tiene al menos un mutante probado y cada uno tiene resultado.
5. **Refactorizar** en la misma copia el código de esos módulos sin cambiar su comportamiento (extraer una función, renombrar algo interno, partir un módulo, reordenar llamadas internas, llamar a una dependencia de otra forma con el mismo resultado), y correr sus tests. Cada test que se pone rojo es **Frágil**, con ese refactor como evidencia. Hecho cuando cada módulo de valor tiene al menos un refactor probado.
6. **Mirar la forma**: contar tests por nivel (unit, integración, e2e) y buscar lo que solo se detecta en el nivel caro. Hecho cuando hay conteo por nivel y, si la forma está mal, tests concretos que podrían bajar de nivel y cómo sería el test más barato.
7. **Buscar los huecos**: primero cada regla de la lista contra la suite, y después ramas, errores, bordes y validaciones del código. Priorizar por costo: caminos de error, bordes, bugs ya arreglados sin test de regresión (`git log --grep=fix`), y concurrencia o fallos parciales. Hecho cuando cada comportamiento que importa tiene test o propuesta de test.
8. **Buscar el workflow automático**: si algo corre los tests sin que nadie lo pida (`.github/workflows`, `.gitlab-ci.yml`, hook de pre-push). Si no existe, o deja afuera un nivel de la suite, proponer uno usando los comandos reales del proyecto. Hecho cuando quedó citado el que existe y qué niveles corre, o el reporte trae la propuesta con el archivo completo, que se crea recién con aprobación.
9. **Reportar**, agrupado por categoría. Cada hallazgo lleva un id correlativo en todo el reporte (T1, T2…, sin reiniciar por categoría) para que el usuario los apruebe por id, el `archivo:línea` del test, el `archivo:línea` del código que protege o debería proteger, y una oración que se entienda sin haber leído esta skill. Al final, los mutantes probados y la forma. Sin cita no hay hallazgo.

Aplicar cambios recién cuando el usuario los apruebe. Al borrar un duplicado, comprobar antes que el test que queda cubre todo lo del borrado.

## Categorías

- **Se queda**: hay un cambio dañino concreto que lo pone rojo. No va al reporte salvo en el conteo.
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
  - *Verde sin el código*: sigue en verde con el código de producción borrado (paso 4). No prueba nada, y el test también tiene que garantizar que el código funciona.
- **Test complejo** → simplificar: el cuerpo de un test es lineal y explícito, porque un test no tiene tests que lo protejan y cada rama suya es un lugar más donde equivocarse. Muchas líneas y detalles no son un problema. La simplificación se hace manteniendo el verde todo el tiempo.
  - *Condicional*: un `if` o ternario dentro del test. Casi nunca se justifica, y suele esconder dos casos que van en dos tests.
  - *Bucle*: recorre una lista corta en vez de acceder directo a sus índices con más sentencias.
  - *Indirección prematura*: un método de apoyo con lógica propia, o que esconde lo que se está probando. Los métodos de apoyo se extraen en la fase de refactor, con los tests ya escritos y en verde.
  - *Helper con lógica*: un método de apoyo solo lleva condicionales o bucles cuando lee o escribe algo que no se puede tocar de otra forma (recorrer una hoja de Excel) y no hay manera de evitarlo. Como esa lógica también puede fallar, lleva su propio test. Si no cumple las dos cosas, es hallazgo.
- **Mentiroso** → fortalecer: parece proteger algo y no lo nota si se rompe. Solo con evidencia: un mutante **vivo** sobre lo que el test promete, o un assert más débil que lo que promete el nombre (`rechaza_email_invalido` que solo mira `status != 200`, y un 500 también pasa).
- **No cumple FIRST** → corregir: cada test es *Fast*, *Independent*, *Repeatable*, *Self-validated* y *Timely*.
  - *Lento*: tarda mucho más que sus vecinos sin que lo justifique lo que protege.
  - *Dependiente*: su resultado depende de que otro test corra antes o de lo que deja (estado global, archivo o base de datos compartidos). Cada test prepara lo suyo y corre solo.
  - *No repetible*: depende del reloj real, la red, la zona horaria o el azar, así que hoy pasa y mañana no. Fijar esa entrada.
  - *Sin autovalidar*: hay que mirar un log o una salida para saber si pasó. Termina en un assert que decide solo.
  - *Tardío*: el mejor momento para escribir un test es antes que el código, porque así se lo ve rojo. Hay evidencia cuando `git log` muestra el test en un commit posterior al código, o un fix sin su test de regresión. Si entraron en el mismo commit no se puede saber y no es hallazgo.
- **Nombre técnico** → renombrar: el nombre de un test es una afirmación clara, en lenguaje de negocio, sobre el comportamiento del sistema. Los nombres juntos se leen como el manual de instrucciones: alguien entiende qué hace el sistema solo con leerlos, y los detalles concretos se ven dentro del test. Proponer el nombre nuevo cuando el actual:
  - Repite el dato de entrada o de salida, que ya se lee en el cuerpo: `Returns 4 when the input is 2`, `Empty String`, `Returns null`.
  - Nombra un detalle de implementación que puede cambiar: `Throws exception if empty` pasa a `Does not allow for blanks`, que sigue valiendo si mañana deja de ser una excepción.
  - Habla de funciones, claves o mecanismos: `getAll construye objeto con claves explícitas`.

  Nombres que cumplen: `Removes duplicated items from the collection`, `Counts characters in the document`, `Registers a failure in the communication`, `Calculates the net pay`, `Finds patients by surname`, `Is case insensitive`, `Requires at least one number`.
- **Hueco** → agregar: salió del paso 7. Nombre en lenguaje de negocio, entrada, resultado esperado y junto a qué test va. Tiene que pasar la misma vara que los demás, y se escribe antes que el arreglo para verlo rojo.
