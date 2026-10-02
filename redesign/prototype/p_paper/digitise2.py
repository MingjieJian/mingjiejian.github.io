import numpy as np, json
from PIL import Image, ImageDraw
from scipy import ndimage, signal
img = Image.open("figures/age-P.png").convert("RGB")
im = np.asarray(img).astype(float)
top = im[:600]
a0, b, c, d = 711.8, 260.3, 2021.3, -319.5
to_t = lambda x: 10 ** ((x - a0) / b); to_A = lambda y: (y - c) / d
CEPH_KNOWN = [(0.016,5.88,.09),(0.051,5.52,.23),(0.096,5.73,.17),(0.039,5.61,.07),(0.080,5.97,.08),(0.031,5.65,.08),
              (0.075,5.61,.13),(0.071,5.65,.25),(0.031,5.43,.07),(0.051,5.39,.18),(0.059,5.54,.09)]
orange = (np.sqrt(((top - [255,127,14])**2).sum(2)) < 30).astype(float)
tpl = orange[462-11:462+12, 199-11:199+12]
resp = signal.fftconvolve(orange, tpl[::-1, ::-1], mode="same") / tpl.sum()
pk = (resp == ndimage.maximum_filter(resp, size=7)) & (resp > 0.55)
sy, sx = np.nonzero(pk)
cand = [(x, y, resp[y, x]) for x, y in zip(sx, sy) if not (150 < x < 260 and 430 < y < 500) and 120 < x < 700]
print("candidates:", len(cand))

def err_bar(x, y):
    """half-length (px) of the vertical bar through (x, y): rows where column x differs from x±5 by an orange tint"""
    def tinted(r):
        cx = top[r, x - 1:x + 2].mean(0); side = (top[r, x - 6] + top[r, x + 6]) / 2
        dv = side - cx                          # orange tint: blue drops most, red barely
        return dv[2] > 12 and dv[2] > dv[0] + 8
    up = y - 9
    while up > 5 and tinted(up - 1): up -= 1
    dn = y + 9
    while dn < 595 and tinted(dn + 1): dn += 1
    return (dn - up) / 2

rows = []
for x, y, r in sorted(cand):
    e = err_bar(x, y) / abs(d)
    rows.append((to_t(x), to_A(y), e, x, y, r))
for t, A, e, x, y, r in rows:
    k = [kk for kk in CEPH_KNOWN if abs(np.log10(kk[0]/t)) < 0.03 and abs(kk[1]-A) < 0.02]
    tag = f"   table err {k[0][2]:.2f}" if k else ""
    print(f"x{x:4d} y{y:4d} score {r:.2f}  age {t:.3f}  A {A:.3f}  err {e:.2f}{tag}")
# overlay for visual check
ov = img.copy(); dr = ImageDraw.Draw(ov)
for t, A, e, x, y, r in rows:
    dr.ellipse([x-9, y-9, x+9, y+9], outline=(0, 160, 0), width=2)
ov.crop((100, 0, 760, 560)).save("overlay.png")
json.dump([[t, A, e] for t, A, e, *_ in rows], open("ceph_digitised.json", "w"))
