"""Compose BGM, place VO + SFX, mix and master.  python make_audio.py v|h"""
import sys, os, json, subprocess
import numpy as np
import soundfile as sf
from synth import *

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'build'); os.makedirs(OUT, exist_ok=True)


class Mix:
    def __init__(self, dur):
        self.n = int(dur * SR); self.dur = dur
        self.b = {k: np.zeros((self.n, 2)) for k in ('drums', 'bass', 'music', 'fx', 'sfx', 'vo', 'verb', 'intro')}

    def add(self, bus, x, t0, db=0.0, pan=0.0, send=0.0):
        if x.ndim == 1:
            x = np.stack([x * np.sqrt(1 - pan), x * np.sqrt(1 + pan)], 1)
        s = int(round(t0 * SR))
        if s < 0: x = x[-s:]; s = 0
        e = min(self.n, s + len(x))
        if e <= s: return
        g = 10 ** (db / 20)
        self.b[bus][s:e] += x[:e - s] * g
        if send: self.b['verb'][s:e] += x[:e - s] * g * send


def decode(path):
    wav = path + '.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ar', str(SR), '-ac', '1', wav], check=True)
    x, _ = sf.read(wav); return x


def fade(x, fi=0.01, fo=0.03):
    n = len(x); a = int(fi * SR); b = int(fo * SR)
    x = x.copy(); x[:a] *= np.linspace(0, 1, a); x[n - b:] *= np.linspace(1, 0, b); return x


def vo_track(m, src, plan):
    v = decode(src)
    v = filt(v, 'highpass', 85)
    v = peq(v, 220, -2.0, 0.9); v = peq(v, 3200, 3.0, 0.8); v = peq(v, 9000, 1.5, 0.7)
    v = compress(v, -22, 3.0, 0.004, 0.1)
    v = norm(v, 0.9)
    for a, b, t0 in plan:
        seg = fade(v[int(a * SR):int(b * SR)], 0.008, 0.04)
        m.add('vo', seg, t0, 0, 0, send=0.05)


def sidechain(n, kicks, depth=0.55, rel=7.0):
    g = np.ones(n)
    t = np.arange(n) / SR
    for k in kicks:
        s = int(k * SR); e = min(n, s + int(0.5 * SR))
        if s >= n: continue
        g[s:e] = np.minimum(g[s:e], 1 - depth * np.exp(-(t[s:e] - k) * rel))
    return g


# ===================================================================== VERTICAL (9:16)
def track_v():
    B = 60 / 140; D = 6 * B; S2 = 6.0; S3 = 6.0 + 12 * B; S4 = 6.0 + 20 * B; LOGO = S4 + 2 * B
    DUR = 18.5
    m = Mix(DUR)
    st = B / 4
    kicks = []
    roots = [33, 29, 31, 28]                       # A1 F1 G1 E1
    chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 56, 59]]
    # ---------------- intro (dark build)
    m.add('intro', sub_drone(D - 0.08, 55.0) * 0.5, 0, -15)
    m.add('intro', pad([45, 57, 60, 64], D - 0.05, cutoff=520, attack=0.8, release=0.08), 0, -12, send=0.3)
    for i in range(int((D - 0.1) / (B / 2))):
        tm = i * B / 2
        m.add('intro', tick(4200 if i % 2 == 0 else 3100), tm, -28 + 10 * tm / D, 0.25 if i % 2 else -0.25)
    m.add('fx', riser(D - 1.05), 1.0, -8)
    m.add('fx', rev_swell(0.9), D - 0.9, -4)
    # ---------------- main beat
    melody = {0: [(0, 69), (3, 69), (6, 72), (8, 69), (10, 67), (11, 69), (14, 64)],
              1: [(0, 69), (3, 69), (6, 72), (8, 74), (10, 72), (12, 69), (14, 67)]}

    def bar(t0, bi, full=True, fill=False, hats=True, cow=True):
        kpat = [0, 3, 8, 11] if bi % 2 == 0 else [0, 3, 6, 10, 14]
        r = roots[bi % 4]
        for j, s in enumerate(kpat):
            tm = t0 + s * st
            m.add('drums', kick(), tm, -3); kicks.append(tm)
            nxt = kpat[j + 1] if j + 1 < len(kpat) else 16
            note = r + (12 if (bi % 2 == 1 and s == 14) else 0)
            m.add('bass', b808(midi(note), (nxt - s) * st * 0.98), tm, -4)
        for s in (4, 12):
            m.add('drums', clap(), t0 + s * st, -6, send=0.18)
        if hats:
            for s in range(0, 16, 2):
                if fill and s >= 12: break
                m.add('drums', hat(), t0 + s * st, -9 if s % 4 == 0 else -13, 0.3)
            if bi % 2 == 1 and not fill:
                for k in range(6):
                    m.add('drums', hat(), t0 + (12 + k * 2 / 3) * st, -14 + k, 0.3)
        if fill:
            for k in range(8):
                m.add('drums', snare(seed=40 + k), t0 + (12 + k * 0.5) * st, -16 + k * 1.3, send=0.1)
        if cow:
            for s, n in melody[bi % 2]:
                m.add('music', cowbell(n), t0 + s * st, -9, -0.15 if s % 4 else 0.15, send=0.22)
        m.add('music', pad(chords[bi % 4], 4 * B, cutoff=1100, attack=0.05, release=0.2), t0, -10, send=0.2)

    nbars = 7
    for bi in range(nbars):
        t0 = D + bi * 4 * B
        fill = bi in (1, 4, 6)
        bar(t0, bi, fill=fill)
    for tc in (D, S2, S3):
        m.add('drums', crash(), tc, -6, send=0.2)
    # ---------------- S4 breakdown -> logo
    m.add('bass', b808(midi(33), 2 * B - 0.05, decay=0.6), S4, -6)
    m.add('music', pad([45, 57, 60, 64], 2 * B, cutoff=600, attack=0.05, release=0.1), S4, -8, send=0.3)
    m.add('fx', rev_swell(0.75), LOGO - 0.75, -5)
    bar(LOGO, 0, fill=False)
    m.add('drums', crash(), LOGO, -5, send=0.2)
    FIN = LOGO + 4 * B
    m.add('drums', kick(), FIN, -2); kicks.append(FIN)
    m.add('bass', b808(midi(33), 1.25, decay=0.8), FIN, -3)
    m.add('drums', crash(dur=2.4), FIN, -5, send=0.3)
    m.add('music', stab([57, 60, 64, 69]), FIN, -6, send=0.4)
    m.add('music', pad([45, 57, 60, 64, 69], DUR - FIN, cutoff=900, attack=0.02, release=0.9), FIN, -9, send=0.4)

    # ---------------- VO (source in, source out, dest start)
    vo_track(m, os.path.join(ROOT, 'assets/audio/vo_v.mp3'), [
        (0.00, 0.82, 0.10), (1.14, 2.27, 1.15), (2.68, 3.96, 2.62), (4.40, 5.95, 4.20),
        (6.38, 7.52, 6.05), (7.58, 9.42, 7.40), (9.66, 11.04, 9.40), (11.40, 12.72, 11.18),
        (13.00, 15.14, 12.75), (15.42, 17.06, 15.45)])

    # ---------------- SFX on visual events
    X = []
    X += [(hit(), 0.06, -4), (hit(seed=31), 0.44, -4), (flyby(2.4), -0.3, -14)]
    X += [(pop(), 1.29, -10), (pop(320, 1250), 1.29 + B, -10), (pop(360, 1400), 1.29 + 2 * B, -10)]
    X += [(boom(), D, -3), (whoosh(0.6, 0.6), D - 0.3, -10)]
    X += [(hit(), 3.36, -6), (whoosh(0.6, 0.5, 12), 3.45, -9), (typing(9), 3.98, -14), (click(), 4.45, -8),
          (pop(240, 900), 4.66, -9), (stamp(), 5.60, -3), (whoosh(0.6, 0.6, 13), 5.66, -9)]
    X += [(pop(500 + 80 * i, 1600 + 150 * i), 5.05 + 0.15 * i, -16) for i in range(4)]
    X += [(boom(1.6, 41, big=False), S2, -6), (hit(), 6.70, -6), (whoosh(0.6, 0.55, 14), 6.95, -9)]
    # slot ticks for the price roll
    prev = 999
    for i in range(400):
        tm = 7.62 + i * 0.002
        if tm > 8.44: break
        k = (tm - 7.62) / 0.82; val = round(999 + (50 - 999) * (1 - (1 - k) ** 4))
        if prev - val >= 37: X.append((tick(3600 + (i % 3) * 300), tm, -18)); prev = val
    X += [(scan(), 7.72, -12), (beep(), 8.28, -12), (hit(seed=33), 8.44, -6), (sparkle(), 8.46, -12),
          (chime((88, 95)), 8.9, -10), (flyby(1.2, 24), 9.3, -10)]
    X += [(pop(300 + 40 * i, 1100 + 90 * i), 9.62 + 0.09 * i, -15) for i in range(6)]
    X += [(notif(), 10.12, -11), (whoosh(0.8, 0.6, 15), 10.55, -6)]
    X += [(boom(1.6, 42, big=False), S3, -6), (hit(), 11.88, -6), (whoosh(0.6, 0.55, 16), 12.05, -9),
          (pop(), 12.77, -11), (swipe(), 12.95, -10), (hit(seed=34), 13.2, -7), (pop(400, 1500), 13.4, -9),
          (stamp(seed=35), 14.06, -3), (whoosh(0.6, 0.55, 17), 14.2, -10)]
    X += [(chime((84 + 4 * i, 91 + 4 * i)), S4 + 0.07 + i * B / 2, -12) for i in range(3)]
    X += [(boom(), LOGO, -3), (sparkle(23), LOGO + 0.02, -10), (whoosh(0.5, 0.5, 18), LOGO + 0.05, -12),
          (pop(260, 980), 16.28, -10)]
    for x, t0, db in X:
        m.add('sfx', x, t0, db, send=0.12)
    return m, kicks, 'v'


# ===================================================================== HORIZONTAL (16:9)
def track_h():
    B = 60 / 130; D = 17 * B
    VIS, ESIM, HOT, END = 21 * B, 25 * B, 36 * B, 45 * B
    LOGO = 51 * B
    DUR = 25.5
    m = Mix(DUR)
    st = B / 4
    kicks = []
    roots = [33, 29, 31, 28]
    chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 56, 59]]
    arp = {0: [57, 60, 64, 69], 1: [57, 60, 65, 69], 2: [59, 62, 67, 71], 3: [56, 59, 64, 68]}
    CUT = 6.70
    # ---------------- intro build
    for i in range(int(CUT / B) + 1):
        tm = i * B
        if tm >= CUT: break
        m.add('intro', kick(f0=42, f1=90, punch=20, decay=9, click=0.05), tm, -16 + 6 * tm / CUT)
    for i in range(int(CUT / (B / 2))):
        tm = i * B / 2
        m.add('intro', tick(4200 if i % 2 == 0 else 3100), tm, -28 + 8 * tm / CUT, 0.3 if i % 2 else -0.3)
    m.add('intro', pad([45, 57, 60, 64], CUT, cutoff=480, attack=1.0, release=0.03), 0, -12, send=0.3)
    m.add('intro', sub_drone(CUT, 55), 0, -14)
    for i in range(int((CUT - 6 * B) / st)):
        tm = 6 * B + i * st
        bi = int(tm / (4 * B)) % 4
        n = arp[0][i % 4] + (12 if (i // 4) % 2 else 0)
        cut = 500 + 3000 * ((tm - 6 * B) / (CUT - 6 * B)) ** 1.5
        m.add('intro', pluck(n, 0.2, cutoff=cut), tm, -16, 0.2 if i % 2 else -0.2, send=0.25)
    for i in range(int((CUT - 9 * B) / (B / 2))):
        m.add('intro', hat(), 9 * B + i * B / 2, -15, 0.3)
    # snare build 10->14 beats
    tms = []
    for k in range(4): tms += [10 * B + k * B * j / [1, 2, 4, 8][k] for j in range([1, 2, 4, 8][k])]
    tms = [10 * B + 0 * B] + [11 * B + j * B / 2 for j in range(2)] + [12 * B + j * B / 4 for j in range(4)] + [13 * B + j * B / 8 for j in range(8)]
    for j, tm in enumerate(tms):
        m.add('drums', snare(seed=60 + j), tm, -16 + 10 * j / len(tms), send=0.15)
    m.add('fx', riser(CUT - 4.6), 4.6, -6)
    # vacuum: very quiet drone + reverse swell into the drop
    m.add('music', sub_drone(D - CUT, 55), CUT, -22)
    m.add('fx', rev_swell(0.85), D - 0.85, -4)

    # ---------------- drop: trap beat
    def bar(t0, bi, fill=False, quiet=False):
        kpat = [0, 7, 10] if bi % 2 == 0 else [0, 3, 10, 14]
        r = roots[bi % 4]
        for j, s in enumerate(kpat):
            tm = t0 + s * st
            m.add('drums', kick(), tm, -3); kicks.append(tm)
            nxt = kpat[j + 1] if j + 1 < len(kpat) else 16
            m.add('bass', b808(midi(r), (nxt - s) * st * 0.98), tm, -4)
        m.add('drums', clap(seed=5), t0 + 8 * st, -6, send=0.25)
        for s in range(16):
            if s % 2 == 0 or (bi % 2 == 1 and s >= 12):
                if fill and s >= 12: continue
                m.add('drums', hat(), t0 + s * st, -10 if s % 4 == 0 else -14, 0.3)
        if bi % 2 == 0:
            for k in range(3): m.add('drums', hat(), t0 + (6 + k * 2 / 3) * st, -15, 0.3)
        if fill:
            for k in range(8): m.add('drums', snare(seed=80 + k), t0 + (12 + k * 0.5) * st, -15 + k, send=0.1)
        for i in range(16):
            n = arp[bi % 4][i % 4] + (12 if i in (6, 7, 14, 15) else 0)
            m.add('music', pluck(n, 0.22, cutoff=2600), t0 + i * st, -11, 0.25 if i % 2 else -0.25, send=0.25)
        m.add('music', pad(chords[bi % 4], 4 * B, cutoff=1000, attack=0.05, release=0.2), t0, -11, send=0.2)

    nb = int(round((END - D) / (4 * B)))   # 7 bars
    for bi in range(nb):
        bar(D + bi * 4 * B, bi, fill=(bi in (1, 4, 6)))
    for tc in (D, VIS, ESIM, HOT):
        m.add('drums', crash(), tc, -6, send=0.2)
    # ---------------- end stabs "Compare. Discover. Save."
    stabs = [[57, 60, 64, 69], [53, 57, 60, 65], [52, 56, 59, 64]]
    sroots = [33, 29, 28]
    for i, tm in enumerate((END, END + 2 * B, END + 4 * B)):
        m.add('drums', kick(), tm, -2); kicks.append(tm)
        m.add('bass', b808(midi(sroots[i]), 2 * B - 0.05, decay=0.7), tm, -4)
        m.add('music', stab(stabs[i], 2 * B), tm, -5, send=0.4)
        m.add('drums', crash(seed=70 + i, dur=1.6), tm, -8, send=0.2)
        for k in range(4): m.add('drums', hat(), tm + B / 2 + k * B / 2 * 0.98, -17, 0.3)
    m.add('fx', rev_swell(0.8), LOGO - 0.8, -4)
    m.add('fx', riser(0.9, 50), LOGO - 0.9, -10)
    # ---------------- logo + outro
    m.add('drums', kick(), LOGO, -2); kicks.append(LOGO)
    m.add('bass', b808(midi(33), 1.6, decay=0.7), LOGO, -3)
    m.add('drums', crash(dur=2.5), LOGO, -5, send=0.3)
    m.add('music', stab([57, 60, 64, 69], 2.0), LOGO, -6, send=0.45)
    m.add('music', pad([45, 57, 60, 64, 69], DUR - LOGO, cutoff=1000, attack=0.02, release=1.0), LOGO, -9, send=0.4)
    for i in range(16):
        tm = LOGO + 4 * B + i * st * 2
        if tm > DUR - 0.5: break
        m.add('music', pluck(arp[0][i % 4] + 12, 0.25, cutoff=1800), tm, -18 - i * 0.6, 0.3 if i % 2 else -0.3, send=0.4)

    # ---------------- VO (src in, src out, dest)
    vo_track(m, os.path.join(ROOT, 'assets/audio/vo_h_fixed.wav'), [
        (0.00, 1.33, 0.10), (1.44, 2.88, 1.50), (3.00, 4.12, 3.00), (4.28, 5.58, 4.15), (5.64, 6.70, 5.45),
        (6.76, 7.86, 6.75), (7.96, 9.66, 7.90), (9.76, 11.78, 9.75), (11.88, 17.13, 11.70),
        (17.22, 18.40, 16.70), (18.48, 19.56, 17.90), (19.60, 21.04, 18.98),
        (21.13, 21.94, 20.80), (22.02, 22.85, 21.72), (23.30, 24.10, 22.64)])

    X = []
    # hook: photo slams + glass search typing, zoom-through into the browser
    X += [(hit(48), 0.08, -5), (hit(49), 0.80, -5), (typing(14, 50), 0.34, -15), (whoosh(0.6, 0.6, 47), 1.1, -8)]
    X += [(pop(400 + 30 * i, 1300 + 60 * i, 51 + i), 1.55 + i * 0.13, -16) for i in range(10)]
    X += [(hit(46), 1.95, -11), (hit(45), 3.05, -10), (hit(44), 4.25, -10), (hit(43), 5.55, -10)]
    X += [(glitch(0.25, 52), 3.0, -13), (whoosh(0.5, 0.5, 53), 2.8, -12), (glitch(0.25, 54), 4.15, -13),
          (whoosh(0.5, 0.5, 55), 3.95, -12), (glitch(0.25, 56), 5.45, -13), (whoosh(0.5, 0.5, 57), 5.25, -12),
          (glitch(0.3, 58), 6.42, -8)]
    X += [(pop(260 + 50 * i, 900 + 120 * i, 40 + i), 5.76 + 0.16 * i, -14) for i in range(3)]
    X += [(swipe(59), 6.9 + 0.07 * i, -18) for i in range(5)]
    # drop + logo, pull back to browser
    X += [(boom(), D, -2), (sparkle(60), D + 0.05, -12), (whoosh(0.5, 0.5, 39), D + 0.1, -12), (whoosh(0.6, 0.55, 61), 9.1, -10)]
    # visa
    X += [(click(62), 9.68, -9), (click(64), 10.32, -8), (pop(240, 900, 65), 10.52, -9)]
    X += [(pop(500 + 80 * i, 1600 + 150 * i, 66 + i), 10.85 + 0.12 * i, -16) for i in range(4)]
    X += [(stamp(), 11.2, -4), (whoosh(0.7, 0.55, 70), 11.2, -6)]
    # esim
    X += [(pop(300 + 30 * i, 1100 + 70 * i, 71 + i), 11.9 + 0.07 * i, -17) for i in range(8)]
    X += [(whoosh(0.5, 0.5, 85), 12.0, -12), (hit(81), 12.3, -9), (hit(82), 14.5, -9)]
    prev = 0
    for i in range(500):
        tm = 12.3 + i * 0.004
        if tm > 13.2: break
        v = round(901 * (1 - (1 - (tm - 12.3) / 0.9) ** 3))
        if v - prev >= 45: X.append((tick(3800 + (i % 3) * 250), tm, -20)); prev = v
    prev = 0
    for i in range(500):
        tm = 14.5 + i * 0.004
        if tm > 15.6: break
        v = round(175 * (1 - (1 - (tm - 14.5) / 1.1) ** 3))
        if v - prev >= 9: X.append((tick(3400 + (i % 3) * 250), tm, -20)); prev = v
    X += [(click(86 + i), 15.0 + 0.42 * i, -11) for i in range(3)]
    X += [(swipe(87 + i), 15.05 + 0.42 * i, -15) for i in range(3)]
    X += [(whoosh(0.7, 0.55, 88), 16.1, -9), (whoosh(0.6, 0.55, 38), 16.4, -8)]
    # hotels
    X += [(typing(5, 89), 16.92, -14), (click(90), 17.32, -9), (riser(0.5, 37), 17.36, -20), (pop(280, 1000, 91), 17.9, -11)]
    X += [(pop(360, 1300, 92), 17.98, -12), (swipe(93), 18.15, -11)]
    X += [(pop(400 + 50 * i, 1500 + 100 * i, 94 + i), 18.35 + 0.06 * i, -11) for i in range(3)]
    X += [(click(95), 18.75, -10), (click(36), 18.88, -10)] + [(pop(320 + 40 * i, 1200 + 80 * i, 96 + i), 18.92 + 0.08 * i, -15) for i in range(7)]
    X += [(stamp(97), 19.6, -3), (whoosh(0.7, 0.55, 98), 20.15, -7)]
    # end: three word slams with zoom-through whooshes
    for i, tm in enumerate((END, END + 2 * B, END + 4 * B)):
        X += [(boom(1.6, 99 + i, big=False), tm, -5), (hit(110 + i), tm, -6)]
        X += [(whoosh(0.45, 0.6, 115 + i), tm + 2 * B - 0.3, -11)]
    X += [(boom(), LOGO, -2), (sparkle(103), LOGO + 0.03, -10), (whoosh(0.5, 0.5, 104), LOGO + 0.05, -12),
          (pop(260, 980, 105), 24.2, -10), (pop(300, 1200, 120), 24.45, -13), (flyby(2.2, 106), 23.7, -15)]
    for x, t0, db in X:
        m.add('sfx', x, t0, db, send=0.12)
    return m, kicks, 'h'


def master(m, kicks, tag):
    n = m.n
    # sidechain pump on melodic + bass
    sc = sidechain(n, kicks, 0.45, 8.0)[:, None]
    music = (m.b['music'] * sc + m.b['bass'] * (0.35 + 0.65 * sc) + m.b['drums'] + m.b['fx'] + m.b['intro'] * 0.5)
    ir = make_ir(1.8, 31)
    verb = reverb(m.b['verb'], ir, 1.0) - m.b['verb']
    music = music + verb * 0.5
    music = filt(music, 'highpass', 28)
    music = compress(music, -16, 2.5, 0.01, 0.15)
    music = norm(music, 0.85)
    vo = m.b['vo']
    vo = vo + (reverb(vo, make_ir(0.6, 40, 7000), 0.05) - vo)
    # ducking from VO envelope
    env = np.abs(vo).max(axis=1)
    a = np.exp(-1 / (0.015 * SR)); r = np.exp(-1 / (0.25 * SR))
    from scipy.ndimage import maximum_filter1d
    env = maximum_filter1d(env, int(0.03 * SR))
    env = signal.lfilter([1 - r], [1, -r], env)
    duck = 1 - 0.6 * np.clip(env / 0.12, 0, 1)
    music = music * duck[:, None]
    sfx = m.b['sfx']
    mix = music * 0.74 + sfx * 0.55 + vo * 0.95
    fo = int(0.45 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    mix = compress(mix, -10, 2.0, 0.005, 0.12)
    mix = limiter(mix, 0.9)
    raw = os.path.join(OUT, f'mix_{tag}_raw.wav')
    sf.write(raw, mix.astype(np.float32), SR, subtype='FLOAT')
    for name, x in (('music', music * 0.74), ('vo', vo * 0.95), ('sfx', sfx * 0.55)):
        sf.write(os.path.join(OUT, f'stem_{tag}_{name}.wav'), x.astype(np.float32), SR, subtype='FLOAT')
    # two-pass loudnorm to -14 LUFS / -1 dBTP
    meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json', '-f', 'null', '-'],
                          capture_output=True, text=True).stderr
    js = json.loads(meas[meas.rfind('{'):meas.rfind('}') + 1])
    af = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    final = os.path.join(OUT, f'mix_{tag}.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af', af, '-ar', str(SR), final], check=True)
    print(tag, 'measured', js['input_i'], 'LUFS ->', final)


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'v'
    m, k, tag = track_v() if which == 'v' else track_h()
    master(m, k, tag)
