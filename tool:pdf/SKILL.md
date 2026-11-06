---
name: tool:pdf
description: Convierte un archivo de texto en PDF, en dos columnas justificado (por defecto), una columna, o cuadernillo para imprimir, con diagramas si hacen falta. Usar cuando el usuario pida pasar un texto a PDF o sumarle un diagrama.
---

# Texto a PDF

El PDF reproduce el archivo de texto tal cual: todo el contenido, en el orden en que está, con las páginas que haga falta. Si el contenido todavía no está en un archivo, guardarlo primero en uno.

```bash
uv run ~/.claude/skills/tool:pdf/scripts/pdf.py <entrada.txt> [-f columnas|simple|cuadernillo] [--color] [-o salida.pdf]
```

- `columnas` (por defecto): A4, dos columnas, justificado.
- `simple`: A4, una columna.
- `cuadernillo` (booklet): páginas A5 de a dos por hoja A4 apaisada, reordenadas para que al imprimir doble faz y doblar al medio queden en orden. Al entregarlo, decirle al usuario que imprima doble faz **volteando por el borde corto**.

La salida por defecto es el mismo nombre con `.pdf`, junto a la entrada. Cada página lleva su número, chico y centrado al pie. El script entiende `# ` título, `## ` sección, `### ` subsección, bloques de `- ` viñetas, bloques de `> ` cita (sangrados), `**negrita**`, `*itálica*` y `[texto](url)`; los párrafos y bloques se separan con una línea en blanco. Si el texto usa otras marcas, se imprimen literales.

## Diagramas

Un bloque `![epígrafe](diagrama.svg)` inserta el SVG centrado en la página, con la ruta relativa al archivo de entrada; el epígrafe es opcional. En `columnas` el diagrama corta las dos columnas y queda centrado sobre el espacio entre ellas: el texto anterior se reparte parejo arriba y el siguiente sigue abajo.

Cuando el diagrama no existe todavía, invocar la skill `diagram-design` para elegir el tipo y componerlo, y escribir el resultado como un archivo SVG suelto. Las reglas de abajo mandan sobre las suyas: reemplazan su guía de estilo (paleta, tipografías y consulta inicial) y su salida en HTML.

- **Grises** por defecto, para imprimir en blanco y negro. Rellenos `#ffffff`, `#d9d9d9` y `#333333` (este con texto blanco); líneas y el resto del texto `#000000`. Cada tipo de elemento se distingue también por su forma, su rótulo o su trazo (`stroke-dasharray`), de modo que nada dependa solo del tono.
- **Color** únicamente si el usuario lo pide, y entonces correr con `--color`. Sin esa opción, un SVG con colores corta la ejecución.
- **Dibujo directo**: el conversor ignora `marker`, `pattern` y `dominant-baseline`. Las puntas de flecha son `<polygon>` y el texto se centra con `text-anchor="middle"` más una `y` igual al centro + `font-size`/3.
- **Tamaño**: `width`/`height` en px, con un ancho de 640 a 680 para aprovechar la página (460 en `cuadernillo`; lo más grande se achica para entrar, y la letra con él). `font-size` 12 o más, `font-family="Helvetica"`.

## Revisión

Antes de entregar, pasar una página a imagen (`pdftoppm -r 50 -png -f 1 -l 1`) y mirarla. Si hay un diagrama, mirar además su página a `-r 100`: cada rótulo dentro de su forma y cada flecha llegando a su destino.
