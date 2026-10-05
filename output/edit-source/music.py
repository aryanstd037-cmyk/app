# Original procedurally-synthesised track (no samples) -> 100% copyright-free.
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
DUR = 39.2
N = int(SR * DUR)
rng = np.random.default_rng(7)
BPM = 120
BEAT = 60 / BPM
DROP = 16.64              # "Toh aaj..." -> solution
FINALE = 35.10
END_HIT = 38.55
T0 = DROP - 9 * 2 * BEAT * 2 / 2  # grid origin so a bar line lands on DROP
T0 = DROP - np.ceil(DROP / (4 * BEAT)) * 4 * BEAT

L = np.zeros(N); R = np.zeros(N)

def lp(x, f, o=2):  return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2):  return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i+n] += sig[:n] * gain * l * 1.414
    R[i:i+n] += sig[:n] * gain * r * 1.414

def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e

def midi(m): return 440 * 2 ** ((m - 69) / 12)

def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune):
        ph = (t * f * (1 + d)) % 1
        out += 2 * ph - 1
    return out / 3

# ---------- instruments ----------
def kick(g=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t * 300) * 0.25
    return np.tanh((s + click) * 1.6) * g

def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR
    nz = bp(rng.standard_normal(n), 900, 3500)
    e = np.zeros(n)
    for k, off in enumerate((0, 0.011, 0.022)):
        e += np.where(t >= off, np.exp(-(t - off) * (180 if k < 2 else 22)), 0)
    return nz * e * 0.8

def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7500) * np.exp(-t * (14 if open_ else 70)) * 0.35

def pluck(m, dur=0.22, bright=4500):
    n = int(dur * SR); t = np.arange(n) / SR
    s = saw(midi(m), n, 0.004) + 0.5 * np.sign(np.sin(2 * np.pi * midi(m + 12) * t))
    return lp(s * env(n, 0.002, 0.09), bright) * 0.35

def bass(m, dur, cutoff=700):
    n = int(dur * SR); t = np.arange(n) / SR
    s = saw(midi(m), n, 0.003) * 0.7 + np.sin(2 * np.pi * midi(m) * t) * 0.6
    e = np.minimum(1, t / 0.005) * np.minimum(1, (dur - t) / 0.02)
    return lp(s * e, cutoff, 4) * 0.55

def pad(notes, dur, cutoff=2500):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(saw(midi(m), n, 0.006) for m in notes) / len(notes)
    e = np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.3)
    return lp(s * e, cutoff, 2) * 0.32

def sub(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    e = np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.3)
    return np.sin(2 * np.pi * midi(m) * t) * e * 0.5

# progressions (A minor)
dark = [(45, [57, 60, 64]), (41, [53, 57, 60]), (38, [50, 53, 57]), (40, [52, 56, 59])]  # Am F Dm E
hype = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]  # Am F C G
BAR = 4 * BEAT

# ---------- PART A: tension 0 -> DROP ----------
bars_a = np.arange(T0, DROP - 1e-6, BAR)
for bi, bt in enumerate(bars_a):
    root, ch = dark[bi % 4]
    d = min(BAR, DROP - max(bt, 0))
    if bt + BAR <= 0: continue
    add(pad(ch, BAR, 900 + 120 * bi), bt, 0.55)
    add(sub(root - 12 + 12, BAR), bt, 0.55)
    for k in range(8):                       # clock-like ticking pulse
        tt = bt + k * BEAT / 2
        if 0.8 <= tt < DROP - 0.6:
            add(pluck(ch[k % 3] + 12, 0.12, 2200), tt, 0.33, pan=(-0.35 if k % 2 else 0.35))
    for k in (0, 2):                           # half-time heartbeat kick
        tt = bt + k * BEAT
        if 3.0 <= tt < DROP - 1.2:
            add(kick(0.55), tt, 0.7)
            add(kick(0.35), tt + 0.22, 0.6)
# riser into drop
rs = 2.6; n = int(rs * SR); t = np.arange(n) / SR
nz = rng.standard_normal(n)
sweep = np.zeros(n)
for j in range(0, n, 2400):
    fc = 400 + (9000 - 400) * (j / n) ** 2
    seg = nz[j:j+2400]
    sweep[j:j+len(seg)] = bp(seg, fc * 0.7, min(fc * 1.3, 20000))
f = 200 + 1400 * (t / rs) ** 2
riser = sweep * (t / rs) ** 2 * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / rs) ** 3 * 0.25
add(riser, DROP - rs, 0.9)
for k in range(16):                            # snare roll accelerating
    tt = DROP - 2.0 + 2.0 * (1 - (1 - k / 16) ** 1.6)
    add(clap(), tt, 0.15 + 0.45 * k / 16)

# ---------- PART B: drop -> END ----------
pump = np.ones(N)
bars_b = np.arange(DROP, END_HIT, BAR)
for bi, bt in enumerate(bars_b):
    root, ch = hype[bi % 4]
    final = bt >= FINALE - 0.01
    add(pad(ch, BAR, 3800 if not final else 5200), bt, 0.55)
    for k in range(8):
        tt = bt + k * BEAT / 2
        if tt >= END_HIT: break
        add(bass(root - 12 + (12 if k % 2 else 0), BEAT / 2 * 0.9, 900), tt, 0.75)
    for k in range(4):
        tt = bt + k * BEAT
        if tt >= END_HIT: break
        add(kick(), tt, 0.95)
        i = int(tt * SR); m = min(int(0.32 * SR), N - i)
        pump[i:i+m] = np.minimum(pump[i:i+m], 0.35 + 0.65 * (np.arange(m) / m) ** 0.6)
        if k in (1, 3): add(clap(), tt, 0.55)
        add(hat(True), tt + BEAT / 2, 0.5, pan=0.25)
        if final:
            add(hat(), tt + BEAT / 4, 0.45, pan=-0.3); add(hat(), tt + 3 * BEAT / 4, 0.45, pan=-0.3)
    arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24]
    for k in range(16):
        tt = bt + k * BEAT / 4
        if tt >= END_HIT: break
        add(pluck(arp[k % 4], 0.18, 5200), tt, 0.38, pan=(-0.5 if k % 2 else 0.5))
# apply sidechain pump to everything except the kick (approximation: whole bus after drop, light)
i0 = int(DROP * SR)
L[i0:] *= 0.55 + 0.45 * pump[i0:]; R[i0:] *= 0.55 + 0.45 * pump[i0:]
for tt in (DROP, FINALE):                      # impacts
    add(kick(1.2), tt, 1.0)
# end hit + tail
add(kick(1.3), END_HIT, 1.0)
n = int(0.7 * SR); t = np.arange(n) / SR
add(lp(rng.standard_normal(n), 6000) * np.exp(-t * 5) * 0.4, END_HIT, 0.8)
fade = int(0.5 * SR)
L[int(END_HIT * SR):] *= np.linspace(1, 0, N - int(END_HIT * SR)) ** 2
R[int(END_HIT * SR):] *= np.linspace(1, 0, N - int(END_HIT * SR)) ** 2
fi = int(0.6 * SR)
L[:fi] *= np.linspace(0, 1, fi); R[:fi] *= np.linspace(0, 1, fi)

mix = np.stack([L, R], 1)
mix = hp(mix.T, 30).T
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= np.abs(mix).max() / 0.89
sf.write('music.wav', mix.astype(np.float32), SR)
print('ok', T0, len(bars_a), len(bars_b))
