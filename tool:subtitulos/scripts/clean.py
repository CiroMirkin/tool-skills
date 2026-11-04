"""Quita las líneas de publicidad de un .srt y renumera.  clean.py <entrada> <salida>"""
import re, sys
blocks = re.split(r"\n\s*\n", open(sys.argv[1], encoding="utf-8-sig").read().replace("\r", "").strip())
ads = re.compile(r"opensubtitles|osdb\.link|getray|subdl|addic7ed|Watch Online|Anuncie su producto|www\.\S+\.(com|org|net|app|link)", re.I)
keep = [b for b in blocks if not ads.search(b)]
out = ["\n".join([str(i)] + b.split("\n")[1:]) for i, b in enumerate(keep, 1)]
open(sys.argv[2], "w", encoding="utf-8").write("\n\n".join(out) + "\n")
print(f"{len(blocks)} -> {len(keep)} bloques ({len(blocks) - len(keep)} anuncios quitados)")
