# Instrumentos de test-audit: mutator y crapper

Referencia del paso 4 (mutación) y del paso 7 (huecos). Fuentes: `github.com/unclebob/mutator` y `github.com/unclebob/crapper`, licencia 0BSD, repos jóvenes. Soportan Clojure, Java, Go, TypeScript/JavaScript, Rust y Python.

## Aprobación única

Un solo pedido al usuario, con las dos herramientas juntas, antes de clonar o instalar nada. El pedido lista:

- **Clones**: `unclebob/crapper` y `unclebob/mutator`, uno al lado del otro (`mutator` exige `../crapper`), en `<scratchpad>/herramientas/`.
- **`.venv`**: lo crea la primera corrida de cada herramienta. Anotar en el reporte dónde quedó.
- **En la copia del proyecto**: `coverage` y `pytest` en el Python del proyecto, `@vitest/coverage-v8` en `node_modules` (sin editar `package.json`), y las carpetas `.metrics/` y `target/mutation-workers/`.
- **Fuera de la copia, en la máquina del usuario**: `cargo-llvm-cov` en `~/.cargo/bin` (Rust, si no hay `cargo-llvm-cov` ni `tarpaulin`) y el plugin JaCoCo 0.8.12 en `~/.m2` (Java). Decir cuáles aplican al stack del alcance.

Hecho cuando el usuario respondió. Sin aprobación: mutantes a mano, y el reporte lo dice y nombra una vez la herramienta que encaja.

## Cómo correr

Desde la raíz de la copia. El README las muestra como `./crapper` y `./mutator` dentro de su carpeta: la primera vez, comprobar cómo se invocan desde la raíz de la copia.

- **crapper**: `crapper` imprime la tabla, peor CRAP primero, y escribe `.metrics/crap.edn`. Variantes: `--use-existing-coverage`, `--changed`, rutas o fragmentos de ruta como argumento.
- **mutator**: `mutator --scan <ruta>` lista los sitios sin correr tests. `mutator <archivo o carpeta>` los corre. Variantes: `--changed`, `--use-existing-coverage`, `--no-coverage`, `--test-command "<comando>"`, `--max-workers N`.
- **Orden**: crapper primero (también genera la cobertura que mutator usa), después mutator sobre los archivos de los módulos de valor, en orden de CRAP. La primera corrida de un árbol ejecuta todos los mutantes cubiertos: empezar por un archivo y, si va a tardar, correrla en segundo plano.
- **Salida de mutator**: `0` todos muertos, `2` la línea base falla (es un error, no una muerte: se diagnostica como el rojo del paso 1), `3` sobrevivió algún mutante.

## Leer los resultados

`mutator` escribe `.metrics/mutate/<namespace>.edn`: por función, `:killed`, `:survived`, `:uncovered` y `:sites`.

- **Vivo** (`:survived`): se clasifica como en el paso 4 (equivalente, *Mentiroso* o *Hueco*).
- **Sin cobertura** (`:uncovered`): ningún test ejecuta esa línea, así que mutator no la corre. Va como candidato a *Hueco*, con el sitio y la función.
- **Muerto** (`:killed`): mutator no informa qué test lo mató. Para los muertos que sostienen un hallazgo (un *Duplicado*, un test dudoso), repetir el mutante a mano con `--test-command` acotado al archivo de ese test.
- **Alcance de los mutantes**: operadores aritméticos y de comparación, `true`/`false`, `&&`/`||` y sus equivalentes por lenguaje. No quita chequeos ni borra código de producción, así que esos mutantes del paso 4 siguen a mano.

## Leer CRAP

`CRAP = CC² × (1 − cobertura)³ + CC`. De 1 a 5 es riesgo bajo, de 5 a 30 vale mirarlo, más de 30 es complejo y poco probado. Sirve para ordenar dónde mirar primero. Si el reporte muestra 0% de cobertura en todo un lenguaje, es probable que la cobertura no haya corrido (crapper puntúa en 0% el lenguaje cuando falta la herramienta o falla la corrida) y no que falten tests: verificar antes de usar el orden.

## Fuera de los seis stacks

Nombrar una vez, sin instalar: PITest (JVM sin Maven), Infection (PHP), Stryker (JS/TS), mutmut (Python), cargo-mutants (Rust).
