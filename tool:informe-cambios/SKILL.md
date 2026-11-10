---
name: tool:informe-cambios
description: Escribe un informe de cambios para enviar a un cliente (un .md, un PDF general y un PDF por etapa) a partir de la conversación, de sesiones anteriores y de los datos del proyecto. Usar cuando el usuario pida un informe, plan de mejoras o análisis con cambios propuestos para entregar a un cliente.
---

# Informe de cambios

Un documento para que el **cliente** entienda qué se va a cambiar, por qué y con qué números. Se escribe como lo diría quien hace el trabajo: frases cortas, primera persona para lo pendiente («tengo que confirmar», «me tienen que confirmar»). Cada cambio cabe en una tabla de tres filas; lo que no tiene número todavía no está listo.

## Pasos

1. **Reunir.** Leer la conversación actual, las sesiones anteriores que indique el usuario (`~/.claude/projects/<proyecto>/<id>.jsonl`) y los archivos con los datos. Hecho cuando cada cambio tiene al menos una cifra con su fuente.
2. **Ordenar en etapas.** Una etapa agrupa cambios del mismo tipo (por ejemplo, mejoras iniciales, mejoras grandes, medición). Hecho cuando cada cambio está en una sola etapa y tiene su número `E.N`.
3. **Escribir el `.md`** con el formato de abajo. Hecho cuando cada cambio tiene sus tres filas y un cliente podría leerlo sin abrir otro archivo.
4. **Humanizar.** Pasar los textos por la skill `humanizer`. Hecho cuando no quedan tics de IA y las cifras siguen iguales.
5. **Generar.**
   ```bash
   python3 -I ~/.claude/skills/tool:informe-cambios/scripts/generar.py informe.md --cliente "Nombre"
   ```
   Crea `entrega/` junto al `.md` con `informe.md` y `informe.pdf` (todo el informe), más `etapa-N.md` y `etapa-N.pdf` por etapa. La primera vez instala sus dependencias (`npm install`) y necesita internet para las fuentes. Hecho cuando el script termina sin error: valida que cada enlace y cada referencia apunten a un cambio que existe.
6. **Mirar.** Pasar la página 1 de cada PDF a imagen (`pdftoppm -r 50 -png -f 1 -l 1`) y revisar que se lee bien. Hecho cuando se vio la imagen de cada PDF.

## Formato del `.md`

```markdown
# Título del informe, sin repetir el nombre del cliente (ya va en el encabezado)

## Resumen

**Etapa 1. Nombre**

1. Qué cambia: el dato que lo justifica. [Ver](#m1-1)
2. ...

## De dónde salen los números

- Fuente: cantidad, período y fecha de descarga.

## Etapa 1. Mejoras iniciales: lo que se puede hacer mejor

Una línea que explique qué tipo de cambios son.

### 1.1 Título del cambio

| | |
|---|---|
| Por qué es mejor | Una frase. |
| Cómo se detectó | Los números y su origen. |
| Qué cambia | Lo que se hace, concreto, sin tener que abrir otro archivo. |
```

- El enlace `[Ver](#mE-N)` va después del punto que cierra cada ítem del resumen; `E-N` es el número del cambio con guion (`1.3` es `#m1-3`).
- Filas extra cuando hacen falta, con el mismo estilo: `Mientras tanto`, `Definir`, `Cómo se elige`.
- Para nombrar un cambio de otra etapa, escribir `{{2.2}}`: el PDF general muestra `2.2` y el PDF de la etapa 1 muestra «mejora grande que estoy documentando».
- Secciones sin etapa (por ejemplo, decisiones pendientes) quedan solo en el PDF general.
- Las fechas llevan año. Sin `·`, sin MAYÚSCULAS sostenidas, sin «sección N» ni nombres de archivos internos, sin cifras de dinero si el usuario dijo que todavía no se habla de plata.
- Con más de una etapa, la portada del PDF general lleva el título, una frase y un índice con enlaces al pie; el resumen empieza en la hoja siguiente. La frase es el primer párrafo bajo el título: una sola oración con el objetivo del informe.
- El PDF lo arma el script con el estilo escandinavo (`scripts/src/build.tsx`); no se pasa por `tool:pdf`.
