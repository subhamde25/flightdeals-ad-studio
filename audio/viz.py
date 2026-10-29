import sys, numpy as np, soundfile as sf
from PIL import Image, ImageDraw
from scipy import signal
tag = sys.argv[1]; marks = [float(x) for x in sys.argv[2].split(',')]
W, Hh = 1600, 130
x, sr = sf.read(f'build/mix_{tag}.wav'); dur = len(x)/sr
img = Image.new('RGB', (W, Hh*3 + 260), (18, 18, 24)); d = ImageDraw.Draw(img)
cols = {'music': (80, 180, 255), 'vo': (255, 210, 80), 'sfx': (120, 255, 150)}
for i, name in enumerate(['music', 'vo', 'sfx']):
    y, _ = sf.read(f'build/stem_{tag}_{name}.wav'); y = y.mean(1)
    hop = sr // 100; rms = np.sqrt(np.convolve(y**2, np.ones(hop)/hop, 'same'))[::hop]
    db = np.clip(20*np.log10(rms+1e-6), -60, 0)
    pts = [(k/100/dur*W, i*Hh + Hh - (v+60)/60*Hh) for k, v in enumerate(db)]
    d.line(pts, fill=cols[name], width=1); d.text((5, i*Hh+3), name, fill=cols[name])
f, t, S = signal.spectrogram(x.mean(1), sr, nperseg=2048, noverlap=1024)
S = 10*np.log10(S[f < 8000] + 1e-12); S = np.clip((S + 110) / 80, 0, 1)
sp = Image.fromarray((np.flipud(S)*255).astype(np.uint8)).resize((W, 260)).convert('RGB')
img.paste(sp, (0, Hh*3))
for m in marks:
    X = m/dur*W; d.line([(X, 0), (X, img.height)], fill=(255, 60, 60), width=1)
for s in range(int(dur)+1):
    d.text((s/dur*W+2, Hh*3-12), str(s), fill=(150,150,150))
img.save(f'_stills/audio_{tag}.png')
