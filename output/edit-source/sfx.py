# Synthesised SFX (original, copyright-free) placed on the edit timeline -> sfx.wav (stereo)
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000; DUR = 39.2; N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def T(d): return np.arange(int(d * SR)) / SR
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0: return
    l = np.cos((pan + 1) * np.pi / 4) * 1.414; r = np.sin((pan + 1) * np.pi / 4) * 1.414
    L[i:i+n] += sig[:n] * g * l; R[i:i+n] += sig[:n] * g * r

def whoosh(d=0.45, up=True):
    t = T(d); nz = rng.standard_normal(len(t)); out = np.zeros(len(t)); blk = 1200
    for j in range(0, len(t), blk):
        x = j / len(t); fc = (300 + 5000 * x ** 1.5) if up else (5300 - 5000 * x ** 0.7)
        out[j:j+blk] = bp(nz[j:j+blk], fc * 0.6, min(fc * 1.6, 20000))
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
    return out * e * 0.8
def pop(f=900):
    t = T(0.12); fr = f * (1 + 1.5 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 38) * 0.7
def click():
    t = T(0.04); return (hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 260) + np.sin(2*np.pi*2200*t) * np.exp(-t*180) * 0.5) * 0.7
def key():
    t = T(0.05); return hp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 150) * 0.35
def bell(f=1046.5, d=1.6):
    t = T(d); s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * (2.2 + m)) for m, a in ((1, 1), (2.76, .45), (5.4, .25), (8.9, .12)))
    return s * 0.35
def ding():
    return bell(1568, 0.9) * 0.9 + bell(2093, 0.9) * 0.5
def impact(g=1.0):
    t = T(1.2); f = 38 + 90 * np.exp(-t * 14)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    crack = lp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 18) * 0.5
    return np.tanh((boom + crack) * 1.4) * 0.8 * g
def thump():
    t = T(0.35); f = 50 + 60 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * 0.9
def tick():
    t = T(0.03); return bp(rng.standard_normal(len(t)), 3000, 7000) * np.exp(-t * 300) * 0.5
def glitch(d=0.55):
    t = T(d); out = np.zeros(len(t)); seg = int(0.035 * SR)
    for j in range(0, len(t), seg):
        k = rng.integers(0, 3)
        tt = t[:min(seg, len(t) - j)]
        if k == 0: s = np.sign(np.sin(2 * np.pi * rng.uniform(80, 400) * tt))
        elif k == 1: s = rng.standard_normal(len(tt)) * 0.7
        else: s = np.sin(2 * np.pi * rng.uniform(800, 2500) * tt)
        out[j:j+len(tt)] = s * rng.uniform(0.3, 1)
    out = np.round(out * 6) / 6                     # bit-crush
    return lp(out, 6000) * 0.35 * np.minimum(1, (d - t) / 0.05)
def buzz():
    t = T(0.5); s = np.sign(np.sin(2*np.pi*110*t)) + 0.5*np.sign(np.sin(2*np.pi*116*t))
    return lp(s, 1800) * np.exp(-t*3) * 0.22
def ring(d=1.1):
    t = T(d); s = (np.sin(2*np.pi*1300*t) + np.sin(2*np.pi*1650*t)) * (np.sin(2*np.pi*22*t) > 0)
    gate = ((t % 0.55) < 0.42).astype(float)
    return lp(s * gate, 5000) * 0.18 * np.minimum(1, (d - t) / 0.05)
def shimmer(d=1.4):
    t = T(d); s = sum(np.sin(2*np.pi*f*t + i) for i, f in enumerate((1760, 2217, 2637, 3520)))
    return s * np.exp(-t * 2.5) * np.minimum(1, t / 0.02) * 0.08
def reverse_swell(d=0.8):
    return impact(0.5)[:int(d*SR)][::-1] * 0.8

# ---------------- timeline ----------------
add(impact(0.7), 0.0); add(whoosh(0.6, False), 0.0, 0.6)
for k in range(5): add(tick(), 1.0 + k * 0.32, 0.5, pan=0.3 if k % 2 else -0.3)  # clock ticks
add(bell(880, 2.2), 2.44, 0.55)                       # "12 baje" chime
add(thump(), 4.22, 0.9); add(thump(), 4.48, 0.6)       # "dard" heartbeat
add(whoosh(), 6.25, 0.6, -0.4)
add(pop(750), 8.2, 0.55)                               # kidney card
add(whoosh(), 10.65, 0.6, 0.4)
for tt in (12.36, 12.9, 13.44): add(click(), tt, 0.45); add(whoosh(0.18), tt, 0.25)  # calendar flips
add(impact(), 14.18, 0.85)                             # "Kyun?"
add(glitch(), 15.66, 0.75); add(buzz(), 16.1, 0.6)     # aarthik tangi
add(shimmer(), 16.64, 0.9); add(whoosh(0.5, False), 16.64, 0.5)
add(reverse_swell(0.9), 19.15); add(click(), 20.06, 0.8)  # brand click
for k in range(10): add(key(), 20.15 + k * 0.085, 0.6)   # url typing
add(pop(1100), 21.05, 0.5)
add(click(), 21.8, 0.7); add(whoosh(0.35), 21.8, 0.4)
add(whoosh(), 23.15, 0.55, -0.3)
add(ding(), 24.05, 0.5); add(ding(), 27.26, 0.5)        # checklist
add(whoosh(), 28.6, 0.55, 0.3)
add(ring(), 29.0, 0.45)                                 # phone ring
for k in range(10): add(tick(), 29.98 + k * 0.17, 0.45)  # digits roll in
add(pop(1300), 31.9, 0.45)
add(pop(900), 32.7, 0.5)                                # "call"
add(whoosh(0.6, False), 34.95, 0.6); add(impact(0.8), 35.1, 0.6)
add(ring(1.0), 36.0, 0.35)
add(shimmer(1.2), 37.0, 0.6)
add(impact(0.9), 38.55, 0.7)

mix = np.stack([L, R], 1); mix = np.tanh(mix * 1.1)
sf.write('sfx.wav', mix.astype(np.float32), SR); print('sfx ok', np.abs(mix).max())
