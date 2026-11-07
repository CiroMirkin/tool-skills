---
name: tool:roadmap
description: Investiga uno o más temas en fuentes (las que pase el usuario y las que se encuentren en internet) y escribe un roadmap de estudio en .md aplicado al proyecto del usuario (o un vistazo general del área si no hay proyecto), separando qué estudiar y qué solo conocer, con escenarios concretos y el enlace de cada fuente. Usar cuando el usuario pida un roadmap, una guía de estudio o una síntesis de un tema a partir de fuentes.
---

# Roadmap de estudio

El roadmap es una **síntesis aplicada**: no explica un tema en general, sino qué parte de ese tema necesita *este* proyecto, en qué orden estudiarla, y qué sale mal si se ignora. Cada afirmación sale de una fuente y cada fuente usada queda enlazada. Se escribe en el idioma y el registro del usuario (si escribe en rioplatense, con voseo).

## Pasos

1. **Leer el pedido.** Sacar de él:
   - los temas (cada tema grande es una **Parte**);
   - el **caso**: el proyecto concreto, sus entidades y sus números (usuarios, registros, peticiones, dispositivos);
   - lo que el usuario ya sabe, que queda fuera del roadmap;
   - las **fuentes del usuario**: URLs, repos, PDFs o archivos locales. Si el tema es de desarrollo de software, se suman siempre las **fuentes fijas** de [`fuentes.md`](fuentes.md);
   - el destino: el que pida el usuario; si no, donde ya guarda sus documentos de estudio, siguiendo su convención de nombres; si no hay ninguna, `roadmap-<tema>.md` en el directorio actual.

   Un dato ambiguo ("10 mil por organizar") se interpreta de la forma más razonable y se anota como **supuesto**.

   Si el pedido no trae un caso, preguntar con `AskUserQuestion` antes de seguir:
   - **Escribir el caso** (recomendada): esperar a que lo escriba y seguir.
   - **Sin caso**: vistazo general del área; versión floja, útil para orientarse, no para decidir qué necesita un proyecto. Leer [`vistazo.md`](vistazo.md) y seguir los pasos con sus cambios.
   - **Caso ficticio** (opcional, si el tema da para proponer uno): la opción trae la propuesta en una línea, con entidades y números. Se sigue como un caso normal: sus números son supuestos y el documento lo declara ficticio.

   Un pedido que ya dice que quiere un vistazo sin proyecto cuenta como **Sin caso**, sin preguntar.

   Hecho cuando están anotados los temas, el caso, los supuestos y la lista de fuentes del usuario.

2. **Dimensionar.** Si el caso trae números, hacer la cuenta *back-of-the-envelope*: carga por segundo, filas por año y volumen con 100 y 1.000 instancias del caso. Cerrar con una conclusión de una línea sobre dónde está lo difícil (escala, correctitud, seguridad, operación). Esa conclusión decide qué va a ESTUDIAR y qué a CONOCER. Hecho cuando cada número del caso tiene su cuenta.

3. **Mapear la cobertura.** Antes de investigar, listar las subsecciones que el roadmap va a tener. El mapa está completo cuando cubre:
   - **los conceptos** de cada tema que el caso toca;
   - **la tecnología concreta** que el proyecto usa o va a usar (el motor de base de datos, el framework, la nube), cada una con su propia subsección "en profundidad", aparte de los conceptos generales: lo que aparece apenas eso está en producción;
   - **dónde se despliega**, empezando por una arquitectura base recomendada para la escala del caso;
   - **las alternativas que alguien va a proponer** (microservicios, GraphQL, NoSQL, colas, Kubernetes, sharding): cada una con su subsección completa, aunque sea [CONOCER], porque el usuario tiene que poder discutirlas.

   Hecho cuando cada punto de la lista tiene subsecciones asignadas.

4. **Investigar.** Despachar un subagente **en segundo plano** por Parte, en paralelo; pasarle el caso, los supuestos, la conclusión del paso 2, lo que el usuario ya sabe, el mapa de su Parte y las fuentes del usuario. Cada investigación:
   - Lee **todas** las fuentes del usuario y recorre las fuentes fijas que tocan su Parte. En un repo o una lista *awesome*, recorrer el índice y abrir las secciones que tocan el caso; anotar el enlace exacto a la sección (con su ancla `#...`), no solo a la raíz del repo.
   - Busca en internet lo que falte, prefiriendo **fuentes primarias**: documentación oficial, specs, OWASP, el repo del proyecto. Un artículo secundario solo entra si explica algo que la fuente primaria no.
   - Lleva cada afirmación hasta su **dueño**: la fuente que la define (la doc oficial de PostgreSQL para un comportamiento de PostgreSQL, la spec para un protocolo). Una lista *awesome* o unas notas son el camino, no el dueño: se cita la sección del repo que llevó ahí y también el dueño. Cada dato concreto (un límite, un valor por defecto, un comportamiento) lleva el enlace a su dueño.
   - Comprueba la **vigencia** de cada servicio o herramienta recomendada: si está discontinuado o dejó de aceptar clientes nuevos, se anota con el enlace al aviso oficial y su reemplazo.
   - Devuelve por concepto: qué es, por qué toca a este caso, un escenario, la clasificación propuesta y los enlaces que lo respaldan.

   Mientras las investigaciones corren, escribir lo que no depende de ellas: título, caso, dimensionamiento y "Cómo leer este documento". Hecho cuando cada subsección del mapa tiene sus conceptos, cada dato concreto tiene el enlace a su dueño, y cada fuente del usuario está citada en algún concepto o anotada como "no aportó" con el motivo.

5. **Clasificar.** Cada concepto lleva una etiqueta:
   - **[ESTUDIAR]**: el caso lo necesita con sus números y requisitos actuales.
   - **[CONOCER]**: resuelve un problema que aparece solo si cambia algo (más escala, un requisito nuevo, otra decisión del equipo). Su escenario dice qué tendría que cambiar.

   En una alternativa [CONOCER] que el equipo podría adoptar, marcar con **(\*)** los conceptos que pasan a [ESTUDIAR] si se adopta (los que más problemas de rendimiento o seguridad generan), y decir para qué parte del caso conviene no usarla aunque se adopte. Ordenar los conceptos en **fases** por orden de estudio: lo que es base de otra cosa va antes. Hecho cuando cada concepto tiene etiqueta y fase.

6. **Escribir** con el formato de abajo. El **escenario** es el corazón del documento y va en **todos** los conceptos, [ESTUDIAR] y [CONOCER], en todas las Partes: una situación de este proyecto, con sus entidades y sus números, y el **problema**: lo que concretamente se rompe, se pierde o se filtra si el concepto falta. Un escenario que valdría para cualquier proyecto se reescribe con las entidades del caso. Hecho cuando cada concepto tiene explicación, escenario, problema y enlace, ningún dato concreto queda sin el enlace a su dueño, y cada Parte termina en su proyecto práctico.

7. **Verificar.** Comprobar que cada enlace responde (`curl -sIL -o /dev/null -w '%{http_code}' <url>`) y que cada ancla de GitHub existe en la página. Corregir o quitar los rotos. Hecho cuando todos los enlaces responden 200.

8. **Entregar.** Informar al usuario:
   - el archivo, las Partes y fases;
   - la conclusión del dimensionamiento y cómo cambió las prioridades;
   - los supuestos, pidiendo que los corrija si no son así;
   - las **preguntas para el equipo**: decisiones del caso que cambian el diseño (por ejemplo, si un dispositivo manda valores absolutos o deltas), con la fase donde se explican;
   - las fuentes del usuario que no aportaron.

   Si pidió PDF, convertir el `.md` con la skill `tool:pdf`, sin tocar el contenido.

## Formato

El `.md` se escribe ya listo para `tool:pdf`: solo párrafos, títulos, citas y enlaces. Sin tablas, sin viñetas ni listas numeradas: cada fila o ítem es un párrafo que empieza con su tema en **negrita**.

```markdown
# Roadmap: <temas>

Roadmap pensado para una plataforma con estas características:

<Hecho del caso con sus números en **negrita**.>

<Otro hecho.>

## Cómo leer este documento

**[ESTUDIAR]**: lo vas a necesitar sí o sí para este proyecto. Estudialo en profundidad y practicalo.

**[CONOCER]**: entendé qué es, qué problema resuelve y en qué momento te haría falta. No lo implementes hasta que aparezca la necesidad real.

Cada concepto tiene un bloque Escenario / Problema: una situación concreta de esta plataforma y lo que sale mal si no aplicás ese concepto. Si el escenario no te parece realista para tu caso, probablemente ese tema pueda esperar.

<Orden sugerido: qué fases son el núcleo, cuáles se pueden intercalar y cuáles conviene estudiar en paralelo.>

## Parte 1. <Tema>

## Fase 0. Dimensionar antes de diseñar

**[ESTUDIAR]**

**Estimaciones back-of-the-envelope**: <qué son y qué evitan>.

> **Escenario:** <...>

> **Problema:** <...>

Aplicado a tu caso:

**<Magnitud>**: <cuenta>, resultado <valor>.

Conclusión: <dónde está lo difícil y, por lo tanto, dónde va el tiempo de estudio>.

## Fase 1. <Área>

**[ESTUDIAR]**

**<Concepto>**: <qué es y por qué toca a este caso, en dos o tres oraciones>.

> **Escenario:** <situación concreta del proyecto>.

> **Problema:** <qué se rompe, con números o consecuencias visibles>.

[<owner/repo - Sección>](<url con ancla>)

### <Tecnología> en profundidad [ESTUDIAR]

<Lo anterior son conceptos generales; estos son propios de <tecnología> y aparecen apenas está en producción.>

<bloques de concepto>

### <Tecnología> en profundidad [CONOCER]

<bloques de concepto>

Recursos: [<fuente general de la fase>](<url>)

## Fase N. <Alternativa>

**[CONOCER]** <Por qué no hace falta hoy. Si el equipo la adopta, los puntos con (\*) pasan a [ESTUDIAR].>

**<Concepto> (\*)**: <...>

## Proyecto práctico sugerido

Para fijar todo lo anterior, construir una versión mínima:

**Paso 1:** <construcción mínima que fija los conceptos [ESTUDIAR] de las primeras fases>.

**Paso 2:** <...>, con un test o una simulación que demuestre que funciona.

## Fuentes principales

[<fuente>](<url>): <qué se tomó de ella, en una línea>.
```

- Con una sola Parte, se omite la línea `## Parte`. Con varias, las fases se numeran dentro de cada Parte.
- Los enlaces se escriben `[owner/repo - Sección](url)` para repos y `[Sitio - Página](url)` para el resto, así el lector sabe adónde va antes de abrirlo.
- Cada bloque va separado por una línea en blanco, y el escenario y el problema van cada uno en su propio `> `.
- Las flechas y símbolos se escriben en ASCII (`->`, `>=`): la fuente del PDF no los tiene.
