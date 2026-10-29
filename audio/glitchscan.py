import sys, subprocess, numpy as np
f, W, H = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
raw = subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-vf',f'scale={W}:{H},format=gray','-f','rawvideo','-'], capture_output=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
by, bx = H // 8, W // 8
def blocks(x): return x[:by*8, :bx*8].reshape(8, by, 8, bx).mean((1, 3))
hits = []
for i in range(1, len(a) - 1):
    dp = blocks(np.abs(a[i] - a[i-1])); dn = blocks(np.abs(a[i] - a[i+1])); ds = blocks(np.abs(a[i+1] - a[i-1]))
    score = np.minimum(dp, dn) - 3 * ds
    if score.max() > 12: hits.append((i, round(i/60, 3), round(float(score.max()), 1)))
print(len(a), 'frames; suspicious:', hits)
