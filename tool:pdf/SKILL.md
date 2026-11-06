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

Cada bloque cortado muestra al menos 3 líneas antes del corte; si no llega, empieza en la columna o página siguiente y deja ese espacio en blanco. Un título, o un párrafo todo en negrita como `**[ESTUDIAR]**`, va pegado al comienzo de lo que le sigue. El script lo valida: si una página igual termina con un título o un bloque recién empezado, sale con error nombrando la página y el texto, y ese PDF no se entrega.

## Diagramas

Un bloque `![epígrafe](diagrama.svg)` inserta el SVG centrado en la página, con la ruta relativa al archivo de entrada; el epígrafe es opcional. En `columnas` el diagrama corta las dos columnas y queda centrado sobre el espacio entre ellas: el texto anterior se reparte parejo arriba y el siguiente sigue abajo.

Cuando el diagrama no existe todavía, invocar la skill `diagram-design` para elegir el tipo y componerlo, y escribir el resultado como un archivo SVG suelto. Las reglas de abajo mandan sobre las suyas: reemplazan su guía de estilo (paleta, tipografías y consulta inicial) y su salida en HTML.

- **Completo**: el diagrama lleva todo lo que el contenido necesita para entenderse. El límite de elementos de `diagram-design` decide cuándo dividir, nunca qué se omite. Al pasarlo, repartir todos los elementos en varios diagramas que se muestran uno debajo del otro: bloques `![epígrafe](...)` seguidos, sin texto entre ellos, con el mismo elemento rotulado donde uno termina y el siguiente empieza. El script los mantiene juntos en una página, pasa el grupo a la siguiente si no entra y lo centra en lo que queda de página cuando el texto siguiente no llega a empezar ahí, así que su alto sumado no debe pasar de 900 px (A4) para no partirse. Si dividirlo cortaría algo que solo se entiende entero, dejarlo en un único diagrama aunque pase el límite.
- **Grises** por defecto, para imprimir en blanco y negro. Rellenos `#ffffff`, `#d9d9d9` y `#333333` (este con texto blanco); líneas y el resto del texto `#000000`. Cada tipo de elemento se distingue también por su forma, su rótulo o su trazo (`stroke-dasharray`), de modo que nada dependa solo del tono.
- **Color** únicamente si el usuario lo pide, y entonces correr con `--color`. Sin esa opción, un SVG con colores corta la ejecución.
- **Dibujo directo**: el conversor ignora `marker`, `pattern` y `dominant-baseline`. Las puntas de flecha son `<polygon>` y el texto se centra con `text-anchor="middle"` más una `y` igual al centro + `font-size`/3.
- **Tamaño**: `width`/`height` en px, con un ancho de 640 a 680 para aprovechar la página (460 en `cuadernillo`; lo más grande se achica para entrar, y la letra con él). `font-size` 12 o más, `font-family="Helvetica"`.

## Revisión

Antes de entregar, pasar una página a imagen (`pdftoppm -r 50 -png -f 1 -l 1`) y mirarla. Si hay un diagrama, mirar además su página a `-r 100`: cada rótulo dentro de su forma y cada flecha llegando a su destino.
