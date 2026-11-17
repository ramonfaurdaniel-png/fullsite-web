"""Soundtrack synth for the Fullsite launch video (120 BPM, 51 s).
Pure numpy. Every hit lines up with a cut in fullsite-launch.html.
Usage: python3 build_audio.py out.wav
"""
import sys, wave
import numpy as np

SR = 48000
DUR = 51.0
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)
BEAT = 0.5


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def env(n, a=0.002, d=0.2, curve=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-5)) * np.exp(-curve * np.maximum(0, t - a) / d)
    return e


def lp_fft(x, cutoff, hp=0):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (f / cutoff) ** 4)
    if hp: m *= 1 - 1 / (1 + (f / hp) ** 4)
    return np.fft.irfft(X * m, len(x))


def kick(big=False):
    n = int(SR * (0.9 if big else 0.42))
    t = np.arange(n) / SR
    f = 42 + (160 if big else 120) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env(n, 0.001, 0.5 if big else 0.22, 3)
    click = rng.standard_normal(n) * np.exp(-t * 400) * 0.25
    return np.tanh((s + click) * 1.6)


def clap():
    n = int(SR * 0.3); t = np.arange(n) / SR
    nz = lp_fft(rng.standard_normal(n), 3500, 900)
    e = np.zeros(n)
    for o in (0, 0.011, 0.022):
        e += np.where(t >= o, np.exp(-(t - o) * 60), 0) * (t >= o)
    e += np.exp(-t * 14) * 0.4
    return nz * e * 0.5


def hat(open_=False):
    n = int(SR * (0.25 if open_ else 0.06)); t = np.arange(n) / SR
    nz = lp_fft(rng.standard_normal(n), 16000, 7000)
    return nz * np.exp(-t * (14 if open_ else 70)) * 0.35


def tick():
    n = int(SR * 0.04); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * 0.5 + lp_fft(rng.standard_normal(n), 9000, 3000)) * np.exp(-t * 160) * 0.5


def thud():
    n = int(SR * 0.5); t = np.arange(n) / SR
    f = 38 + 110 * np.exp(-t * 18)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    return np.tanh(s * 2) * 0.9


def whoosh(d=0.6, up=True):
    n = int(SR * d); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    # sweep via chunked filtering
    out = np.zeros(n); ch = 1024
    for i in range(0, n, ch):
        k = i / n
        c = (300 + 9000 * (k if up else 1 - k) ** 2)
        seg = nz[max(0, i - ch): i + ch]
        f = lp_fft(seg, c, c * 0.25)
        out[i:i + ch] = f[min(i, ch): min(i, ch) + len(out[i:i + ch])]
    e = np.sin(np.pi * np.minimum(1, t / d)) ** 2
    return out * e * 0.6


def riser(d):
    n = int(SR * d); t = np.arange(n) / SR
    f = 110 * 2 ** (3 * t / d)
    s = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR))
    w = whoosh(d, True)
    return (s * 0.18 + w) * (t / d) ** 2


def impact():
    n = int(SR * 2.5); t = np.arange(n) / SR
    k = np.zeros(n); kk = kick(True); k[:len(kk)] = kk
    nz = lp_fft(rng.standard_normal(n), 5000, 200) * np.exp(-t * 3.5) * 0.45
    sub = np.sin(2 * np.pi * 36 * t) * np.exp(-t * 1.6) * 0.6
    return np.tanh((k + nz + sub) * 1.2)


def blip(f=1320):
    n = int(SR * 0.16); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 1.5 * t * (t < 0.06))
    return s * np.exp(-t * 30) * 0.35


def glitch(d=0.12):
    n = int(SR * d)
    s = np.sign(np.sin(2 * np.pi * rng.uniform(80, 900) * np.arange(n) / SR)) * 0.3
    s += rng.standard_normal(n) * 0.2
    s = np.round(s * 4) / 4
    return s * env(n, 0.001, d, 2)


def note(freq, d, kind='pad'):
    n = int(SR * d); t = np.arange(n) / SR
    if kind == 'pad':
        s = sum(np.sin(2 * np.pi * freq * m * t + rng.uniform(0, 6)) / m ** 1.3 for m in (1, 2, 3, 4))
        s += sum(np.sin(2 * np.pi * freq * (1 + dt) * t) for dt in (-0.004, 0.004)) * 0.5
        a = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.6)
        return s * a * 0.06
    if kind == 'bass':
        s = np.tanh(np.sin(2 * np.pi * freq * t) * 2.5 + 0.3 * np.sin(4 * np.pi * freq * t))
        return s * env(n, 0.004, d * 0.6, 3) * 0.35
    if kind == 'pluck':
        s = sum(np.sin(2 * np.pi * freq * m * t) * np.exp(-t * (6 + 4 * m)) / m for m in (1, 2, 3, 5))
        return s * 0.16


def hz(midi): return 440 * 2 ** ((midi - 69) / 12)

# chords per 2-second bar: Am  F  C  G  (roots in midi)
PROG = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]


def groove(t_start, t_end, energy=1.0, bass=True):
    t = t_start; i = 0
    while t < t_end - 1e-6:
        b = i % 4
        add(kick(), t, 0.9 * min(1, energy + 0.2))
        if b in (1, 3): add(clap(), t, 0.5 * energy)
        add(hat(), t + 0.25, 0.4 * energy, 0.25)
        if energy > 1.05 and b == 3: add(hat(True), t + 0.25, 0.3, -0.25)
        add(hat(), t, 0.18 * energy, -0.25)
        if bass:
            root = PROG[int((t + 1e-6) // 2.0) % 4][0]
            add(note(hz(root), 0.22, 'bass'), t + 0.25, 1.0)
        t += BEAT; i += 1


def pads(t_start, t_end, gain=1.0):
    t = t_start
    while t < t_end - 1e-6:
        bar = int((t + 1e-6) // 2.0) % 4
        d = min(2.0, t_end - t)
        for m in PROG[bar][1]:
            add(note(hz(m), d + 0.4, 'pad'), t, gain, rng.uniform(-0.5, 0.5))
        t += 2.0


def plucks(t_start, t_end, gain=1.0):
    t = t_start; i = 0
    while t < t_end - 1e-6:
        notes = PROG[int((t + 1e-6) // 2.0) % 4][1]
        m = notes[[0, 2, 1, 2][i % 4]] + 12
        add(note(hz(m), 0.6, 'pluck'), t, gain, (-1) ** i * 0.4)
        t += 0.25; i += 1

# ---------------- ARRANGEMENT (v3 timeline) ----------------
# soft intro pad + arp
pads(0.0, 6.0, 0.55)
plucks(0.5, 6.0, 0.35)
for t0 in (3.25, 3.55, 3.85, 4.15, 4.45):        # loss rows on receipt
    add(tick(), t0, 0.6, 0.2)
for i in range(20):
    add(tick(), 4.6 + i * 0.045, 0.18)          # counter
add(riser(1.2), 4.8, 0.6)
add(impact(), 6.0, 0.75)
add(blip(880), 6.35, 0.6)                       # square bounce
add(whoosh(0.6), 6.6, 0.55)
pads(6.0, 10.0, 0.6)
groove(7.0, 9.5, 0.7, bass=False)
add(blip(1320), 8.4, 0.4); add(blip(1560), 8.6, 0.4)
add(riser(0.5), 9.5, 0.7)
add(impact(), 10.0, 0.9)
# CONNECT (dark)
n2 = int(SR * 11); t2 = np.arange(n2) / SR
add(np.sin(2 * np.pi * 41.2 * t2) * np.minimum(1, t2 / 1.5) * np.minimum(1, (11 - t2) / 0.5) * 0.12, 10.0)
groove(11.0, 20.6, 1.0)
pads(10.0, 21.0, 0.55)
plucks(16.0, 20.6, 0.55)
add(whoosh(0.6), 13.9, 0.6)
for i in range(16):
    add(tick(), 14.7 + i * 0.06, 0.35, 0.3)     # typing
add(tick(), 15.8, 0.9)
for t0 in (16.0, 16.35, 16.7):
    add(blip(1100), t0, 0.55)
add(blip(1480), 19.5, 0.9); add(blip(1975), 19.62, 0.6)   # notification
add(whoosh(0.5), 20.55, 0.7)
add(impact(), 21.0, 0.8)
# POS (light)
groove(21.0, 34.6, 1.1)
pads(21.0, 35.0, 0.55)
plucks(21.0, 24.0, 0.5)
add(whoosh(0.5), 23.5, 0.6)
for t0 in (24.8, 25.3, 25.8, 26.7):
    add(tick(), t0, 0.9)
for i, m in enumerate((76, 79, 84)):
    add(note(hz(m), 0.8, 'pluck'), 26.9 + i * 0.07, 0.8)   # paid chime
add(whoosh(0.4), 27.35, 0.5)
for k in range(5):
    add(glitch(0.05), 28.9 + k * 0.08, 0.35)
for i, m in enumerate((72, 79)):
    add(note(hz(m), 0.8, 'pluck'), 30.2 + i * 0.08, 0.8)
add(whoosh(0.5), 30.5, 0.5)
add(riser(0.6), 34.4, 0.7)
add(impact(), 35.0, 0.85)
# TOGETHER
groove(35.0, 42.5, 1.15)
pads(35.0, 43.0, 0.6)
plucks(35.0, 42.5, 0.6)
for t0 in (36.0, 37.0, 38.0):
    add(tick(), t0, 0.8)
add(riser(0.6), 42.4, 0.8)
add(impact(), 43.0, 1.0)
add(blip(880), 43.4, 0.5)
for m in (48, 55, 60, 62, 64, 67):
    add(note(hz(m), 7.6, 'pad'), 43.0, 1.3, rng.uniform(-0.6, 0.6))
for i, m in enumerate((72, 76, 79, 84)):
    add(note(hz(m), 1.5, 'pluck'), 44.4 + i * 0.25, 0.6, (-1) ** i * 0.4)

# master: soft-clip, normalise, fade
mix = np.stack([L, R], 1)
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.89
fade = np.ones(N); fl = int(SR * 0.9); fade[-fl:] = np.linspace(1, 0, fl) ** 2
mix *= fade[:, None]
out = (mix * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print('ok')
