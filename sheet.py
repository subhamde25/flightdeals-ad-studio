"""Contact sheet: python sheet.py <dir> <out.png> [thumb_width] [cols]"""
import sys, glob, os
from PIL import Image, ImageDraw

d, out = sys.argv[1], sys.argv[2]
tw = int(sys.argv[3]) if len(sys.argv) > 3 else 300
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
files = sorted(glob.glob(os.path.join(d, 'still_*.png')), key=lambda f: float(os.path.basename(f)[6:-4]))
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size
th = int(h * tw / w)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 8) + 8, rows * (th + 30) + 8), (30, 30, 30))
dr = ImageDraw.Draw(sheet)
for i, (f, im) in enumerate(zip(files, ims)):
    x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 30)
    sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y + 22))
    dr.text((x + 2, y + 4), os.path.basename(f)[6:-4] + 's', fill=(255, 255, 0))
sheet.save(out)
print(out, sheet.size)
