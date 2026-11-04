---
name: tool:readme
description: Escribe o reescribe el README.md de un proyecto a partir de relevar todo el repo, con estilo de proyecto open source (header con logo y badges, features, instalación, uso). Usar cuando el usuario pida un README o mejorar el que hay.
---

# README

El README es la **vitrina** del proyecto: en una lectura de treinta segundos, alguien que nunca lo vio entiende qué es, por qué le sirve y cómo arrancarlo. Atractivo y escaneable, nunca largo: cada sección se gana el lugar respondiendo una pregunta que el lector de verdad se hace. Todo lo que dice sale del repo; un comando, flag, variable o badge que no está en el repo no existe.

## Pasos

1. **Relevar el proyecto entero.** Fuentes: el README actual si hay, los manifiestos (`package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`, `justfile`…), los entrypoints y el `--help` de la CLI, la config y las variables de entorno que el código lee, `docs/`, `GLOSSARY.md`, ADRs, los workflows de `.github/` y `git remote -v` (para el `owner/repo` de los badges). Buscar el **logo**: imágenes cuyo nombre o carpeta sugiera logo, icon o favicon (`find . -iname '*logo*' -o -iname '*icon*' -o -iname 'favicon*'` fuera de `node_modules`, `.venv`, `dist`). Hecho cuando sabés qué hace el proyecto, para quién, qué lo distingue, cómo se instala y se corre, con qué personas y sistemas externos habla (cada uno sacado de un import, una URL, una API key o una ruta del código), y tenés la ruta del logo o confirmaste que no hay.
2. **Dibujar el diagrama de contexto** según la sección de abajo. Hecho cuando el diagrama tiene cada actor y sistema externo del paso 1, y nada más.
3. **Escribir** `README.md` en la raíz con la estructura de abajo, en el idioma de los docs del proyecto. Si ya había README, conservar lo que siga siendo cierto. Hecho cuando cada comando del README es uno que el paso 1 encontró en un script, manifiesto o `--help`.
4. **Verificar**: cada ruta relativa (logo, diagrama, imágenes, links a `docs/`, `LICENSE`) existe, cada badge apunta a algo real (el workflow de CI existe, el paquete está publicado, el archivo de licencia existe) y cada ancla de la barra de navegación coincide con un encabezado. Hecho cuando no queda ningún link roto.
5. **Reportar** el archivo y lo que no se pudo confirmar desde el repo (requisitos, plataformas, un paso de instalación dudoso), como preguntas.

## Estructura

Tomada de los README de [smoke](https://github.com/sinedied/smoke), [run-on-output](https://github.com/sinedied/run-on-output) y los samples serverless de Azure-Samples. Las secciones opcionales van solo si el proyecto tiene con qué llenarlas.

```markdown
<div align="center">

<img src="<logo>" alt="" height="96" />

# <nombre>

*<tagline: qué hace, en una línea>*

<badges>

[Features](#features) • [Instalación](#instalación) • [Uso](#uso)

</div>

<Pitch: uno o dos párrafos con qué es, qué problema resuelve y para quién.>

<Opcional: captura, GIF de demo o un ejemplo mínimo de 3 pasos que muestre el valor de entrada.>

## Features

- **<Feature>**: <qué le da al usuario, en una línea>.

## Instalación

<Requisitos (runtime y versión, herramientas del sistema) y los comandos, en bloques con lenguaje.>

## Uso

<Del caso más común al avanzado: ejemplos que se pueden copiar y pegar, opciones de la CLI en tabla.>

## Cómo funciona

<Diagrama de contexto y un párrafo que lo recorra.>

## <Opcionales: Configuración, Troubleshooting, Recursos>
```

- **Header**: centrado. El logo solo si el paso 1 lo encontró. Badges con `style=flat-square` de shields.io, pocos y verificables: CI, versión publicada, runtime, licencia (link a `LICENSE`).
- **Admonitions** de GitHub (`> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`) para lo que el lector no puede pasar por alto: un requisito que rompe la instalación, un costo, una acción destructiva, un atajo útil. Un puñado en todo el README.
- **Sobrio**: emojis como mucho uno decorativo en el header; los encabezados y los bullets van limpios.
- La licencia, cómo contribuir, el changelog y el código de conducta viven en sus propios archivos: el README los enlaza, como mucho, desde un badge.

## Diagrama de contexto

El nivel 1 de C4: el proyecto es **una sola caja** en el centro, rodeada de las personas que lo usan y los sistemas externos de los que depende (APIs, servicios, bases de datos ajenas, el filesystem si es central). Cada flecha lleva un verbo que dice qué viaja ("busca metadatos en", "descarga pósters de"). Lo de adentro del sistema (módulos, capas, tablas) queda para otro diagrama.

- Si la sesión lista una skill de diagramas (como `diagram-design`), generarlo con ella en formato `svg`, guardarlo junto a las otras imágenes del repo (o en `docs/images/` si no hay) y embeberlo con `![Diagrama de contexto](<ruta>)`.
- Si no, un bloque ` ```mermaid ` con `flowchart LR` dentro del README, que GitHub renderiza solo.
