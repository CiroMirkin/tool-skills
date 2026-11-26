import { minimalTheme } from "@/components/pdf/theme-minimal";
import type { PdfcnTheme } from "@/components/pdf/theme-types";

// Escala de tinta: negro con alfa sobre blanco, sin grises tintados.
export const ink = {
  primary: "#000000",
  secondary: "rgba(0, 0, 0, 0.64)",
  // Los datos reales no bajan de 56 %: el 44 % de la skill no llega a 4,5:1 sobre blanco.
  tertiary: "rgba(0, 0, 0, 0.56)",
  border: "rgba(0, 0, 0, 0.10)",
  borderStrong: "rgba(0, 0, 0, 0.18)",
  wash: "rgba(0, 0, 0, 0.04)",
};

export const SANS = "Inter";
export const MONO = "'JetBrains Mono', monospace";

export const scandinavianTheme: PdfcnTheme = {
  ...minimalTheme,
  name: "scandinavian",
  colors: {
    ...minimalTheme.colors,
    accent: ink.primary,
    background: "#ffffff",
    border: ink.border,
    foreground: ink.primary,
    info: ink.primary,
    muted: ink.wash,
    mutedForeground: ink.secondary,
    primary: ink.primary,
  },
  spacing: {
    ...minimalTheme.spacing,
    componentGap: 16,
    paragraphGap: 8,
    sectionGap: 32,
  },
  typography: {
    body: { fontFamily: SANS, fontSize: 10, lineHeight: 1.55 },
    heading: {
      ...minimalTheme.typography.heading,
      fontFamily: SANS,
      fontSize: { h1: 32, h2: 22, h3: 12.5, h4: 11, h5: 10, h6: 10 },
      fontWeight: 600,
      lineHeight: 1.15,
    },
  },
};
