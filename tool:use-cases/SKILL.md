---
name: tool:use-cases
description: Genera o actualiza el documento de casos de uso de un proyecto (actores, historias de usuario y reglas de negocio por feature), para compartir con alguien no técnico. Usar cuando el usuario pida documentar casos de uso, historias de usuario o reglas de negocio.
---

# Casos de uso

El documento es el **resumen funcional** del proyecto: qué puede hacer cada actor hoy y bajo qué reglas. Su lector es alguien del negocio que nunca vio el código, así que todo se escribe en el **vocabulario del usuario**: lo que se ve, se toca y se decide. Lo técnico (archivos, funciones, endpoints, librerías, tablas, formatos internos, nombres de variables) queda afuera; si una regla solo se explica con eso, se describe por su efecto visible ("el corte no se pierde aunque se corte la conexión").

Cada historia dice **qué** hace el actor, nunca **por dónde**: los menús, botones, rutas de navegación ("desde «…» › «Escanear biblioteca»") y atajos de teclado son interfaz y quedan afuera. "Como dueño, escaneo la biblioteca para buscar los datos", no "desde el menú toco «Escanear»".

## Pasos

1. **Ubicar el documento.** Si el proyecto ya tiene uno (`docs/casos-de-uso.md` o similar), se actualiza ese conservando su redacción donde siga siendo cierta. Si no, se crea `docs/casos-de-uso.md`. Hecho cuando está decidido el archivo destino.
2. **Relevar lo implementado.** Fuentes, en este orden de autoridad: el código y sus tests (lo que de verdad hace), luego `GLOSSARY.md`, ADRs, specs e issues cerradas (el porqué y los nombres). Solo entra lo que está implementado; lo planeado o a medio hacer queda afuera. Cada regla sale de un lugar concreto: un límite, una validación, un mensaje de error, un caso de test. Hecho cuando cada feature tiene sus actores, sus acciones y **todas** sus reglas: cada validación, límite numérico, confirmación, caso de error y efecto secundario que el código aplica tiene su línea.
3. **Escribir** con el formato de abajo. Hecho cuando el documento cubre cada feature relevada y ninguna línea menciona un detalle técnico.
4. **Reportar** al usuario el archivo, las features cubiertas y las dudas: reglas cuyo motivo o comportamiento no quedó claro del código van como preguntas, no como suposiciones.

## Formato

```markdown
# Casos de uso

<Una o dos oraciones: qué es el producto y para qué sirve.>

## Actores

* **<Actor>**: <quién es y qué hace en el sistema, en una línea>.

## Resumen

* **[<Feature>](#<ancla-de-su-sección>)**: <qué permite, en una línea>.

## <Feature>

* Como <actor>, puedo <acción>.
  * <Regla de negocio.>
  * <Regla de negocio, con ejemplo concreto si ayuda: `40090` es el pedido `040090`.>

### <Sub-feature, si la feature es grande>
```

- Un `##` por feature, en el orden en que el usuario las recorre.
- Cada historia es `Como <actor>, puedo/debo <acción>.`; sus reglas cuelgan debajo como sub-bullets, una regla por bullet. Una regla que no pertenece a ninguna historia va como bullet suelto en la feature.
- Los números van exactos (límites, plazos, cantidades), con un ejemplo cuando el límite se entiende mejor visto.
- El actor es un rol (operador, supervisor, usuario invitado), nunca un componente del sistema. Lo que el sistema hace solo se cuenta desde el punto de vista del actor que lo ve.
