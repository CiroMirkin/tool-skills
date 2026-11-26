// Uso: tsx src/build.tsx <entrada.md> <salida.pdf>
// Pasa un informe de cambios en Markdown a PDF con pdfcn + Takumi y el sistema visual escandinavo.
import { readFile, writeFile } from "node:fs/promises";
import type { ReactNode } from "react";
import { marked, type Token, type Tokens } from "marked";
import { googleFonts } from "@takumi-rs/helpers";
import { measure, render } from "takumi-pdf";

import { KeepTogether } from "@/components/pdf/keep-together/keep-together";
import { PageBreak } from "@/components/pdf/page-break/page-break";
import { PageNumber } from "@/components/pdf/page-number/page-number";
import { Text } from "@/components/pdf/text/text";
import { PdfcnThemeProvider } from "@/components/pdf/theme-provider";
import { Text as Span, View } from "@/lib/pdf-primitives";
import { ink, MONO, SANS, scandinavianTheme } from "@/theme-scandinavian";

const [, , INPUT, OUTPUT] = process.argv;
if (!INPUT || !OUTPUT) {
  console.error("uso: tsx src/build.tsx <entrada.md> <salida.pdf>");
  process.exit(1);
}

const MARGIN_X = 40;
// PAGINAR=1 (lo usa parte-1.sh): cada hoja se compone aparte, con el encabezado pegado al margen
// superior y el contenido pegado al inferior, así el espacio libre queda solo en el medio.
const PAGINAR = process.env.PAGINAR === "1";
const MARGIN_TOP = 44;
const PAGE_W = 793.7;
const PAGE_H = 1122.5;
const CONTENT_W = PAGE_W - MARGIN_X * 2;
const SAFETY = 8; // px de resguardo para que una hoja nunca desborde a la siguiente

// ---------- inline ----------

let keySeq = 0;
const k = () => `k${keySeq++}`;

const decode = (s: string) =>
  s
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");

function inline(tokens: Token[] = []): ReactNode[] {
  return tokens.map((t) => {
    switch (t.type) {
      case "strong":
        return (
          <Span key={k()} style={{ fontWeight: 600 }}>
            {inline((t as Tokens.Strong).tokens)}
          </Span>
        );
      case "em":
        return (
          <Span key={k()} style={{ fontStyle: "italic" }}>
            {inline((t as Tokens.Em).tokens)}
          </Span>
        );
      case "codespan":
        return (
          <Span key={k()} style={{ fontFamily: MONO, fontSize: 8.2, color: ink.secondary }}>
            {decode((t as Tokens.Codespan).text)}
          </Span>
        );
      case "link":
        return (
          <Span key={k()} href={(t as Tokens.Link).href} style={{ textDecoration: "underline" }}>
            {inline((t as Tokens.Link).tokens)}
          </Span>
        );
      case "text":
      case "escape": {
        const tt = t as Tokens.Text;
        return tt.tokens ? inline(tt.tokens) : decode(tt.text);
      }
      default:
        return decode((t as { raw: string }).raw);
    }
  });
}

const plain = (tokens: Token[] = []): string =>
  tokens
    .map((t) => {
      const any = t as { tokens?: Token[]; text?: string; raw: string };
      return any.tokens ? plain(any.tokens) : decode(any.text ?? any.raw);
    })
    .join("");

// ---------- bloques ----------

function Para({ children }: { children: ReactNode }) {
  return <Text style={{ marginBottom: 8 }}>{children}</Text>;
}

// Las listas numeradas (el resumen) van más compactas para que entren dos etapas en la primera hoja.
const COMPACTO = { fontSize: 9.6, lineHeight: 1.4 };

function BulletList({ token }: { token: Tokens.List }) {
  return (
    <View style={{ marginBottom: 10, gap: token.ordered ? 3 : 4 }}>
      {token.items.map((item, i) => {
        const body = item.tokens.flatMap((t) =>
          t.type === "text" || t.type === "paragraph" ? inline((t as Tokens.Text).tokens ?? [t]) : [],
        );
        return (
          <View key={k()} style={{ flexDirection: "row", gap: 8 }}>
            {token.ordered ? (
              <Text noMargin style={{ width: 16, color: ink.secondary, ...(token.ordered ? COMPACTO : {}) }}>
                {`${Number(token.start || 1) + i}.`}
              </Text>
            ) : (
              <View
                style={{
                  width: 3,
                  height: 3,
                  borderRadius: 2,
                  backgroundColor: ink.secondary,
                  marginTop: 6,
                  marginLeft: 4,
                  marginRight: 5,
                }}
              />
            )}
            <Text noMargin style={{ flex: 1, ...(token.ordered ? COMPACTO : {}) }}>
              {body}
            </Text>
          </View>
        );
      })}
    </View>
  );
}

// Tablas de 2 columnas sin encabezado (| | |): ficha de una mejora, etiqueta a la izquierda.
function KeyValue({ token }: { token: Tokens.Table }) {
  return (
    <View style={{ marginBottom: 6, gap: 7 }}>
      {token.rows.map((row) => (
        <View key={k()} style={{ flexDirection: "row", gap: 20 }}>
          <View style={{ width: 96 }}>
            <Span style={{ fontFamily: SANS, fontSize: 8.6, fontWeight: 500, color: ink.secondary, lineHeight: 1.5 }}>
              {inline(row[0].tokens)}
            </Span>
          </View>
          <View style={{ flex: 1 }}>
            <Span style={{ fontFamily: SANS, fontSize: 9.6, lineHeight: 1.55 }}>{inline(row[1].tokens)}</Span>
          </View>
        </View>
      ))}
    </View>
  );
}

// Tablas de datos: una línea fina bajo el encabezado y entre filas (superficie densa de consulta).
function DataTable({ token }: { token: Tokens.Table }) {
  const cols = token.header.length;
  const weights = Array.from({ length: cols }, (_, c) => {
    const lens = [token.header[c], ...token.rows.map((r) => r[c])].map((cell) => plain(cell.tokens).length);
    const avg = lens.reduce((a, b) => a + b, 0) / lens.length;
    return Math.min(Math.max(avg, 17), 80);
  });
  return (
    <View style={{ marginBottom: 14 }}>
      <View style={{ flexDirection: "row", borderBottomWidth: 1, borderBottomColor: ink.borderStrong, borderBottomStyle: "solid" }}>
        {token.header.map((h, c) => (
          <View key={k()} style={{ flex: weights[c], paddingBottom: 6, paddingRight: c === cols - 1 ? 0 : 14 }}>
            <Span style={{ fontFamily: SANS, fontSize: 8.4, fontWeight: 500, color: ink.secondary }}>{inline(h.tokens)}</Span>
          </View>
        ))}
      </View>
      {token.rows.map((row) => (
        <View
          key={k()}
          style={{
            flexDirection: "row",
            borderBottomWidth: 0.5,
            borderBottomColor: ink.border,
            borderBottomStyle: "solid",
            breakInside: "avoid",
          }}
        >
          {row.map((cell, c) => (
            <View key={k()} style={{ flex: weights[c], paddingTop: 6, paddingBottom: 6, paddingRight: c === cols - 1 ? 0 : 14 }}>
              <Span style={{ fontFamily: SANS, fontSize: 9, lineHeight: 1.45, fontWeight: c === 0 ? 500 : 400 }}>
                {inline(cell.tokens)}
              </Span>
            </View>
          ))}
        </View>
      ))}
    </View>
  );
}

function MdTable({ token }: { token: Tokens.Table }) {
  const emptyHeader = token.header.every((h) => plain(h.tokens).trim() === "");
  return emptyHeader && token.header.length === 2 ? <KeyValue token={token} /> : <DataTable token={token} />;
}

function block(t: Token): ReactNode {
  switch (t.type) {
    case "paragraph":
      return <Para key={k()}>{inline((t as Tokens.Paragraph).tokens)}</Para>;
    case "list":
      return <BulletList key={k()} token={t as Tokens.List} />;
    case "table":
      return <MdTable key={k()} token={t as Tokens.Table} />;
    default:
      return null;
  }
}

// ---------- documento ----------

type Toc = { kicker: string; title: string; id: string }[];

const slug = (s: string) => s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
// Cada sección de nivel 2 tiene un ancla: «etapa-1» para «Etapa 1», o el título sin tildes.
const idDeSeccion = (text: string, part: { kicker: string } | null) => (part ? slug(part.kicker) : slug(text));

const splitPart = (text: string) => {
  // «Parte 1. Título» o, en general, «Rótulo corto. Título».
  const m = /^([^.:]{3,30})\.\s+(.+)$/.exec(text);
  return m ? { kicker: m[1], title: m[2] } : null;
};

function Cover({ title, lead }: { title: string; lead: string }) {
  return (
    <View style={{ marginTop: 0, marginBottom: PAGINAR ? 0 : 28 }}>
      <Span style={{ fontFamily: SANS, fontSize: 9.5, fontWeight: 500, color: ink.secondary, marginBottom: 14 }}>
        {process.env.COVER_KICKER ?? "Parnerson"}
      </Span>
      <h1 style={{ margin: 0, fontSize: "inherit", fontWeight: "inherit", display: "flex" }}>
        <Span style={{ fontFamily: SANS, fontSize: 34, fontWeight: 600, lineHeight: 1.1, letterSpacing: "-0.02em" }}>{title}</Span>
      </h1>
      {lead ? (
        <View style={{ width: 400, marginTop: 14 }}>
          <Span style={{ fontFamily: SANS, fontSize: 11, lineHeight: 1.5, color: ink.secondary }}>{lead}</Span>
        </View>
      ) : null}
    </View>
  );
}

// Índice al pie de la portada: cada entrada lleva al comienzo de su sección.
function Indice({ toc }: { toc: Toc }) {
  return (
    <View style={{ gap: 7 }}>
      <Span style={{ fontFamily: SANS, fontSize: 9.5, fontWeight: 500, color: ink.secondary, marginBottom: 5 }}>Índice</Span>
      {toc.map((e) => (
        <View key={k()} style={{ flexDirection: "row", gap: 20 }}>
          <View style={{ width: 48 }}>
            <Span style={{ fontFamily: SANS, fontSize: 9.5, color: ink.secondary }}>{e.kicker}</Span>
          </View>
          <Span href={`#${e.id}`} style={{ fontFamily: SANS, fontSize: 10, fontWeight: 500, textDecoration: "underline" }}>{e.title}</Span>
        </View>
      ))}
    </View>
  );
}

type Unit = { node: ReactNode; space: number; header?: boolean; part?: boolean; breakBefore?: boolean };

function buildBody(tokens: Token[], resumenEnHoja: boolean): Unit[] {
  const out: Unit[] = [];
  let inHeader = false; // encabezado de una parte: su título y la introducción antes del primer 1.x
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    if (t.type === "space" || t.type === "hr") continue;

    if (t.type === "heading") {
      const h = t as Tokens.Heading;
      const text = decode(h.text);

      if (h.depth === 2) {
        const part = splitPart(text);
        // Cada parte abre hoja nueva; el resto sigue en la misma.
        inHeader = !!part;
        const innerTop = part || PAGINAR || text === "De dónde salen los números" ? 0 : 34;
        // Un título de sección sin etapa viaja pegado a su primer bloque (salvo que sea el resumen por etapa).
        let sig = i + 1;
        while (sig < tokens.length && tokens[sig].type === "space") sig++;
        const tk = sig < tokens.length ? tokens[sig] : null;
        const pegar = !part && !!tk && (tk.type === "list" || (tk.type === "paragraph" && !((tk as Tokens.Paragraph).tokens.length === 1 && (tk as Tokens.Paragraph).tokens[0].type === "strong")));
        const siguiente = pegar && tk ? block(tk) : null;
        out.push({
          part: !!part,
          header: !!part,
          breakBefore: resumenEnHoja && text === "Resumen",
          space: part ? 0 : text === "De dónde salen los números" ? 14 : 34,
          node: (
          <h2 key={k()} style={{ margin: 0, fontSize: "inherit", fontWeight: "inherit", display: "flex", flexDirection: "column" }}>
            <View id={idDeSeccion(text, part)} style={{ marginTop: innerTop, marginBottom: 14 }}>
              {part ? (
                <Span style={{ fontFamily: SANS, fontSize: 9.5, fontWeight: 500, color: ink.secondary, marginBottom: 8 }}>
                  {part.kicker}
                </Span>
              ) : null}
              <Span style={{ fontFamily: SANS, fontSize: 22, fontWeight: 600, lineHeight: 1.15, letterSpacing: "-0.015em" }}>
                {part ? part.title : text}
              </Span>
            </View>
          </h2>
          ),
        });
        if (siguiente) {
          const u = out[out.length - 1];
          u.node = <KeepTogether key={k()}>{u.node}{siguiente}</KeepTogether>;
          i = sig;
        }
        continue;
      }

      if (h.depth === 3) {
        const m = /^(\d\.\d+)\s+(.*)$/.exec(text);
        // Espacio arriba unas tres veces el de abajo: el título pertenece a lo que le sigue.
        let j = i + 1;
        while (j < tokens.length && tokens[j].type === "space") j++;
        const next = j < tokens.length ? block(tokens[j]) : null;
        inHeader = false;
        out.push({ space: 26, node: (
          <KeepTogether key={k()} style={{ marginTop: PAGINAR ? 0 : 26 }}>
            <View id={m ? "m" + m[1].replace(".", "-") : undefined} style={{ flexDirection: "row", gap: 12, marginBottom: 9 }}>
              {m ? (
                <Span style={{ fontFamily: SANS, fontSize: 10, fontWeight: 500, color: ink.secondary, width: 26, marginTop: 2 }}>
                  {m[1]}
                </Span>
              ) : null}
              <Span style={{ fontFamily: SANS, fontSize: 12.5, fontWeight: 600, lineHeight: 1.25, flex: 1 }}>{m ? m[2] : text}</Span>
            </View>
            <View style={{ paddingLeft: m ? 38 : 0 }}>{next}</View>
          </KeepTogether>
        ) });
        if (next) i = j;
        continue;
      }
      continue;
    }

    // Un título en negrita seguido de una lista (el resumen por etapa) viaja pegado a su lista.
    if (t.type === "paragraph" && (t as Tokens.Paragraph).tokens.length === 1 && (t as Tokens.Paragraph).tokens[0].type === "strong") {
      let j = i + 1;
      while (j < tokens.length && tokens[j].type === "space") j++;
      if (j < tokens.length && tokens[j].type === "list") {
        out.push({ space: 14, node: <KeepTogether key={k()}>{block(t)}{block(tokens[j])}</KeepTogether> });
        i = j;
        continue;
      }
    }

    const node = block(t);
    if (node) out.push({ node, space: 0, header: inHeader });
  }
  return out;
}

type Page = { header: Unit[]; items: Unit[]; used: number };

// Las hojas 1 y 2 usan los márgenes originales (superior 44 px, inferior del pie). Las siguientes
// tienen más margen arriba y abajo y un poco más a la derecha. El motor solo admite un margen para
// todo el documento, así que se fija el menor y el resto se logra con espacio dentro de cada hoja.
const HOJAS_MARGEN_ORIGINAL = 2;
const EXTRA_DERECHA = 10; // px
const NUEVO_TOP = 64;
const NUEVO_BOTTOM = 72;
const ORIGINAL_TOP = 44;

// Mide cada bloque, los reparte en hojas y arma cada hoja con una altura fija:
// encabezado arriba, contenido abajo y el espacio libre en el medio.
async function paginate(units: Unit[], fonts: Awaited<ReturnType<typeof googleFonts>>, bottomOriginal: number) {
  const wrap = (n: ReactNode, width: number) => (
    <PdfcnThemeProvider theme={scandinavianTheme}>
      <View style={{ width: `${width}px`, color: ink.primary }}>{n}</View>
    </PdfcnThemeProvider>
  );
  const anchoOriginal = CONTENT_W;
  const anchoNuevo = CONTENT_W - EXTRA_DERECHA;
  const hOriginal: number[] = [];
  const hNuevo: number[] = [];
  for (const u of units) {
    hOriginal.push((await measure(wrap(u.node, anchoOriginal), { size: "a4", fonts })).height);
    hNuevo.push((await measure(wrap(u.node, anchoNuevo), { size: "a4", fonts })).height);
  }

  const alto0 = PAGE_H - ORIGINAL_TOP - bottomOriginal - SAFETY; // alto de la hoja con margen original
  const padTop = NUEVO_TOP - ORIGINAL_TOP;
  const padBottom = NUEVO_BOTTOM - bottomOriginal;
  const capacidad = (idx: number) => (idx < HOJAS_MARGEN_ORIGINAL ? alto0 : alto0 - padTop - padBottom);
  const altoDe = (i: number, idx: number) => (idx < HOJAS_MARGEN_ORIGINAL ? hOriginal[i] : hNuevo[i]);

  const pages: Page[] = [];
  let cur: Page | null = null;
  const nueva = () => pages.push((cur = { header: [], items: [], used: 0 }));
  units.forEach((u, i) => {
    if (!cur || u.part || u.breakBefore) nueva();
    let h = altoDe(i, pages.length - 1);
    if (u.header) {
      cur!.header.push(u);
      cur!.used += h;
      return;
    }
    const gap = cur!.items.length ? u.space : 0;
    if (cur!.used + gap + h > capacidad(pages.length - 1)) {
      nueva();
      h = altoDe(i, pages.length - 1);
      cur!.items.push(u);
      cur!.used += h;
      return;
    }
    cur!.items.push(u);
    cur!.used += gap + h;
  });
  console.error(`hojas planeadas: ${pages.length}`);

  return (
    <PdfcnThemeProvider theme={scandinavianTheme}>
      <View style={{ color: ink.primary }}>
        {pages.map((pg, idx) => {
          const original = idx < HOJAS_MARGEN_ORIGINAL;
          const libre = capacidad(idx) - pg.used;
          const hasHeader = pg.header.length > 0;
          // Sin encabezado, repartir el sobrante entre los bloques solo si es muy chico: una hoja con aire queda arriba.
          const reparte = hasHeader || libre <= 60;
          const itemNodes = pg.items.map((u, j) => (
            <View key={k()} style={{ marginTop: j === 0 ? 0 : u.space }}>
              {u.node}
            </View>
          ));
          const contenido = (
            <View
              key={k()}
              style={{
                height: `${capacidad(idx)}px`,
                justifyContent: reparte ? "space-between" : "flex-start",
              }}
            >
              {hasHeader ? <View>{pg.header.map((u) => u.node)}</View> : null}
              {hasHeader ? <View>{itemNodes}</View> : itemNodes}
            </View>
          );
          return (
            <View
              key={k()}
              style={{
                height: `${alto0}px`,
                ...(idx > 0 ? { breakBefore: "page" } : {}),
              }}
            >
              {original ? (
                contenido
              ) : (
                <View style={{ marginTop: `${padTop}px`, marginRight: `${EXTRA_DERECHA}px` }}>{contenido}</View>
              )}
            </View>
          );
        })}
      </View>
    </PdfcnThemeProvider>
  );
}

async function main() {
  const md = (await readFile(INPUT, "utf8")).trim() + "\n";
  const tokens = marked.lexer(md);

  const first = tokens.findIndex((t) => t.type === "heading" && (t as Tokens.Heading).depth === 1);
  const title = decode((tokens[first] as Tokens.Heading).text);
  const after = tokens.slice(first + 1);
  const firstH2 = after.findIndex((t) => t.type === "heading");
  const leadToken = after.slice(0, firstH2).find((t) => t.type === "paragraph") as Tokens.Paragraph | undefined;
  const lead = leadToken ? plain(leadToken.tokens) : "";
  const rest = after.filter((t) => t !== leadToken);

  // Índice de la portada: todas las secciones de nivel 2. Con más de una etapa, la portada
  // lleva solo título, frase e índice al pie, y el resumen empieza en la hoja siguiente.
  const toc: Toc = [];
  for (const t of rest) {
    if (t.type === "heading" && (t as Tokens.Heading).depth === 2) {
      const text = decode((t as Tokens.Heading).text);
      const part = splitPart(text);
      toc.push({ kicker: part ? part.kicker : "", title: part ? part.title : text, id: idDeSeccion(text, part) });
    }
  }
  const etapas = toc.filter((e) => /^Etapa \d+$/.test(e.kicker)).length;
  const portadaAparte = PAGINAR && etapas > 1;

  const fonts = await googleFonts([
    { name: "Inter", weight: [400, 500, 600] },
    { name: "JetBrains Mono", weight: [400], generic: "monospace" },
  ]);

  // PIE_SIMPLE=1: pie solo con el número de página (lo usa parte-1.sh).
  const pieSimple = process.env.PIE_SIMPLE === "1";
  const footer = (
    <PdfcnThemeProvider theme={scandinavianTheme}>
      <View
        style={{
          flexDirection: "row",
          justifyContent: pieSimple ? "flex-end" : "space-between",
          width: "100%",
          paddingLeft: MARGIN_X * 0.75,
          paddingRight: MARGIN_X * 0.75,
          paddingTop: 14,
          paddingBottom: 14,
        }}
      >
        {pieSimple ? null : <Span style={{ fontFamily: SANS, fontSize: 8, color: ink.tertiary }}>{title}</Span>}
        <View style={{ width: 80 }}>
          <PageNumber format={pieSimple ? "{page}" : "{page} / {total}"} align="right" size="xs" muted />
        </View>
      </View>
    </PdfcnThemeProvider>
  );

  // Margen inferior original: lo que ocupa el pie (el motor lo calcula con "auto", nunca menos de 37,8 px).
  const bottomOriginal = Math.max(37.8, Math.ceil((await measure(footer, { size: "a4", fonts })).height));

  const units: Unit[] = [
    { node: <Cover title={title} lead={lead} />, space: 0, header: true, part: true },
    ...(portadaAparte ? [{ node: <Indice toc={toc} />, space: 0 }] : []),
    ...buildBody(rest, portadaAparte),
  ];

  const doc = PAGINAR ? await paginate(units, fonts, bottomOriginal) : (
    <PdfcnThemeProvider theme={scandinavianTheme}>
      <View style={{ color: ink.primary }}>
        {units.flatMap((u) => (u.part && u !== units[0] ? [<PageBreak key={k()} />, u.node] : [u.node]))}
      </View>
    </PdfcnThemeProvider>
  );

  const pdf = await render(doc, {
    size: "a4",
    margin: { top: MARGIN_TOP, bottom: PAGINAR ? bottomOriginal : "auto", left: MARGIN_X, right: MARGIN_X },
    footer,
    fonts,
    outline: true,
    lang: "es",
    metadata: {
      title,
      description: process.env.DESCRIPCION ?? title,
    },
  });
  await writeFile(OUTPUT, pdf);
  console.log(`PDF: ${pdf.length} bytes`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
