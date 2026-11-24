# Vistazo general

El **vistazo** es el roadmap sin caso: orienta sobre un área (qué partes tiene, en qué orden se estudian, qué herramientas y debates hay), pero no puede decir qué parte necesita un proyecto. Es la versión floja, y el documento lo declara.

Los pasos y el formato de [`SKILL.md`](SKILL.md) valen igual, con estos cambios. Donde dicen "el caso", leer "el área".

## Cambios por paso

**Paso 1. Leer el pedido.** Anotar como supuesto el rol desde el que se mira el área (un design system se estudia distinto desde desarrollo que desde diseño). Hecho cuando están anotados los temas, el rol y las fuentes del usuario.

**Paso 2. Dimensionar.** Se saltea, y el documento va sin Fase 0: sin números no hay cuenta. El criterio de clasificación pasa a ser el del paso 5.

**Paso 3. Mapear la cobertura.** El mapa está completo cuando cubre:

- **los conceptos núcleo** del área, contrastados con `developer-roadmap` si tiene un roadmap de ella;
- **las herramientas dominantes**, cada una en su subsección, con el contexto que favorece a cada una en lugar de una elegida;
- **las corrientes o alternativas en debate**, cada una con su subsección.

"Dónde se despliega" entra solo si el área trata de eso.

**Paso 5. Clasificar.**

- **[ESTUDIAR]**: aparece en casi cualquier proyecto del área.
- **[CONOCER]**: aparece solo en cierto tipo de proyecto. Su escenario dice cuál.

Las marcas (\*) quedan fuera: no hay equipo que adopte nada.

**Paso 6. Escribir.** El escenario es una situación típica del área: nombra el tipo de proyecto donde aparece el concepto y usa números de ejemplo verosímiles, distintos según el concepto. El problema sigue diciendo qué se rompe. El proyecto práctico se plantea sobre un ejemplo mínimo.

**Paso 8. Entregar.** En lugar de la conclusión del dimensionamiento y las preguntas para el equipo, informar qué datos de un caso cambiarían más el roadmap y ofrecer rehacerlo con uno.

## Cambios en el formato

Reemplazar el título y el principio del documento por este:

```markdown
# Roadmap: <temas> (vistazo general)

Vistazo general de <área>, visto desde <rol>. No se basa en un proyecto: muestra el mapa del área, pero no qué parte necesita un proyecto concreto. Para estudiar en serio, conviene rehacerlo con un caso.

## Cómo leer este documento

**[ESTUDIAR]**: aparece en casi cualquier proyecto del área. Es lo primero para entenderla.

**[CONOCER]**: aparece solo en cierto tipo de proyecto. Entendé qué es y qué problema resuelve, y profundizá cuando te toque uno de esos proyectos.

Cada concepto tiene un bloque Escenario / Problema: una situación típica del área, con números de ejemplo, y lo que sale mal si no aplicás ese concepto.

<Orden sugerido: qué fases son el núcleo y cuáles se pueden intercalar.>
```

Y agregar esta sección antes de `## Fuentes principales`:

```markdown
## Qué cambiaría con un caso

**<Dato del caso>**: <qué conceptos subiría o bajaría de prioridad>.
```
