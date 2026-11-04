---
name: tool:pdf
description: Convierte un archivo de texto en PDF, en dos columnas justificado (por defecto), una columna, o cuadernillo para imprimir. Usar cuando el usuario pida pasar un texto a PDF.
---

# Texto a PDF

El PDF reproduce el archivo de texto tal cual: todo el contenido, en el orden en que está, con las páginas que haga falta. Si el contenido todavía no está en un archivo, guardarlo primero en uno.

```bash
uv run ~/.claude/skills/tool:pdf/scripts/pdf.py <entrada.txt> [-f columnas|simple|cuadernillo] [-o salida.pdf]
```

- `columnas` (por defecto): A4, dos columnas, justificado.
- `simple`: A4, una columna.
- `cuadernillo` (booklet): páginas A5 de a dos por hoja A4 apaisada, reordenadas para que al imprimir doble faz y doblar al medio queden en orden. Al entregarlo, decirle al usuario que imprima doble faz **volteando por el borde corto**.

La salida por defecto es el mismo nombre con `.pdf`, junto a la entrada. Cada página lleva su número, chico y centrado al pie. El script entiende `# ` título, `## ` sección, `### ` subsección, bloques de `- ` viñetas, bloques de `> ` cita (sangrados), `**negrita**`, `*itálica*` y `[texto](url)`; los párrafos y bloques se separan con una línea en blanco. Si el texto usa otras marcas, se imprimen literales.

Antes de entregar, pasar una página a imagen (`pdftoppm -r 50 -png -f 1 -l 1`) y mirarla.
