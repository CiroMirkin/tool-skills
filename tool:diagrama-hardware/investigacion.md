# Cómo validar los circuitos de `tool:diagrama-hardware`

Notas de investigación (noviembre 2026). Cada afirmación lleva su fuente entre corchetes; la lista completa está al final. Si algo solo aparece en fuentes secundarias, lo marco **[secundaria]**. Lo que probé yo en la máquina va con **[EXP]**, con el comando y el resultado.

## 0. Qué valida hoy la skill

- El flujo es: (A) lista de conexiones escrita a mano, que "serves as the specification"; (B–D) construcción incremental en schemdraw; (E) verificación final mirando el screenshot; (F) entrega [SKILL].
- Toda la verificación es **visual**: una checklist (líneas trazables, puntos de unión, etiquetas que no tapen símbolos, líneas que no toquen el borde de un IC) que primero revisa el agente sobre un PNG y después aprueba el usuario. La definición de "completo" es que el código corra, que se genere el SVG y que el usuario apruebe [SKILL].
- La captura depende de una skill externa (`headless-browser`); si no está, el paso se saltea con un aviso [SKILL].
- No hay ningún chequeo que compare el dibujo contra la lista de conexiones, ni ninguno que diga si el circuito funciona (polaridad, nodos flotantes, valores). La propia skill advierte que "technically connected" no equivale a "visually connected", pero solo cubre el segundo caso [SKILL].

Hay dos preguntas distintas y conviene no mezclarlas:

1. **¿El dibujo es la lista de conexiones?** (validación estructural: cada pin está donde dice la lista, no quedan cables colgando, la polaridad coincide).
2. **¿La lista de conexiones es un circuito que anda?** (validación eléctrica: ERC, punto de operación, valores razonables).

## 1. schemdraw: qué expone para chequear conectividad

- **No tiene netlist.** Ni la documentación ni el código de la 0.23 tienen un concepto de nodo o net; un `grep` de `netlist`/`connect` en el paquete solo encuentra el flowchart `Connect`, el símbolo `NoConnect` y conectores del módulo pictórico [SD-SRC][EXP].
- **Sí expone posiciones absolutas de los pines.** "All elements have a set of predefined anchor positions… Once an element is added to the drawing, all its anchor positions will be added as attributes to the element object" (`Q.base` o `Q['base']`) [SD-PLACE]. En el código, cada `Element` guarda `anchors` (sin transformar) y `absanchors` (absolutas), y el `Drawing` guarda la lista `elements` y ofrece `get_segments()` [SD-SRC].
- **El mantenedor descarta la netlist en el núcleo.** En el issue #82 (exportar a LTspice), Collin Delker dice que prefiere un módulo aparte y enumera los problemas: los valores son strings, faltan modelos SPICE, muchos ejemplos "cheat" dibujando una sola línea de tierra larga donde terminan varios elementos (hace falta detectar uniones en T), los opamps tienen alimentación implícita que no se dibuja, y el backend de salida solo ve segmentos, no elementos eléctricos. Cerró el issue el 29-05-2026 "for development in other repositories" [SD-82].
- El autor del issue publicó un convertidor (schemdraw ↔ SPICE ↔ LTspice) que, según él, usa "Union-Find on anchor coordinates for node detection" [SD-82]. El repo que enlaza (`ksugahar/circuit-converter`) devolvió 404 cuando lo busqué, así que no lo pude evaluar.
- Versión actual: 0.23, publicada el 29-05-2026, licencia MIT, "Development Status 4 - Beta", un solo mantenedor [SD-PYPI].

### 1.1 Prueba: sacar las nets del dibujo por coincidencia de anchors [EXP]

Instalé schemdraw 0.23 en un venv (`uv venv` + `uv pip install schemdraw`) y escribí un prototipo de ~60 líneas (`exp/check_drawing.py` en el scratchpad). Hace lo que describe el issue #82:

1. Toma los `absanchors` de cada elemento. Para los cables (`Line`, `Wire`, `Dot`) une `start` con `end`.
2. Para cada componente toma solo los anchors que son pines: `start`/`end` en los de dos terminales, `base`/`collector`/`emitter` en BJT, `in1`/`in2`/`out` en opamp, `start` en `Ground`/`Vdd`, y `pinN` en `Ic` (el `Ic` expone cada pin dos veces, por nombre y como `pin1`, `pin2`…; además trae anchors que no son pines, como `center`, `xy`, `inL1`) [SD-SRC][EXP].
3. Une por Union-Find los puntos que coinciden (tolerancia 0,01 unidades) y los que caen en el interior de un tramo recto de cable (unión en T, el caso de la "línea de tierra larga").
4. Reporta las nets, los **pines solos** (net de un solo pin) y las **puntas de cable colgando**.

Resultados:

- Divisor LED (fuente, R, LED, retorno a tierra): bien cerrado da 3 nets y ningún pin solo. Si acorto el cable de retorno 0,3 unidades (algo que en el PNG casi no se nota), el reporte da `pines sueltos: ['D1.end']`.
- **Ejemplo 1 de `references/examples.md` (555 astable), sin tocar el código:** salen 8 nets correctas (pines 2 y 6 juntos con C y Rb; pin 7 con Ra y Rb; 4 y 8 juntos a Vdd; la línea de tierra larga junta C, C de control, LED y pin 1), sin pines solos ni cables colgando.
- Limitación que apareció: los dos símbolos `Vdd('+5V')` del 555 quedan como dos nets separadas, porque en el dibujo no están unidos por cable. Hay que fusionar las nets de los símbolos de alimentación por etiqueta.

### 1.2 Polaridad en schemdraw [EXP]

- En `SourceV` el signo "+" está cerca de `end` (x = 0,75 del cuerpo) [SD-SRC].
- En `Diode` (y en `LED`, que hereda de él) el triángulo apunta de `start` a `end`: ánodo en `start` y cátodo en `end` [SD-SRC].
- **Cuidado con `.reverse()`:** lo probé con dos diodos `.right()`, uno con `.reverse()`. En los dos casos `start` queda en x = 0 y `end` en x = 3, pero la punta del triángulo pasa de x = 1,67 a x = 1,32. O sea que `reverse()` da vuelta el símbolo y deja los anchors en su lugar, así que el nombre del anchor ya no indica la polaridad. El flag se lee de `element._userparams['reverse']`, que es un atributo privado [SD-SRC][EXP]. Un chequeo de polaridad tiene que leer ese flag.

## 2. Simulación por netlist desde Python

### 2.1 ngspice (CLI en modo batch)

- `ngspice -b archivo.cir` corre en modo batch: "ngspice will read the standard input or the specified input file and do the simulation" [NG-MAN].
- En Ubuntu 24.04 el paquete es `ngspice` 42 (`42+ds-3build1`, universe); la librería compartida viene en `libngspice0` [EXP: `apt-cache policy`].
- **[EXP]** No tenía root, así que bajé los .deb con `apt-get download ngspice libngspice0`, los extraje con `dpkg-deb -x` y corrí el binario con `SPICE_LIB_DIR` y `LD_LIBRARY_PATH` apuntando ahí. Con un `apt install` normal eso no hace falta.
  - LED con 330 Ω a 5 V (modelo `D(IS=1e-20 N=1.8 RS=5)`) y `.op`: `v(a) = 1.9715`, `i(V1) = -9.18 mA`. Un valor razonable para un LED rojo.
  - **Nodo flotante** (R2 colgada de un capacitor, sin camino DC a tierra): ngspice escribe `Warning: singular matrix: check node b`, fallan el gmin stepping y el source stepping, recurre a "Transient op", **imprime resultados y sale con código 0**.
  - **Circuito sin nodo 0:** el mismo patrón (warnings de matriz singular, resultado impreso, código 0).
  - **Dos fuentes de tensión en paralelo con valores distintos** (5 V y 3 V): `DC solution failed`, `op simulation(s) aborted` y código 1.
  - Conclusión práctica: **el código de salida no alcanza**. El validador tiene que buscar en la salida `singular matrix`, `Error`, `failed` y `aborted`, y además comparar valores contra rangos esperados.

### 2.2 PySpice

- Última versión en PyPI: 1.5, del **15-05-2021**, un mantenedor, GPLv3 [PS-PYPI]. El README de GitHub lista, bajo "On Devel HEAD" (sin release), "fixed simulation aborting due to a message from newer ngspice" [PS-GH].
- Usa la librería compartida por CFFI y la busca como `libngspice.so`, o donde diga la variable `NGSPICE_LIBRARY_PATH` [PS-SRC].
- **[EXP]** Con PySpice 1.5 y libngspice 42: primero falla porque Debian solo instala `libngspice.so.0` (el `.so` sin número viene en el paquete `-dev`); con `NGSPICE_LIBRARY_PATH=…/libngspice.so.0` carga, avisa "Unsupported Ngspice version 42" y el `.op` termina en `NgSpiceCommandError: Command 'run' failed`.
- La causa está documentada en el issue #379: PySpice trata como error cualquier línea de stderr que no empiece con "Warning:", y las versiones nuevas de ngspice escriben ahí "Using SPARSE 1.3 as Direct Linear Solver" [PS-379]. El #399 muestra lo mismo con las "Note:" del gmin stepping [PS-399].
- **InSpice** es un fork de PySpice, versión 1.7.0.7 publicada el 17-09-2026, con dos mantenedores [INS]. SKiDL lo adoptó en la 2.1.0 (30-08-2025) porque "InSpice has replaced PySpice to allow the use of newer versions of the ngspice simulator" [SK-PYPI]. No lo probé.
- Encaje con la skill: malo. Suma una dependencia frágil para algo que `subprocess` + `ngspice -b` ya resuelve.

### 2.3 spicelib (ex PyLTSpice)

- Versión 1.6.4, GPLv3. Edita netlists (`SpiceEditor`), corre simuladores en batch (`SimRunner`) y lee `.raw` (`RawRead`) de LTspice, ngspice, QSPICE y Xyce [SL-PYPI].
- "The `NGspiceSimulator` class works with Ngspice CLI, it cannot (yet) work with the shared library version" [SL-PYPI]. Con secciones `.control` hay que escribir el raw a mano y terminar con `quit` [SL-PYPI].
- **[EXP]** `NGspiceSimulator.create_from(<ruta a ngspice>)` + `SpiceEditor` + `add_instruction('.op')` + `SimRunner.run_now()`, y después `RawRead(raw, dialect='ngspice')`, dio `{'v(vcc)': 5.0, 'v(a)': 1.9715, 'i(v1)': -0.00918}`, igual que el CLI.
- Encaje: opcional. Sirve si se quieren leer formas de onda de un `.tran` sin parsear texto. Para un `.op` con `print` alcanza el CLI.

### 2.4 Lcapy (análisis simbólico, también dibuja)

- Versión 1.26 del 28-09-2025, LGPLv2+, un mantenedor [LC-PYPI]. Es "symbolic linear circuit analysis" sobre SymPy, y su lista de limitaciones arranca con "Non-linear components cannot be modelled (apart from a linearisation around a bias point)" [LC-PYPI]. En el código, los componentes no lineales lanzan `NotImplementedError('Cannot analyse non-linear component')` [LC-SRC].
- Dibuja esquemáticos desde la misma netlist, pero con **circuitikz/LaTeX** y con pistas de orientación en cada línea (`R 1 2; right`) [LC-SCH]. Necesita `pdflatex` y el paquete circuitikz; en esta máquina no están, así que no lo probé.
- Trae un grafo del circuito con `is_connected`, `networks()` y `unreachable_nodes()` (networkx) [LC-SRC].
- **[EXP]**
  - Divisor: `c[2].V.dc` da `R2*Vs/(R1 + R2)`, y con valores da `5/2`.
  - Inversor con fuente controlada (A = 1e6), Ri = 1 k y Rf = 10 k: ganancia `-9.99989`.
  - Nodo flotante (el mismo caso de 2.1): devolvió `5` **sin ningún aviso**.
- Encaje: bueno para chequear una fórmula (ganancia, frecuencia de corte) en circuitos lineales, malo como única fuente del diagrama. Cambiaría schemdraw por LaTeX, no maneja diodos ni transistores en el análisis y no avisa sobre los nodos flotantes.

### 2.5 SKiDL (netlist en Python + ERC)

- Versión 3.0.0 del 16-10-2026, MIT, 1,7k estrellas [SK-PYPI][SK-GH]. Describe el circuito en Python, corre `ERC()` y genera netlist para KiCad. En la 3.0 la generación de esquemáticos pasó al paquete aparte `schematizer` [SK-PYPI].
- Qué revisa el ERC, según el código (`skidl/erc.py`) [SK-SRC]:
  - pin sin conectar que no sea `NOCONNECT`;
  - pin `NOCONNECT` conectado;
  - net sin pines o con un solo pin;
  - conflictos entre tipos de pin (por ejemplo, dos salidas en la misma net);
  - net sin driver, o con drive insuficiente para un pin (por ejemplo, un `POWER-IN` sin `POWER-OUT`).
  - Además se pueden agregar reglas propias con `erc_assert` [SK-SRC].
- Avisa si faltan las variables `KICAD*_SYMBOL_DIR`, pero **funciona sin KiCad** si las partes se definen a mano con `tool=SKIDL` y `Pin(func=…)` [EXP].
- **[EXP]** Con una R, un LED y un "regulador" de tres pines (VIN/GND como `PWRIN`, VOUT como `PWROUT`), dejando VIN suelto a propósito:
  - `ERC WARNING: Unconnected pin: POWER-IN pin 1/VIN of REG/U1.`
  - `ERC WARNING: Insufficient drive current on net GND for pin POWER-IN pin 2/GND` (falta declarar `gnd.drive = POWER`).
  - `0 errors`: todo lo encontrado sale como *warning*, así que el validador tiene que contar los warnings.
- Para simular usa InSpice (no PySpice) [SK-PYPI][SK-SRC].
- Encaje: útil para circuitos con ICs, donde el problema típico es un pin de alimentación suelto o dos salidas peleando en la misma net. Para pasivos sueltos aporta poco más que el chequeo de pines solos de 1.1, y obliga a escribir cada parte con sus tipos de pin.

## 3. ERC: SKiDL vs KiCad

- **SKiDL `ERC()`:** puro Python, corre headless y sin KiCad si las partes se definen a mano [SK-SRC][EXP].
- **`kicad-cli sch erc`:** la documentación de KiCad 9 lo describe como "runs an electrical rule check on a schematic and generates a report", con `--severity-*`, `--format` y `--exit-code-violations`, que devuelve "0 if no violations are found, and 5 if any violations are found" [KC-CLI]. La CLI está pensada para usarse "in an automated fashion" [KC-CLI].
  - Problema de encaje: necesita un `.kicad_sch`, y esta skill no lo produce. Para tenerlo habría que pasar por SKiDL + `schematizer` (`generate_schematic`) con las librerías de símbolos de KiCad instaladas [SK-PYPI]. Es mucho armado para un diagrama de documentación.
  - No lo probé: KiCad no está instalado y Ubuntu 24.04 trae KiCad 7.0.11 [EXP: `apt-cache policy`]. No verifiqué desde qué versión existe `sch erc` ni si corre sin display (ver Dudas abiertas).

## 4. Pipelines posibles

| Pipeline | Qué atrapa | Costo | Encaje con la skill |
| --- | --- | --- | --- |
| **A. Chequeo estructural del dibujo** (nets por anchors, comparadas con la lista del Paso A) | Pines sueltos, cables cortos o colgando, pin equivocado, polaridad invertida de diodos y fuentes | ~100 líneas de Python, sin dependencias nuevas | Directo: convierte el Paso A en algo que se puede comparar con el código |
| **B. Paso A como netlist SPICE + `ngspice -b`** (`.op`/`.tran` con asserts) | Nodos flotantes, cortos entre fuentes, valores absurdos (corriente de LED, ganancia, divisor) | `apt install ngspice`; modelos para semiconductores | Bueno para analógico con valores; no sirve para lógica ni para ICs sin modelo |
| **C. SKiDL como fuente + ERC** → dibujar con schemdraw | Pines de alimentación sin driver, conflictos de salida, pines sin conectar | Hay que definir cada parte con sus tipos de pin | Para circuitos con ICs; el dibujo igual se hace a mano y hay que chequearlo con A |
| **D. Lcapy como fuente única** (análisis + dibujo) | Fórmulas simbólicas de circuitos lineales | LaTeX + circuitikz; se abandona schemdraw | Malo: cambia el motor de dibujo y deja afuera lo no lineal |
| **E. `kicad-cli sch erc`** | ERC completo de KiCad | KiCad + `.kicad_sch` (vía SKiDL/schematizer) | Malo para diagramas de documentación |

Notas:

- **A y B se complementan.** A responde "¿el dibujo es la netlist?" y B "¿la netlist anda?". Si la netlist SPICE del Paso A es la fuente de verdad, A compara el dibujo contra ese archivo y B lo simula. Así nunca se mantienen dos descripciones distintas.
- También se podría **generar la netlist desde el dibujo** (A → SPICE → ngspice). Lo probé con el LED (`exp/sd_to_spice.py`): las nets extraídas se mapean a nodos (la net que contiene `GND.start` pasa a ser `0`), se emite `V1 n2 0 DC 5 / R1 n2 n1 330 / D1 n1 0 DLED` y ngspice da los mismos 1,9715 V [EXP]. El problema es que los valores y los modelos tienen que venir de algún lado (en schemdraw son strings de etiqueta), y los opamps no tienen primitiva SPICE ni pines de alimentación dibujados, los mismos puntos que marca el mantenedor [SD-82]. Por eso conviene que la netlist sea la fuente y el dibujo se compare contra ella, no al revés.
- Para que A compare con la netlist hace falta saber qué elemento del dibujo es `R1`. schemdraw no guarda designadores; lo más simple es un dict `{id(elemento): 'R1'}` armado con las variables del script, o leer la primera línea de la etiqueta.

### 4.1 Núcleo del chequeo estructural (del prototipo [EXP])

```python
def key(p, tol=0.01): return (round(float(p[0]) / tol), round(float(p[1]) / tol))
# 1) cables: union(start, end); 2) pines de componentes: find(key(e.absanchors[a]))
# 3) unión en T: un punto colineal y dentro del tramo de un cable se une a ese cable
# 4) nets = grupos de pines; pin solo = net de un pin; cable colgando = punta con
#    una sola conexión que no toca ningún pin
# 5) fusionar nets de Vdd/Vss/Ground con la misma etiqueta
# 6) polaridad: ánodo = 'end' si e._userparams.get('reverse') else 'start'
```

## 5. Dudas abiertas / no verificado

- **`kicad-cli` headless:** la documentación dice que es para uso automatizado, pero no dice si necesita display, y no lo pude probar. Tampoco verifiqué desde qué versión existe `sch erc` (Ubuntu 24.04 trae la 7.0.11).
- **InSpice con ngspice 42:** no lo probé. Que arregle el problema de stderr de PySpice lo afirman SKiDL y el propio fork, no lo verifiqué.
- **`circuit-converter`:** el repo que se cita en el issue #82 dio 404, así que no sé cuánto cubre ni cómo trata los casos difíciles.
- **`_userparams['reverse']`** es un detalle interno de schemdraw y puede cambiar entre versiones. Conviene fijar la versión de schemdraw en la skill o tener un test que lo detecte.
- **Lcapy y el dibujo:** no lo probé (no hay LaTeX en esta máquina).
- **Tolerancia 0,01** en la coincidencia de anchors: anduvo con los ejemplos de la skill. Con `.theta()` en ángulos no ortogonales podría hacer falta más.

## Recomendación

La que mejor encaja es **A + B**, con la lista del Paso A escrita como **netlist SPICE**:

- es la única que no cambia el motor de dibujo;
- no agrega dependencias de Python (solo `ngspice` del sistema);
- convierte la "spec" que la skill ya pide en algo ejecutable.

SKiDL queda como opcional para circuitos con ICs. PySpice, Lcapy como fuente única y KiCad no conviene sumarlos.

Pasos mínimos:

1. **Paso A → `circuito.cir`.** Escribir la lista de conexiones como netlist SPICE, con los mismos designadores que las etiquetas del dibujo (`R1`, `D1`…) y nodos con nombre (`0` = GND). Los semiconductores llevan un `.model` genérico. Los ICs sin modelo van como comentario `* U1 pin VIN -> vin`, solo para el chequeo estructural.
2. **`scripts/verificar_dibujo.py`.** Partir del prototipo de 1.1 (unión por anchors + uniones en T + fusión de alimentaciones por etiqueta + polaridad con `reverse`). Recibe el `Drawing` y el dict de designadores, compara las nets contra `circuito.cir` y falla si hay pines solos, cables colgando o una net distinta.
3. **`scripts/simular.sh`.** Correr `ngspice -b circuito.cir` con `.op` (y `.tran` si aplica). Hacer fallar el paso si la salida contiene `singular matrix`, `Error`, `failed` o `aborted`. Escribir 1 a 3 asserts de sentido común sobre los valores (corriente del LED entre 5 y 20 mA, ganancia del inversor ≈ −Rf/Ri, etc.). Instalación: `sudo apt install ngspice`.
4. **SKILL.md, Paso E.** Exigir que pasen los dos scripts **antes** del screenshot. La revisión visual queda para lo que solo se ve (etiquetas, espaciado, claridad), y al entregar se reporta qué validaron los scripts.
5. **(Opcional)** Para circuitos con ICs, un `erc.py` con SKiDL y partes definidas a mano (tipos de pin `PWRIN`/`PWROUT`/`OUTPUT`), contando los `ERC WARNING`.

## Fuentes

- **[SKILL]** `tool:diagrama-hardware/SKILL.md` y `references/*.md` de este repo (leídos el 08-11-2026).
- **[SD-PLACE]** schemdraw docs, "Placing Elements" (Anchors and Positioning). https://schemdraw.readthedocs.io/en/latest/usage/placement.html
- **[SD-SRC]** Código de schemdraw 0.23 (`schemdraw.py`, `elements/elements.py`, `elements/sources.py`, `elements/twoterm.py`), instalado desde PyPI. Repo: https://github.com/cdelker/schemdraw
- **[SD-PYPI]** schemdraw en PyPI. https://pypi.org/project/schemdraw/
- **[SD-82]** cdelker/schemdraw, issue #82 "Feature Request: LTSpice ASC File Export", con los comentarios del mantenedor. https://github.com/cdelker/schemdraw/issues/82
- **[NG-MAN]** Página de manual `ngspice(1)` del paquete Ubuntu `ngspice 42+ds-3build1`.
- **[PS-PYPI]** PySpice en PyPI. https://pypi.org/project/PySpice/
- **[PS-GH]** PySpice-org/PySpice, README. https://github.com/PySpice-org/PySpice
- **[PS-SRC]** Código de PySpice 1.5, `PySpice/Spice/NgSpice/Shared.py`.
- **[PS-379]** PySpice issue #379, "Incorrectly handles stderr outputs that aren't errors from libngspice version 43". https://github.com/PySpice-org/PySpice/issues/379
- **[PS-399]** PySpice issue #399, "Ngspice .op: Non Fatal Notes and diagnosis written in stderr treated as errors". https://github.com/PySpice-org/PySpice/issues/399
- **[INS]** InSpice en PyPI. https://pypi.org/project/InSpice/
- **[SL-PYPI]** spicelib en PyPI (README de la 1.6.4). https://pypi.org/project/spicelib/
- **[LC-PYPI]** lcapy en PyPI. https://pypi.org/project/lcapy/
- **[LC-SCH]** Lcapy docs, "Schematics". https://lcapy.readthedocs.io/en/latest/schematics.html
- **[LC-SRC]** Código de lcapy 1.26 (`circuitgraph.py`, `mnacpts.py`).
- **[SK-PYPI]** skidl en PyPI (README e History hasta la 3.0.0). https://pypi.org/project/skidl/
- **[SK-GH]** devbisme/skidl, README. https://github.com/devbisme/skidl
- **[SK-SRC]** Código de skidl 3.0.0 (`erc.py`, `skidl.py`, `tools/spice/spice.py`).
- **[KC-CLI]** KiCad 9.0, "Command-Line Interface" (Schematic ERC). https://docs.kicad.org/9.0/en/cli/cli.html
- **[EXP]** Pruebas propias del 08-11-2026 en Ubuntu 24.04, Python 3.12.3, en un venv con schemdraw 0.23, PySpice 1.5, lcapy 1.26, skidl 3.0.0 y spicelib 1.6.4, más ngspice 42 extraído de los .deb de Ubuntu. Scripts en `/tmp/claude-1000/-home-ciro-Documentos-PROYECTOS-tool-skills/63bad7b8-4058-4d49-94cd-a83a0cf19eba/scratchpad/exp/` (`check_drawing.py`, `sd_nets.py`, `sd_to_spice.py`, `rev.py`, `pyspice_led.py`, `skidl_erc.py`, `lcapy_test.py`, `spicelib_test.py`, `*.cir`).
