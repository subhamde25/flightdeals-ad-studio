"""Original synthesized instruments + SFX (royalty-free, made from scratch)."""
import numpy as np
from scipy import signal

SR = 48000


def tt(dur):
    return np.arange(max(1, int(round(dur * SR)))) / SR


def noise(n, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def filt(x, kind, f, order=2):
    sos = signal.butter(order, f, btype=kind, fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0)


def peq(x, f0, gain_db, q=1.0):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x, axis=0)


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


# ---------------------------------------------------------------- drums
def kick(f0=48, f1=170, punch=32, decay=6.0, click=0.5, drive=1.7, seed=0):
    t = tt(0.55)
    f = f0 + (f1 - f0) * np.exp(-t * punch)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    cl = filt(noise(len(t), seed), 'highpass', 2000) * np.exp(-t * 350) * click
    return np.tanh(drive * (body + cl)) / np.tanh(drive)


def b808(freq, dur, drive=2.4, glide=1.18, decay=0.9, seed=0):
    t = tt(dur + 0.06)
    f = freq * (1 + (glide - 1) * np.exp(-t * 45))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.12 * np.sin(2 * ph)
    env = np.minimum(1, t / 0.003) * np.exp(-t * decay)
    rel = np.clip((dur + 0.06 - t) / 0.06, 0, 1)
    x = np.tanh(drive * x * env * rel) / np.tanh(drive)
    return filt(x, 'lowpass', 2600)


def clap(seed=1, tone=0.25):
    t = tt(0.45)
    n = filt(noise(len(t), seed), 'bandpass', (900, 6000))
    env = np.zeros_like(t)
    for d in (0, 0.009, 0.019):
        env += (t >= d) * np.exp(-np.maximum(0, t - d) * 140) * 0.65
    env += (t >= 0.026) * np.exp(-np.maximum(0, t - 0.026) * 15)
    body = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 30) * tone
    return np.tanh(1.4 * (n * env + body)) * 0.8


def snare(seed=2, decay=22):
    t = tt(0.25)
    n = filt(noise(len(t), seed), 'bandpass', (1200, 8000)) * np.exp(-t * decay)
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 35) * 0.6
    return np.tanh(1.3 * (n + tone)) * 0.8


_HF = [205.3, 304.4, 369.6, 522.7, 540.0, 800.0]


def hat(open_=False, seed=3):
    dur = 0.4 if open_ else 0.07
    t = tt(dur)
    x = sum(signal.square(2 * np.pi * f * 1.9 * t + k) for k, f in enumerate(_HF))
    x = filt(x, 'bandpass', (7000, 14000)) + 0.4 * filt(noise(len(t), seed), 'highpass', 9000)
    return x * np.exp(-t * (11 if open_ else 75)) * 0.22


def crash(seed=4, dur=2.2):
    t = tt(dur)
    x = sum(signal.square(2 * np.pi * f * 3.1 * t + k) for k, f in enumerate(_HF))
    x = filt(x, 'highpass', 4000) * 0.5 + filt(noise(len(t), seed), 'highpass', 5000)
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 400))
    return x * env * 0.2


# ---------------------------------------------------------------- tonal
def cowbell(note, dur=0.32, drive=2.0):
    """Pitched phonk-style cowbell. note = midi number."""
    t = tt(dur)
    f = midi(note)
    x = 0.55 * signal.square(2 * np.pi * f * t) + 0.45 * signal.square(2 * np.pi * f * 1.4823 * t)
    x = filt(x, 'bandpass', (max(300, f * 0.8), 6000))
    env = 0.75 * np.exp(-t * 11) + 0.25 * np.exp(-t * 70)
    return np.tanh(drive * x * env) * 0.5


def pluck(note, dur=0.25, cutoff=2400, seed=0):
    t = tt(dur)
    f = midi(note)
    x = signal.sawtooth(2 * np.pi * f * t) + 0.6 * signal.sawtooth(2 * np.pi * f * 1.004 * t + 1.1)
    x = filt(x, 'lowpass', cutoff, 2)
    return x * np.exp(-t * 9) * np.minimum(1, t / 0.002) * 0.35


def pad(notes, dur, cutoff=900, attack=0.5, release=0.6, seed=5):
    t = tt(dur)
    rng = np.random.default_rng(seed)
    L = np.zeros_like(t); R = np.zeros_like(t)
    for n in notes:
        f = midi(n)
        for d in (-0.11, -0.04, 0.04, 0.11):
            ff = f * 2 ** (d / 12)
            w = signal.sawtooth(2 * np.pi * ff * t + rng.uniform(0, 6.28))
            if d < 0: L += w
            else: R += w
            if abs(d) < 0.05: L += 0.5 * w; R += 0.5 * w
    st = np.stack([L, R], 1)
    st = filt(st, 'lowpass', cutoff, 2)
    env = np.minimum(1, t / attack) * np.clip((dur - t) / release, 0, 1)
    return st * env[:, None] / (len(notes) * 4) * 0.9


def sub_drone(dur, f=55.0, seed=6):
    t = tt(dur)
    x = np.sin(2 * np.pi * f * t) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.7 * t))
    tex = filt(noise(len(t), seed), 'bandpass', (80, 400)) * 0.15
    return (x + tex) * np.minimum(1, t / 0.6)


def stab(notes, dur=1.4, seed=7):
    """Big dark chord stab (saws + octave), for the end-card hits."""
    t = tt(dur)
    x = np.zeros_like(t)
    for n in notes:
        for d in (-0.12, 0, 0.12):
            x += signal.sawtooth(2 * np.pi * midi(n) * 2 ** (d / 12) * t + n)
    x = filt(x, 'lowpass', 3200, 2)
    env = np.exp(-t * 2.2) * np.minimum(1, t / 0.004)
    return np.tanh(1.6 * x * env / len(notes) / 2) * 0.7


# ---------------------------------------------------------------- sfx
def sweep_noise(dur, w_lo, w_mid, w_hi, seed=0):
    """noise whose spectral centre moves through 3 bands following weight arrays"""
    n = len(tt(dur))
    base = noise(n, seed)
    lo = filt(base, 'bandpass', (150, 900))
    mid = filt(base, 'bandpass', (900, 3500))
    hi = filt(base, 'bandpass', (3500, 12000))
    return lo * w_lo + mid * w_mid + hi * w_hi


def whoosh(dur=0.7, peak=0.55, seed=11, bright=1.0):
    t = tt(dur); k = t / dur
    env = np.exp(-((k - peak) / 0.2) ** 2)
    pos = np.clip((k - peak) / 0.35, -1, 1)
    w_lo = np.clip(1 - np.abs(pos) * 0.3, 0, 1) * (1 - 0.6 * np.exp(-((k - peak) / 0.12) ** 2))
    w_mid = np.exp(-((k - peak) / 0.22) ** 2)
    w_hi = np.exp(-((k - peak) / 0.12) ** 2) * bright
    x = sweep_noise(dur, w_lo * 0.8, w_mid, w_hi * 0.6, seed) * env
    pan = np.clip((k - peak) * 1.8, -1, 1)
    L = x * np.sqrt((1 - pan) / 2); R = x * np.sqrt((1 + pan) / 2)
    return norm(np.stack([L, R], 1), 0.9)


def riser(dur=1.5, seed=12):
    t = tt(dur); k = t / dur
    x = sweep_noise(dur, (1 - k) ** 2, np.sin(np.pi * np.clip(k * 1.1, 0, 1)), k ** 2, seed)
    f = 120 * (16 ** k)
    saw = filt(signal.sawtooth(2 * np.pi * np.cumsum(f) / SR), 'lowpass', 5000) * 0.35
    gate = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * np.cumsum(4 + 26 * k ** 2) / SR))
    y = (x * 0.8 + saw) * (k ** 2.2) * gate
    return norm(y, 0.9)


def rev_swell(dur=1.0, seed=13):
    t = tt(dur)
    c = filt(noise(len(t), seed), 'highpass', 3500) * np.exp(-t * 3.5)
    c = c + 0.5 * filt(noise(len(t), seed + 1), 'bandpass', (600, 3000)) * np.exp(-t * 5)
    return norm(c[::-1], 0.9)


def boom(dur=2.4, seed=14, big=True):
    t = tt(dur)
    f = 30 + 75 * np.exp(-t * 8)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (1.8 if big else 3.5))
    crack = filt(noise(len(t), seed), 'bandpass', (150, 4000)) * np.exp(-t * 28) * 0.8
    tail = filt(noise(len(t), seed + 1), 'lowpass', 700) * np.exp(-t * 2.6) * (0.35 if big else 0.15)
    return norm(np.tanh(2.0 * (sub + crack + tail)), 0.95)


def hit(seed=15):
    """short punchy impact for text slams"""
    t = tt(0.6)
    f = 45 + 120 * np.exp(-t * 30)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    sn = filt(noise(len(t), seed), 'bandpass', (500, 7000)) * np.exp(-t * 40) * 0.7
    return norm(np.tanh(2.2 * (body + sn)), 0.9)


def click(seed=16):
    t = tt(0.06)
    x = np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 260) * 0.5 + filt(noise(len(t), seed), 'highpass', 2500) * np.exp(-t * 700)
    x += np.sin(2 * np.pi * 900 * t) * np.exp(-t * 150) * 0.4
    return norm(x, 0.8)


def pop(f0=280, f1=1100, seed=17):
    t = tt(0.14)
    f = f0 + (f1 - f0) * (1 - np.exp(-t * 55))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 32) * np.minimum(1, t / 0.002)
    return norm(x, 0.8)


def tick(f=4200, seed=18):
    t = tt(0.03)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 400) + 0.5 * filt(noise(len(t), seed), 'highpass', 5000) * np.exp(-t * 900)
    return norm(x, 0.7)


def stamp(seed=19):
    t = tt(0.7)
    f = 60 + 70 * np.exp(-t * 40)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 16)
    slap = filt(noise(len(t), seed), 'bandpass', (250, 2600)) * np.exp(-t * 55) * 0.9
    rattle = filt(noise(len(t), seed + 1), 'bandpass', (2000, 6000)) * np.exp(-t * 80) * 0.25
    return norm(np.tanh(2.5 * (thump + slap + rattle)), 0.95)


def typing(n=9, seed=20):
    rng = np.random.default_rng(seed)
    times = np.cumsum(rng.uniform(0.045, 0.085, n))
    out = np.zeros(int((times[-1] + 0.1) * SR))
    for i, tm in enumerate(times):
        t = tt(0.04)
        k = filt(noise(len(t), seed + i), 'bandpass', (1200, 5000)) * np.exp(-t * 300)
        k += np.sin(2 * np.pi * rng.uniform(1800, 2600) * t) * np.exp(-t * 500) * 0.4
        s = int(tm * SR); out[s:s + len(k)] += k * rng.uniform(0.6, 1.0)
    return norm(out, 0.7)


def bell(f, dur=1.2):
    t = tt(dur)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 4) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 9) + 0.18 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 16)
    return x * np.minimum(1, t / 0.002)


def chime(notes=(88, 95), gap=0.085):
    out = np.zeros(int((gap * len(notes) + 1.3) * SR))
    for i, n in enumerate(notes):
        b = bell(midi(n)); s = int(i * gap * SR); out[s:s + len(b)] += b
    return norm(out, 0.7)


def scan(dur=0.55, seed=21):
    t = tt(dur); k = t / dur
    f = 900 + 2600 * k
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 * np.sin(np.pi * k)
    x += filt(noise(len(t), seed), 'bandpass', (2000, 6000)) * 0.15 * np.sin(np.pi * k)
    return norm(x, 0.6)


def beep():
    t = tt(0.14)
    x = signal.square(2 * np.pi * 1760 * t) * 0.3 + np.sin(2 * np.pi * 3520 * t) * 0.2
    x = filt(x, 'lowpass', 6000) * np.minimum(1, t / 0.003) * np.clip((0.14 - t) / 0.02, 0, 1)
    return norm(x, 0.6)


def sparkle(seed=22):
    rng = np.random.default_rng(seed)
    out = np.zeros(int(1.2 * SR))
    for i, n in enumerate([96, 100, 103, 108]):
        b = bell(midi(n), 0.9) * 0.6; s = int(i * 0.045 * SR); out[s:s + len(b)] += b
    return norm(out, 0.5)


def flyby(dur=1.8, seed=23):
    t = tt(dur); k = t / dur
    env = np.exp(-((k - 0.5) / 0.25) ** 2)
    rum = filt(noise(len(t), seed), 'lowpass', 500) * 1.0
    jet = filt(noise(len(t), seed + 1), 'bandpass', (1500, 6000)) * np.exp(-((k - 0.5) / 0.12) ** 2) * 0.5
    f = 260 - 90 * np.tanh((k - 0.5) * 6)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.08
    x = (rum + jet + tone) * env
    pan = np.clip((k - 0.5) * 2.2, -1, 1)
    return norm(np.stack([x * np.sqrt((1 - pan) / 2), x * np.sqrt((1 + pan) / 2)], 1), 0.9)


def glitch(dur=0.35, seed=24):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); out = np.zeros(n); i = 0
    while i < n:
        L = int(rng.uniform(0.008, 0.035) * SR)
        kind = rng.integers(0, 3)
        t = np.arange(L) / SR
        if kind == 0: seg = signal.square(2 * np.pi * rng.uniform(200, 1800) * t)
        elif kind == 1: seg = noise(L, seed + i) * 0.8
        else: seg = np.zeros(L)
        seg = np.round(seg * 4) / 4
        out[i:i + L] = seg[:max(0, min(L, n - i))]
        i += L
    return norm(filt(out, 'bandpass', (300, 8000)), 0.6)


def swipe(seed=25):
    t = tt(0.3); k = t / 0.3
    x = filt(noise(len(t), seed), 'bandpass', (2500, 9000)) * np.sin(np.pi * k) ** 2
    return norm(x, 0.5)


def notif():
    out = np.zeros(int(1.4 * SR))
    for i, n in enumerate([84, 91]):
        b = bell(midi(n), 1.2) * (0.9 if i else 0.7); s = int(i * 0.12 * SR); out[s:s + len(b)] += b
    return norm(out, 0.6)


# ---------------------------------------------------------------- fx processing
def make_ir(rt=1.6, seed=30, bright=5500):
    n = int(rt * SR); t = np.arange(n) / SR
    L = noise(n, seed) * np.exp(-t * 6.9 / rt); R = noise(n, seed + 1) * np.exp(-t * 6.9 / rt)
    ir = filt(np.stack([L, R], 1), 'lowpass', bright)
    pre = np.zeros((int(0.018 * SR), 2))
    ir = np.concatenate([pre, ir])
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


def reverb(x, ir, wet=0.25):
    from scipy.signal import fftconvolve
    if x.ndim == 1: x = np.stack([x, x], 1)
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x + y * wet


def compress(x, thresh_db=-18, ratio=3.0, att=0.005, rel=0.12, makeup_db=0):
    mono = np.max(np.abs(x), axis=1) if x.ndim == 2 else np.abs(x)
    a_a = np.exp(-1 / (att * SR)); a_r = np.exp(-1 / (rel * SR))
    lvl = signal.lfilter([1 - a_r], [1, -a_r], mono)  # smoothed envelope (release-ish)
    lvl = np.maximum(lvl, signal.lfilter([1 - a_a], [1, -a_a], mono))
    db = 20 * np.log10(lvl + 1e-9)
    over = np.maximum(0, db - thresh_db)
    gain_db = -over * (1 - 1 / ratio) + makeup_db
    g = 10 ** (gain_db / 20)
    return x * (g[:, None] if x.ndim == 2 else g)


def limiter(x, ceil=0.89, look=0.004, rel=0.08):
    n = int(look * SR)
    pk = np.max(np.abs(x), axis=1)
    from scipy.ndimage import maximum_filter1d
    pk = maximum_filter1d(pk, size=2 * n + 1)
    g = np.minimum(1, ceil / (pk + 1e-9))
    a_r = np.exp(-1 / (rel * SR))
    # smooth: instant attack (already look-ahead), slow release
    gs = g.copy()
    for i in range(1, len(gs)):
        gs[i] = min(g[i], gs[i - 1] * a_r + (1 - a_r) * g[i]) if g[i] >= gs[i - 1] else g[i]
    return x * gs[:, None]
