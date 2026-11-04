"""Mide el desfase entre subtítulos y la voz real del audio (VAD), por tercios de la película.

  check.py <audio.wav 16k mono> <sub.srt>...
Imprime el mejor desfase por tramo y un veredicto: SINCRONIZADO si |desfase| <= 0.2 s en los tres.
"""
import re, sys, wave
import numpy as np, webrtcvad

w = wave.open(sys.argv[1]); sr = w.getframerate(); data = w.readframes(w.getnframes())
vad = webrtcvad.Vad(3); fl = int(sr * 0.01) * 2
speech = np.array([vad.is_speech(data[i:i + fl], sr) for i in range(0, len(data) - fl, fl)], dtype=float)
N = len(speech)

def ts(s):
    return sum(float(x) * m for x, m in zip(s.replace(",", ".").split(":"), (3600, 60, 1)))

def cues(path):
    t = open(path, encoding="utf-8-sig").read()
    c = [(ts(a), ts(b)) for a, b in re.findall(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", t)]
    return [x for x in c if x[0] > 30 and x[1] - x[0] < 10]  # fuera anuncios y carteles largos

for path in sys.argv[2:]:
    c = cues(path); print("==", path, len(c), "líneas")
    ok = True
    for seg in np.array_split(np.array(c), 3):
        best = (-1, 0)
        for off in np.arange(-15, 15.01, 0.1):
            m = np.zeros(N)
            for a, b in seg:
                m[max(int((a + off) * 100), 0):min(int((b + off) * 100), N)] = 1
            best = max(best, (m @ speech / max(m.sum(), 1), round(off, 1)))
        ok &= abs(best[1]) <= 0.2
        print(f"  {seg[0][0]/60:5.0f}-{seg[-1][0]/60:4.0f} min: desfase {best[1]:+.1f} s (coincidencia {best[0]:.3f})")
    print("  SINCRONIZADO" if ok else "  DESINCRONIZADO")
