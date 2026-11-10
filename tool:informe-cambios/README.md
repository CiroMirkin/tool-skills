# tool:informe-cambios

Escribe un informe de cambios para enviar a un cliente. Claude junta los datos de la conversación, de sesiones anteriores y de los archivos del proyecto, ordena los cambios en etapas y entrega un `.md` y sus PDF.

> [!NOTE]
> Esta skill está en revisión.

## Qué entrega

Una carpeta `entrega/` junto al `.md` de origen, que no se modifica:

| Archivo | Contenido |
|---|---|
| `informe.md`, `informe.pdf` | El informe completo, con portada e índice si hay más de una etapa. |
| `etapa-N.md`, `etapa-N.pdf` | Una etapa: el resumen, «De dónde salen los números» y la etapa. |

Cada cambio se presenta en una tabla de tres filas: por qué es mejor, cómo se detectó y qué cambia. Un cambio sin cifra con su fuente no entra.

## Requisitos

- Node.js con `npm`. La primera vez el script corre `npm install` en `scripts/`.
- Python 3, para `scripts/generar.py`.
- Internet, para bajar las fuentes Inter y JetBrains Mono de Google Fonts.
- La skill `humanizer`, que Claude usa para pulir los textos.
- `pdftoppm` (paquete `poppler-utils`), para revisar la primera página de cada PDF.

## Uso

```text
/tool:informe-cambios arma el informe de mejoras para el cliente
```

Para generar los PDF a mano desde un `.md` ya escrito:

```bash
python3 -I ~/.claude/skills/tool:informe-cambios/scripts/generar.py informe.md --cliente "Nombre"
```

El script valida que cada enlace `[Ver](#mE-N)` y cada referencia `{{E.N}}` apunten a un cambio que existe, y falla si no.

## Formato del `.md`

```markdown
# Título del informe

## Resumen

**Etapa 1. Nombre**

1. Qué cambia: el dato que lo justifica. [Ver](#m1-1)

## De dónde salen los números

- Fuente: cantidad, período y fecha de descarga.

## Etapa 1. Mejoras iniciales: lo que se puede hacer mejor

### 1.1 Título del cambio

| | |
|---|---|
| Por qué es mejor | Una frase. |
| Cómo se detectó | Los números y su origen. |
| Qué cambia | Lo que se hace, concreto. |
```

- `{{2.2}}` nombra un cambio de otra etapa: el PDF general muestra `2.2` y el de la etapa 1 muestra «mejora grande que estoy documentando».
- Las secciones sin etapa quedan solo en el PDF general.

Las reglas completas están en [SKILL.md](SKILL.md).

## Estructura

- `SKILL.md`: los pasos y el formato que sigue Claude.
- `scripts/generar.py`: parte el informe por etapas y llama a `md-a-pdf.sh`.
- `scripts/md-a-pdf.sh`: convierte un `.md` en PDF con el estilo escandinavo.
- `scripts/src/`: el render del PDF (`build.tsx`, componentes y tema).
