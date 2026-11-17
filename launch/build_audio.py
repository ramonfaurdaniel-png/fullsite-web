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

# ---------------- ARRANGEMENT ----------------
# 0-5: tension — clock ticks + drone
n = int(SR * 7); tt = np.arange(n) / SR
drone = (np.sin(2 * np.pi * 55 * tt) + 0.5 * np.sin(2 * np.pi * 82.4 * tt)) * np.minimum(1, tt / 3) * 0.12
drone *= np.where(tt < 5, 1, np.maximum(0, 1 - (tt - 5) / 0.3))
add(drone, 0)
for i in range(10):
    add(tick(), i * 0.5, 0.5 if i % 2 else 0.8, 0.3 if i % 2 else -0.3)
for t0 in (1.0, 1.5, 2.0):
    add(thud(), t0, 0.9)
add(whoosh(0.5), 2.1, 0.6)
add(thud(), 2.55, 1.0)
for i, t0 in enumerate([2.7, 2.88, 3.06, 3.24, 3.42]):
    add(tick(), t0, 0.7, (-1) ** i * 0.6)
for i in range(24):
    add(tick(), 3.6 + i * 0.05, 0.25, 0)
add(blip(520), 5.0, 0.6)
add(riser(2.0), 5.0, 0.9)
add(impact(), 7.0, 1.0)
add(whoosh(0.6, False), 7.4, 0.5)


def groove(t_start, t_end, energy=1.0, bass=True):
    t = t_start
    i = 0
    while t < t_end - 1e-6:
        b = i % 4
        add(kick(), t, 0.9)
        if b in (1, 3): add(clap(), t, 0.55 * energy)
        add(hat(), t + 0.25, 0.4 * energy, 0.25)
        if energy > 1.05 and b == 3: add(hat(True), t + 0.25, 0.3, -0.25)
        add(hat(), t, 0.18 * energy, -0.25)
        bar = int((t + 1e-6) // 2.0) % 4
        if bass:
            root = PROG[bar][0]
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
        bar = int((t + 1e-6) // 2.0) % 4
        notes = PROG[bar][1]
        m = notes[[0, 2, 1, 2][i % 4]] + 12
        add(note(hz(m), 0.6, 'pluck'), t, gain, (-1) ** i * 0.4)
        t += 0.25; i += 1

# brand reveal: pads only, then groove from Connect title
pads(7.0, 11.0, 0.8)
add(riser(1.0), 10.0, 0.6)
groove(11.0, 32.4, 1.0)
pads(11.0, 32.4, 0.6)
plucks(17.0, 22.0, 0.7)       # phone scene sparkle
plucks(26.0, 32.0, 0.6)       # mosaic
for t0 in (12.3, 16.8, 25.7):
    add(whoosh(0.5), t0, 0.7)
add(whoosh(0.45), 23.95, 0.9)  # whip pan
for t0 in (18.3, 19.2, 20.2, 21.2):
    add(blip(), t0, 0.8)
for t0 in (27.0, 27.5, 28.0, 28.6, 29.9, 30.4, 30.9):
    add(tick(), t0, 0.6)
# offline: everything drops, glitches
for k in range(9):
    add(glitch(rng.uniform(0.04, 0.12)), 33.2 + k * 0.09, 0.8, rng.uniform(-0.7, 0.7))
add(riser(0.8), 33.4, 0.7)
add(impact(), 34.2, 0.95)
groove(34.2, 44.6, 1.15)
pads(34.2, 44.6, 0.6)
plucks(39.0, 44.6, 0.7)
for t0 in (36.4, 36.9, 37.4):
    add(thud(), t0, 0.6)
for t0 in (41.4, 41.9, 42.4, 42.9):
    add(tick(), t0, 0.7)
add(riser(0.6), 44.6, 0.8)
add(impact(), 45.2, 1.0)
# final resolve chord C add9, long
for m in (48, 55, 60, 62, 64, 67):
    add(note(hz(m), 5.8, 'pad'), 45.2, 1.3, rng.uniform(-0.6, 0.6))
for i, m in enumerate((72, 76, 79, 84)):
    add(note(hz(m), 1.5, 'pluck'), 46.2 + i * 0.25, 0.6, (-1) ** i * 0.4)

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
