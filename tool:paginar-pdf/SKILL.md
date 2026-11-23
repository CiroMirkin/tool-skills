---
name: tool:paginar-pdf
description: Acomoda un PDF existente de a dos páginas por cara en hojas A4 apaisadas, ordenado para imprimir doble faz. Usar cuando el usuario pida juntar, achicar o imprimir de a dos las páginas de un PDF.
---

# Paginar PDF

Toma un PDF que ya existe y devuelve otro con dos de sus páginas por cara, sin tocar su contenido, con una línea de corte entre las dos páginas.

```bash
uv run ~/.claude/skills/tool:paginar-pdf/scripts/paginar.py <entrada.pdf> [--recortar] [-o salida.pdf]
```

La salida por defecto es `<entrada>-paginado.pdf`, junto a la entrada.

## Orden

Cada hoja lleva cuatro páginas: frente `[1, 3]`, dorso `[2, 4]`; la hoja siguiente sigue con `[5, 7]` y `[6, 8]`. Al imprimir doble faz volteando por el **borde largo**, la 1 queda detrás de la 2 y la 3 detrás de la 4, y apilando las hojas se lee 1, 2, 3, 4, 5... Si el total no es múltiplo de 4, el hueco final queda en blanco.

## Recorte

Solo con `--recortar`, y únicamente si el usuario lo pide, no por defecto. Quita el margen en blanco para que el texto salga más grande: se mide el área con texto de todas las páginas del mismo tamaño y todas se recortan igual (la unión), con 6 pt de respiro. El texto queda del mismo tamaño en cada página y las marcas de corte no cuentan. Una página sin texto (portada, ilustración) se recorta igual que las demás y puede perder borde si su imagen llega más lejos que el texto; revisarla.

## Entrega

Cada página se toma solo dentro de su área de página (MediaBox): las marcas de corte y registro de imprenta, que viven afuera, no se imprimen. Entre las dos páginas va una línea vertical gris oscuro de 1 pt, de borde a borde, para cortar la hoja después de imprimirla. Cada página se escala para entrar en su mitad de la cara, centrada y con margen, sea cual sea su tamaño o rotación original. Al entregar, decirle al usuario que imprima doble faz con volteo por el borde largo, y que si la 2 aparece boca abajo o espejada respecto de la 1, pruebe con el borde corto.

## Revisión

Antes de entregar, pasar las dos primeras caras a imagen (`pdftoppm -r 40 -png -f 1 -l 2`) y confirmar que la cara 1 muestra las páginas 1 y 3, y la cara 2 las páginas 2 y 4.
