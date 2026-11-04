"""Alineación por tramos (estilo alass): un desfase por línea con DP, penalizando los cambios.
Para cuando el subtítulo viene de un master con cortes distintos y ffsubsync (un único desfase
más factor de velocidad) deja tramos desfasados. Usar sobre el .srt SIN pasar por ffsubsync.

  piecewise.py <audio.wav 16k mono> <entrada.srt> <salida.srt> [desfase_min=-8 desfase_max=4 penalización_salto=400]
Imprime el desfase aplicado cada ~10 min, para comprobar que la trayectoria es coherente.
"""
import re, sys, wave
import numpy as np, webrtcvad

wav, src, dst = sys.argv[1:4]
lo, hi, P = (float(x) for x in (sys.argv[4:7] or (-8, 4, 400)))
w = wave.open(wav); sr = w.getframerate(); data = w.readframes(w.getnframes())
vad = webrtcvad.Vad(3); fl = int(sr * 0.01) * 2
speech = np.array([vad.is_speech(data[i:i + fl], sr) for i in range(0, len(data) - fl, fl)], dtype=float)
cs = np.concatenate([[0], np.cumsum(speech - 0.4)]); N = len(speech)

def ts(s):
    return sum(float(x) * m for x, m in zip(s.replace(",", ".").split(":"), (3600, 60, 1)))
def fmt(t):
    t = max(t, 0); ms = int(round(t * 1000)); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"

text = open(src, encoding="utf-8-sig").read()
pat = re.compile(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)")
cues = [(ts(a), ts(b)) for a, b in pat.findall(text)]
offs = np.round(np.arange(lo, hi + 1e-9, 0.05), 2); K = len(offs)
S = np.zeros((len(cues), K))
for i, (a, b) in enumerate(cues):
    for k, o in enumerate(offs):
        x, y = int(np.clip((a + o) * 100, 0, N)), int(np.clip((b + o) * 100, 0, N))
        S[i, k] = cs[y] - cs[x]
# DP: mantener desfase (gratis), moverse ±1 paso (deriva suave, coste bajo) o saltar (coste P)
D = S[0].copy(); back = np.zeros((len(cues), K), dtype=int)
for i in range(1, len(cues)):
    best = D.argmax()
    cand = np.stack([D, np.r_[-1e18, D[:-1]] - 5, np.r_[D[1:], -1e18] - 5, np.full(K, D[best] - P)])
    ch = cand.argmax(0)
    back[i] = np.where(ch == 0, np.arange(K), np.where(ch == 1, np.arange(K) - 1, np.where(ch == 2, np.arange(K) + 1, best)))
    D = cand.max(0) + S[i]
k = int(D.argmax()); path = [k]
for i in range(len(cues) - 1, 0, -1):
    k = back[i, k]; path.append(k)
path = offs[path[::-1]]
last = -1e9
for (a, _), o in zip(cues, path):
    if a - last >= 600:
        print(f"  {a/60:5.0f} min: desfase {o:+.2f}"); last = a
it = iter(path)
out = pat.sub(lambda m: (lambda o: f"{fmt(ts(m[1]) + o)} --> {fmt(ts(m[2]) + o)}")(next(it)), text)
open(dst, "w", encoding="utf-8").write(out)
