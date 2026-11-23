# tool:paginar-pdf

Acomoda un PDF existente de a dos páginas por cara en hojas A4 apaisadas, ordenado para imprimir doble faz y cortar por el medio. Claude lo usa solo cuando se lo pides; esta guía es para correr el script a mano.

## Requisitos

[uv](https://docs.astral.sh/uv/). Instala PyMuPDF solo la primera vez que corres el script, sin que tengas que hacer nada.

## Uso

```bash
uv run tool:paginar-pdf/scripts/paginar.py libro.pdf
```

Genera `libro-paginado.pdf` junto al original. Si la skill está instalada, el script está en `~/.claude/skills/tool:paginar-pdf/scripts/paginar.py`.

| Opción | Qué hace |
|---|---|
| `-o salida.pdf` | Elige el nombre y la carpeta de la salida. |
| `--recortar` | Quita el margen en blanco y agranda el texto. Mide el área con texto de todas las páginas y las recorta igual, así el cuerpo queda del mismo tamaño en todas. Una portada o ilustración puede perder borde. |

```bash
uv run tool:paginar-pdf/scripts/paginar.py libro.pdf --recortar -o libro-grande.pdf
```

## Cómo sale

- Cada hoja lleva cuatro páginas: frente `[1, 3]`, dorso `[2, 4]`; luego `[5, 7]` y `[6, 8]`. Si el total no es múltiplo de 4, el hueco final queda en blanco.
- Entre las dos páginas hay una línea vertical gris oscuro de 1 pt, para cortar la hoja después de imprimirla.
- Las marcas de corte y registro de imprenta no se imprimen.
- Cada página se escala para entrar en su mitad, sea cual sea su tamaño original.

## Imprimir

Doble faz, volteando por el **borde largo**: la 1 queda detrás de la 2 y la 3 detrás de la 4. Si la 2 sale boca abajo respecto de la 1, prueba con el borde corto.
