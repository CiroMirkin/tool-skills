"""Busca y descarga subtítulos de la API REST antigua de OpenSubtitles (sin clave).

  search.py list <imdb_id> [idiomas=spa]      -> candidatos ordenados por descargas
  search.py get <IDSubtitleFile> <dir_salida> <imdb_id> [idiomas=spa] -> descarga a UTF-8
"""
import gzip, json, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0", "X-User-Agent": "TemporaryUserAgent"}

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

def search(imdb, langs):
    num = imdb.lower().removeprefix("tt").lstrip("0")
    subs = []
    for lang in langs.split(","):
        subs += json.loads(fetch(f"https://rest.opensubtitles.org/search/imdbid-{num}/sublanguageid-{lang}"))
    return sorted(subs, key=lambda s: -int(s["SubDownloadsCnt"]))

if sys.argv[1] == "list":
    for s in search(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "spa"):
        print(s["IDSubtitleFile"], s["SubLanguageID"], s["SubDownloadsCnt"], s["SubEncoding"], s["MovieReleaseName"], "|", s["SubFileName"], sep="\t")
else:
    sid, out = sys.argv[2], sys.argv[3]
    # El enlace de descarga lleva un token "vrf" por archivo, así que se repite la búsqueda.
    s = next(x for x in search(sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "spa") if x["IDSubtitleFile"] == sid)
    raw = gzip.decompress(fetch(s["SubDownloadLink"]))
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode(s["SubEncoding"] or "cp1252", errors="replace")
    path = f"{out}/{sid}.srt"
    open(path, "w", encoding="utf-8").write(text.replace("\r", ""))
    print(path)
