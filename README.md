<div align="center">

# tool-skills

*Skills para Claude Code que resuelven tareas concretas: de documentar un repo a escribir un A3.*

[![Licencia MIT](https://img.shields.io/badge/licencia-MIT-blue?style=flat-square)](LICENSE)

[Skills](#skills) • [Instalación](#instalación) • [Uso](#uso) • [Cómo funciona](#cómo-funciona)

</div>

Catorce skills en español, cada una con sus pasos y su criterio de terminado, para que Claude Code siga el mismo proceso en cada corrida. Son para quien usa Claude Code y quiere instalarlas todas o solo las que le sirvan.

## Skills

| Skill | Qué hace |
|---|---|
| `tool:a3` | **(En etapa de prueba)** Escribe un A3 al estilo Toyota: el problema, su causa, la contramedida, el plan y el seguimiento en una página, como alternativa corta a un spec. |
| `tool:test-audit` | **(En etapa de prueba)** Auditoría profunda y manual de tests con mutantes (a mano y con mutator y crapper, previa aprobación) y refactores en una copia, y señala cuáles no protegen nada, cuáles impiden refactorizar y qué reglas de negocio quedaron sin test. |
| `tool:test-review` | Revisión rápida y automática al planear y al escribir tests: asegura TDD, FIRST y cobertura de las reglas de negocio, y corrige los que no protegen nada, están atados al cómo, abusan de mocks, son complejos o tienen nombre técnico. |
| `tool:cuestioname` | **(En etapa de prueba)** Sortea una parte del sistema de tu proyecto y te toma un cuestionario HTML de 4 preguntas sobre cómo funciona y cómo está implementada; cada error se explica y se vuelve a preguntar con otros datos. |
| `tool:diagrama-hardware` | Dibuja esquemáticos y diagramas de conexionado de circuitos como SVG con schemdraw. Basada en `schemdraw-circuit-generator` de takazudo/claude-resources. |
| `tool:doc-estudio` | Escribe dos `.md` complementarios que enseñan un tema desde cero (fundamentos y avanzado), con repo de pruebas, tres tareas con tests por doc, diagramas, quiz y fuentes. |
| `tool:el-gremio` | Somete una decisión a 5 asesores que la analizan por separado, se revisan a ciegas y cierran con el veredicto de un presidente. |
| `tool:informe-cambios` | **(En revisión)** Escribe un informe de cambios para enviar a un cliente: un `.md`, un PDF general y un PDF por etapa, cada cambio con su porqué, cómo se detectó y qué cambia. |
| `tool:learn` | **(En etapa de prueba)** Genera un `.html` que te enseña desde cero una parte de tu código o un concepto (por ejemplo, transacciones): diagramas, código real de tu proyecto y de uno ficticio, ejercicios para encontrar errores y una tarea con ayudas. Lo guarda para consultarlo después. |
| `tool:policy` | **(En etapa de prueba)** Prepara los documentos legales para lanzar un repositorio: política de privacidad y de seguridad, `SECURITY.md`, términos, cookies, proveedores, procedimientos y un checklist de trámites, todo a partir de lo que el código hace de verdad. |
| `tool:readme` | Escribe o reescribe el `README.md` de un proyecto a partir de relevar todo el repo. |
| `tool:referencia` | Suma un repo o un sitio (`/tool:referencia <url>`) a la base de referencias de desarrollo que consultan `tool:roadmap`, `tool:learn` y `tool:doc-estudio`. |
| `tool:review-comments` | Revisa los comentarios del código y señala cuáles sobran, cuáles mienten y dónde falta uno. |
| `tool:roadmap` | Investiga temas en distintas fuentes y escribe un roadmap de estudio aplicado a tu proyecto, o un vistazo general del área si no tienes uno, con el enlace de cada fuente. |
| `tool:use-cases` | Genera el documento de casos de uso de un proyecto (actores, historias de usuario y reglas de negocio) para alguien no técnico. |

## Instalación

Requiere [Claude Code](https://docs.anthropic.com/en/docs/claude-code) y Linux o macOS: los nombres de las carpetas llevan `:`, que Windows no admite.

```bash
git clone https://github.com/CiroMirkin/tool-skills.git
cd tool-skills
mkdir -p ~/.claude/skills
ln -s "$PWD"/tool:* ~/.claude/skills/
```

Los enlaces hacen que un `git pull` actualice las skills. Para instalar solo una, enlaza únicamente su carpeta. Las skills nuevas aparecen al abrir una sesión nueva.

Algunas skills necesitan algo más:

- **`tool:diagrama-hardware`**: Python 3 con `schemdraw` y `matplotlib`. Con [uv](https://docs.astral.sh/uv/) alcanza con `uv run --no-project --with schemdraw --with matplotlib python script.py`. Para simular el circuito usa `ngspice` (`sudo apt install ngspice`); si falta, la skill pregunta antes de instalarlo.
- **`tool:doc-estudio`**: Python 3 y `curl`, las skills `diagram-design` y `humanizer`, y las herramientas para compilar y correr el código del tema, como `arduino-cli` en firmware.
- **`tool:learn`**: Python 3, [uv](https://docs.astral.sh/uv/) (instala `pygments` al correr) y internet para investigar. Usa las skills `diagram-design` y `humanizer`, y las herramientas para ejecutar el código del tema. Las lecciones se guardan en `tool:learn/memoria/`, que git ignora.
- **`tool:informe-cambios`**: Node.js con `npm` (instala sus dependencias la primera vez), Python 3 e internet para bajar las fuentes. Usa la skill `humanizer` y `pdftoppm` para revisar los PDF.
- **`tool:referencias-base`**: no es una skill, es la carpeta con `referencias.md` que leen `tool:roadmap`, `tool:learn`, `tool:doc-estudio` y `tool:referencia`. Si instalas esas por separado, enlaza también esta carpeta.

## Uso

Escribe el nombre de la skill en Claude Code, o pide la tarea con tus palabras y Claude la activa solo:

```text
/tool:readme
/tool:roadmap armá un roadmap de estudio sobre este tema
/tool:informe-cambios arma el informe para el cliente
```

## Cómo funciona

![Diagrama de contexto](docs/images/contexto.svg)

Claude Code carga las skills desde `~/.claude/skills` y ejecuta la que corresponde a tu pedido. Según la skill, investiga en la web, instala dependencias, y lee o escribe archivos de tu máquina.
