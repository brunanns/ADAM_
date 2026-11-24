# Gera os sons PLACEHOLDER do ADAM (sintetizados por código, sem copyright).
# Uso:  python gerar_audio.py        (precisa de numpy, scipy e ffmpeg)
# Para usar sons "de verdade", é só substituir os arquivos da pasta audio/ pelos seus, com os mesmos nomes.
import os, subprocess, wave
import numpy as np
from scipy.signal import butter, lfilter

SR = 44100
rng = np.random.default_rng(7)
PASTA = "audio"


def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def tempo(n): return np.arange(n) / SR
def lp(x, fc): b, a = butter(2, min(fc, SR / 2 - 100) / (SR / 2)); return lfilter(b, a, x)
def hp(x, fc): b, a = butter(2, fc / (SR / 2), "high"); return lfilter(b, a, x)
def serra(f, n): return 2 * ((f * tempo(n)) % 1) - 1
def ruido(n): return rng.uniform(-1, 1, n)


def salvar_wav(nome, x, pico=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * pico
    with wave.open(os.path.join(PASTA, nome), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# ---------------- efeitos ----------------
def efeito_tiro():
    n = int(0.14 * SR); t = tempo(n)
    f = 1500 * np.exp(-t * 14) + 250
    x = (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5)
    return lp(x * np.exp(-t * 22), 7000), 0.45

def efeito_dano():
    n = int(0.3 * SR); t = tempo(n)
    f = 110 * np.exp(-t * 6) + 45
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.9 + lp(ruido(n), 1800) * 0.7
    return x * np.exp(-t * 13), 0.75

def efeito_explosao():
    n = int(1.0 * SR); t = tempo(n)
    x = lp(ruido(n), 900) * np.exp(-t * 4) + lp(ruido(n), 4000) * np.exp(-t * 12) * 0.6
    x += np.sin(2 * np.pi * np.cumsum(80 * np.exp(-t * 3) + 35) / SR) * np.exp(-t * 5) * 0.9
    return x, 0.9

def efeito_item():
    n = int(0.28 * SR); t = tempo(n); x = np.zeros(n)
    for ini, f in ((0.0, 880), (0.09, 1320)):
        i = int(ini * SR); m = n - i; tt = tempo(m)
        x[i:] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 14)
    return x, 0.6

def efeito_nivel():
    n = int(0.9 * SR); x = np.zeros(n)
    for k, m in enumerate((72, 76, 79, 84)):
        i = int(k * 0.1 * SR); tt = tempo(n - i)
        x[i:] += (np.sin(2 * np.pi * midi(m) * tt) + 0.25 * serra(midi(m), n - i)) * np.exp(-tt * 6)
    return lp(x, 6000), 0.7


# ---------------- música ----------------
def faixa(bpm, compassos, acordes, camadas):
    """camadas: dict com os instrumentos; cada um tem 'desde' = compasso em que entra (dá evolução à música)."""
    beat = 60 / bpm; barra = 4 * beat; L = int(compassos * barra * SR); buf = np.zeros(L)
    passo = beat / 4

    def colocar(sig, inicio):
        s = int(inicio * SR) % L; n = min(len(sig), L)
        buf[(np.arange(n) + s) % L] += sig[:n]

    def pad(notas, dur, corte, nivel):
        n = int((dur + 1.0) * SR); t = tempo(n); x = np.zeros(n)
        for m in notas:
            for d in (0.997, 1.003):
                x += serra(midi(m) * d, n)
        a = min(0.8, dur * 0.4)
        env = np.minimum(t / a, 1) * np.exp(-np.maximum(t - dur, 0) * 4)
        return lp(x, corte) * env * nivel / len(notas)

    def baixo(m, dur, corte, nivel, seca=4):
        n = int(dur * SR); t = tempo(n)
        x = serra(midi(m), n) * 0.7 + np.sin(2 * np.pi * midi(m) * t)
        return lp(x, corte) * np.exp(-t * seca) * nivel

    def bumbo(nivel):
        n = int(0.25 * SR); t = tempo(n)
        return np.sin(2 * np.pi * np.cumsum(130 * np.exp(-t * 25) + 42) / SR) * np.exp(-t * 11) * nivel

    def caixa(nivel, metal=False):
        n = int(0.2 * SR); t = tempo(n)
        r = hp(ruido(n), 1800 if not metal else 3500) * np.exp(-t * (18 if not metal else 9))
        return (r + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.5) * nivel

    def chimbal(nivel):
        n = int(0.06 * SR); t = tempo(n)
        return hp(ruido(n), 6000) * np.exp(-t * 55) * nivel

    def nota(m, dur, nivel, forma="quad", corte=3000):
        n = int(dur * SR); t = tempo(n)
        x = (np.sign(np.sin(2 * np.pi * midi(m) * t)) * 0.5 if forma == "quad" else serra(midi(m), n) * 0.6)
        return lp(x, corte) * np.exp(-t * 7) * nivel

    def sino(m, nivel):
        n = int(2.0 * SR); t = tempo(n)
        x = np.sin(2 * np.pi * midi(m) * t) + 0.4 * np.sin(2 * np.pi * midi(m) * 2.76 * t)
        return x * np.exp(-t * 2.2) * nivel

    for c in range(compassos):
        acorde = acordes[c % len(acordes)]
        raiz = acorde[0] - 12
        t0 = c * barra
        for nome, p in camadas.items():
            if c < p.get("desde", 0): continue
            if nome == "pad":
                colocar(pad(acorde, barra, p["corte"], p["nivel"]), t0)
            elif nome == "sub":
                colocar(baixo(raiz - 12, barra, 200, p["nivel"], seca=0.8), t0)
            elif nome == "sino":
                for b in p["batidas"]:
                    colocar(sino(acorde[(b + c) % len(acorde)] + 24, p["nivel"]), t0 + b * beat)
            else:
                for s, ch in enumerate(p["padrao"]):
                    if ch == ".": continue
                    ti = t0 + s * passo
                    acento = 1.0 if ch == "X" else 0.7
                    if nome == "bumbo": colocar(bumbo(p["nivel"] * acento), ti)
                    elif nome == "caixa": colocar(caixa(p["nivel"] * acento, p.get("metal", False)), ti)
                    elif nome == "chimbal": colocar(chimbal(p["nivel"] * acento), ti)
                    elif nome == "baixo": colocar(baixo(raiz, passo * 2, p["corte"], p["nivel"] * acento), ti)
                    elif nome == "arp":
                        m = acorde[(s // p.get("cada", 1)) % len(acorde)] + 12 * p.get("oitava", 1)
                        colocar(nota(m, passo * 1.5, p["nivel"] * acento, p.get("forma", "quad"), p.get("corte", 3000)), ti)
                        if p.get("eco"):
                            colocar(nota(m, passo * 1.5, p["nivel"] * acento * 0.45, p.get("forma", "quad"), p.get("corte", 3000)), ti + passo * 3)
    return buf


def salvar_ogg(nome, x):
    x = np.tanh(x * 1.2); x = x / (np.max(np.abs(x)) + 1e-9) * 0.8
    tmp = os.path.join(PASTA, "_tmp.wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c:a", "libvorbis", "-q:a", "4",
                    os.path.join(PASTA, nome)], check=True)
    os.remove(tmp)


Am, F, C, G = [57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]
Dm, Bb, Gm, A_ = [50, 57, 62], [46, 53, 58], [43, 55, 58], [45, 57, 61]
Em, C2, G2, D2 = [52, 59, 64], [48, 55, 60], [55, 59, 62], [50, 57, 62]
Cm, Ab, Bb2, Gm2 = [48, 55, 60], [44, 51, 56], [46, 53, 58], [43, 50, 55]
Bm, G3, D3, A3 = [47, 54, 59], [43, 50, 55], [50, 57, 62], [45, 52, 57]
Dm4, Bb4, C4, A4 = [50, 57, 62], [46, 53, 58], [48, 55, 60], [45, 57, 61]

MUSICAS = {
    "musica_menu.ogg": (70, 16, [Am, F, C, G], {
        "pad": dict(corte=1600, nivel=0.7), "sub": dict(nivel=0.5, desde=2),
        "sino": dict(batidas=[0, 2], nivel=0.25, desde=4)}),
    "musica_cena.ogg": (62, 16, [Dm, Bb, Gm, A_], {
        "pad": dict(corte=1100, nivel=0.8), "sub": dict(nivel=0.6),
        "sino": dict(batidas=[1], nivel=0.18, desde=6)}),
    "musica_fase1.ogg": (92, 16, [Em, C2, G2, D2], {
        "pad": dict(corte=1300, nivel=0.6), "sub": dict(nivel=0.4),
        "baixo": dict(padrao="X.x.x.x.X.x.x.x.", corte=500, nivel=0.5, desde=2),
        "bumbo": dict(padrao="X.......x.......", nivel=0.6, desde=4),
        "chimbal": dict(padrao="..x...x...x...x.", nivel=0.25, desde=6),
        "sino": dict(batidas=[0], nivel=0.2, desde=8)}),
    "musica_fase2.ogg": (104, 16, [Cm, Ab, Bb2, Gm2], {
        "pad": dict(corte=900, nivel=0.6),
        "baixo": dict(padrao="X.xxX.x.X.xxX.x.", corte=450, nivel=0.6),
        "bumbo": dict(padrao="X..x..x.X..x..x.", nivel=0.7, desde=2),
        "caixa": dict(padrao="....X.......X...", nivel=0.5, desde=4, metal=True),
        "chimbal": dict(padrao="x.x.x.x.x.x.x.x.", nivel=0.2, desde=8)}),
    "musica_fase3.ogg": (116, 16, [Bm, G3, D3, A3], {
        "pad": dict(corte=1500, nivel=0.5),
        "bumbo": dict(padrao="X...X...X...X...", nivel=0.65, desde=2),
        "chimbal": dict(padrao="..x...x...x...x.", nivel=0.25, desde=2),
        "baixo": dict(padrao="x.x.x.x.x.x.x.x.", corte=600, nivel=0.5, desde=4),
        "arp": dict(padrao="xxxxxxxxxxxxxxxx", nivel=0.28, forma="quad", corte=2800, oitava=1, eco=True, desde=4)}),
    "musica_boss.ogg": (140, 16, [Dm4, Bb4, C4, A4], {
        "pad": dict(corte=2200, nivel=0.55),
        "baixo": dict(padrao="XxxxXxxxXxxxXxxx", corte=700, nivel=0.65),
        "bumbo": dict(padrao="X..xX..xX..xX.x.", nivel=0.8),
        "caixa": dict(padrao="....X.......X..x", nivel=0.6),
        "chimbal": dict(padrao="xxxxxxxxxxxxxxxx", nivel=0.18, desde=2),
        "arp": dict(padrao="xxxxxxxxxxxxxxxx", nivel=0.3, forma="serra", corte=3500, oitava=2, desde=4)}),
}

if __name__ == "__main__":
    os.makedirs(PASTA, exist_ok=True)
    for nome, fn in (("tiro.wav", efeito_tiro), ("dano.wav", efeito_dano), ("explosao.wav", efeito_explosao),
                     ("item.wav", efeito_item), ("nivel.wav", efeito_nivel)):
        x, pico = fn()
        salvar_wav(nome, x, pico)
        print("ok", nome)
    for nome, (bpm, comp, acordes, camadas) in MUSICAS.items():
        salvar_ogg(nome, faixa(bpm, comp, acordes, camadas))
        print("ok", nome)
