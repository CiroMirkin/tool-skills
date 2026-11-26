# Referencias de desarrollo de software

Base compartida por `learn:roadmap`, `learn:learn` y `learn:doc-estudio`. Cada referencia es un **repo** o un **sitio**, y se consulta cuando el tema es de desarrollo de software, junto con las fuentes que pase el usuario. Se suman entradas con `/learn:referencia <url>`, y la carpeta de documentos personales con `/learn:referencia --docs <ruta>`.

Una referencia es el **camino**, no el dueño: sirve para encontrar qué cubrir y dónde mirar, y se cita la sección o la lección que llevó ahí junto con la fuente que define cada dato. Se recorre el índice, se abren solo las secciones que tocan el caso y se enlaza la exacta: en un repo, la sección con su ancla `#...`; en un sitio, la lección o el capítulo, nunca la portada.

## Documentos personales

Además de los repos y sitios, el usuario puede tener una carpeta local con libros y apuntes. Su ruta está en [`documentos-locales.md`](documentos-locales.md), junto a este archivo: un directorio por línea. Ese archivo es local, git lo ignora y se crea con `/learn:referencia --docs <ruta>`. Si no existe, se omite esta sección.

La carpeta puede tener libros en PDF, que gastan muchos tokens, así que se lee lo mínimo:

- **Elegir sin abrir.** Listar los archivos (nombres y carpetas, con `find` o `ls`) y quedarse solo con los que por su título o su ubicación aportan algo al tema. Si ninguno aporta, no se lee ninguno y se sigue con las demás referencias.
- **Leer solo lo necesario.** Un PDF se ubica primero por su índice (las primeras páginas, o `pdftotext -f <desde> -l <hasta>`) y después se leen solo las páginas del capítulo que toca, con `pages` en `Read`. Un `.md` o `.txt` se recorre con `grep` y se lee con `offset` y `limit`. Nunca se vuelca un libro entero para ver si sirve.
- **Lectura completa solo si se pide.** Se lee un documento entero únicamente cuando el usuario lo indica de forma explícita ("leé este libro completo").
- **Citar.** Cada dato que sale de un documento personal se cita con su título y su capítulo o página, sin enlace. El contenido de los libros no se copia en el resultado, solo se resume o se cita en pocas líneas.

## Arquitectura, sistemas y escala

[mehdihadeli/awesome-software-architecture](https://github.com/mehdihadeli/awesome-software-architecture): lista curada de arquitectura, patrones y principios (DDD, microservicios, CQRS, multi-tenancy, mensajería, bases de datos). Versión navegable en awesome-architecture.com.

[david8zhang/system-design-notes](https://github.com/david8zhang/system-design-notes): notas de diseño de sistemas basadas en *Designing Data-Intensive Applications* (replicación, particionamiento, transacciones, índices, almacenamiento).

[liquidslr/system-design-notes](https://github.com/liquidslr/system-design-notes): notas de *System Design Interview* de Alex Xu (estimaciones back-of-the-envelope, escalado, rate limiting, IDs únicos, colas).

[binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability): patrones de sistemas escalables, confiables y performantes, con casos reales de empresas.

## Correctitud y datos del mundo real

[kdeldycke/awesome-falsehood](https://github.com/kdeldycke/awesome-falsehood): supuestos falsos que los programadores creen sobre fechas, zonas horarias, nombres, direcciones, dinero, números, paginación e internacionalización.

## Planes de estudio y roadmaps

[nilbuild/developer-roadmap](https://github.com/nilbuild/developer-roadmap): roadmaps interactivos por rol y tecnología (backend, frontend, design system, DevOps); sirve para chequear que el mapa de cobertura no deje huecos.

[ossu/computer-science](https://github.com/ossu/computer-science): currículo completo y gratuito de ciencias de la computación; para fundamentos (algoritmos, sistemas operativos, redes, bases de datos) con cursos concretos.

[jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university): plan de estudio de ciencias de la computación orientado a ingeniería de software.

[yangshun/tech-interview-handbook](https://github.com/yangshun/tech-interview-handbook): material curado de preparación de entrevistas técnicas (algoritmos, diseño de sistemas, comportamiento).

[DevCaress/guia-entrevistas-de-programacion](https://github.com/DevCaress/guia-entrevistas-de-programacion): guía de entrevistas de programación en español.

[bregman-arie/devops-exercises](https://github.com/bregman-arie/devops-exercises): preguntas y ejercicios de DevOps e infraestructura (Linux, redes, Git, Docker, Kubernetes, CI/CD, cloud, Terraform, Ansible, bases de datos); sirve para chequear qué conceptos de operación toca el caso.

## Sitios de aprendizaje

[The Odin Project](https://www.theodinproject.com/paths): currículo gratuito y abierto de desarrollo web, con lecturas curadas y proyectos para construir; rutas [Foundations](https://www.theodinproject.com/paths/foundations/courses/foundations), [Full Stack JavaScript](https://www.theodinproject.com/paths/full-stack-javascript) y [Full Stack Ruby on Rails](https://www.theodinproject.com/paths/full-stack-ruby-on-rails). Sirve para fundamentos web (HTML, CSS, JavaScript, Git, línea de comandos, Node, bases de datos) y para ver en qué orden se estudian; su currículo vive en [TheOdinProject/curriculum](https://github.com/TheOdinProject/curriculum).

[System Design, an interactive course](https://designed-to-scale.vercel.app/): curso interactivo de diseño de sistemas donde cada idea es un diagrama animado que se recorre paso a paso (balanceo de carga, caché, sharding, consenso, colas, observabilidad y diseños completos, de un servidor a millones de usuarios).

[Full Stack Open](https://fullstackopen.com/en/): curso abierto y gratuito de desarrollo web con JavaScript de la Universidad de Helsinki, en partes con ejercicios (fundamentos web, React, comunicación con el servidor, Node y Express, testing, estado, GraphQL, TypeScript, React Native, CI/CD, contenedores, bases de datos relacionales y Next.js); hay traducción al español.

## Lenguajes y plataformas

[goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices): buenas prácticas de Node.js (estructura, errores, seguridad, testing, producción).

[melissarofman/typescript-book](https://github.com/melissarofman/typescript-book): libro libre de TypeScript.

[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch): ingeniería de IA de punta a punta (LLMs, RAG, agentes, despliegue).

## Apuntes de diseño y proceso

[CiroMirkin/apuntes](https://github.com/CiroMirkin/apuntes): apuntes teóricos en español, uno por tema (SOLID, GRASP, cohesión y acoplamiento, patrones como MVC, repositorio y value object, arquitectura por capas y C4, TDD/BDD, refactorización, Big O, normalización, Kanban, historias de usuario); dan una idea clara de cada concepto para enlazar como punto de partida.

## Libros

[mouredev/free-programming-books](https://github.com/mouredev/free-programming-books): índice de libros de programación gratuitos, por lenguaje y tema.

[sevenweeks/databases](https://github.com/sevenweeks/databases): código de cada capítulo del libro *Seven Databases in Seven Weeks* con correcciones de errores, para seguir el libro y probar distintos modelos de bases de datos (relacional, clave-valor, columnas, documentos, grafos).
