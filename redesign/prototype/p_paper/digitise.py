import numpy as np, json
from PIL import Image
from scipy import ndimage, signal

im = np.asarray(Image.open("figures/age-P.png").convert("RGB")).astype(float)
top = im[:600]
OC = [(0.04,5.59,.11),(0.11,5.46,.19),(0.15,5.33,.06),(0.19,5.31,.14),(0.19,5.61,.17),(0.23,5.44,.12),(0.23,5.41,.05),
      (0.30,5.45,.28),(0.30,5.40,.15),(0.40,5.30,.07),(0.40,5.30,.12),(0.43,5.63,.05),(0.59,5.30,.04),(0.68,5.62,.18),
      (1.17,5.30,.08),(1.29,5.39,.05),(1.45,5.49,.01),(1.55,5.42,.15),(2.09,5.38,.23),(2.75,5.41,.12),(2.75,5.71,.08),(4.27,5.66,.53)]
CEPH_KNOWN = [(0.016,5.88,.09),(0.051,5.52,.23),(0.096,5.73,.17),(0.039,5.61,.07),(0.080,5.97,.08),(0.031,5.65,.08),
              (0.075,5.61,.13),(0.071,5.65,.25),(0.031,5.43,.07),(0.051,5.39,.18),(0.059,5.54,.09)]

def dist(rgb):
    return np.sqrt(((top - np.array(rgb)) ** 2).sum(axis=2))

# --- calibration from cluster markers: matched-filter for the blue disc, then least squares
blue = (dist((31,119,180)) < 30).astype(float)
yy, xx = np.mgrid[-9:10, -9:10]
disc = ((xx**2 + yy**2) <= 7.5**2).astype(float)
resp = signal.fftconvolve(blue, disc[::-1, ::-1], mode="same")
peaks = (resp == ndimage.maximum_filter(resp, size=11)) & (resp > 0.9 * disc.sum())
py, px = np.nonzero(peaks)
# initial mapping from two well-separated clusters, then refine by nearest matching
b, a0 = 262.0, 524 + 262 * 0.721
d, c = -326.7, 2060.8
for it in range(3):
    pred = np.array([[a0 + b*np.log10(t), c + d*A] for t, A, e in OC])
    pairs = []
    for (u, v) in pred:
        k = np.argmin((px-u)**2 + (py-v)**2)
        if (px[k]-u)**2 + (py[k]-v)**2 < 12**2:
            pairs.append((u, v, px[k], py[k]))
    P = np.array(pairs)
    # refit x = a0 + b log t ; y = c + d A using matched marker pixels
    lt = np.array([np.log10(t) for t, A, e in OC])
    Av = np.array([A for t, A, e in OC])
    sel = [i for i, (u, v) in enumerate(pred) if any(abs(u-p[0]) < 1e-6 and abs(v-p[1]) < 1e-6 for p in pairs)]
    b, a0 = np.polyfit(lt[sel], P[:, 2], 1)
    d, c = np.polyfit(Av[sel], P[:, 3], 1)
    res_x = P[:, 2] - (a0 + b*lt[sel]); res_y = P[:, 3] - (c + d*Av[sel])
print(f"calibration: {len(sel)}/22 clusters matched; x = {a0:.1f} + {b:.1f} log t ; y = {c:.1f} + {d:.1f} A")
print(f"rms residual: {np.sqrt((res_x**2).mean()):.2f} px in x, {np.sqrt((res_y**2).mean()):.2f} px in y  (= {np.sqrt((res_y**2).mean())/abs(d):.4f} dex)")
to_t = lambda x: 10 ** ((x - a0) / b)
to_A = lambda y: (y - c) / d

# --- Cepheid stars: template from the legend star, matched filter on the orange mask
orange = (dist((255,127,14)) < 30).astype(float)
lab, n = ndimage.label(orange[400:520, 150:260])
# legend star sits near (199, 462)
tpl = orange[462-11:462+12, 199-11:199+12]
resp = signal.fftconvolve(orange, tpl[::-1, ::-1], mode="same")
pk = (resp == ndimage.maximum_filter(resp, size=9)) & (resp > 0.72 * tpl.sum())
sy, sx = np.nonzero(pk)
stars = [(x, y) for x, y in zip(sx, sy) if not (150 < x < 260 and 430 < y < 500)]   # drop the legend
ceph = sorted([(to_t(x), to_A(y), x, y) for x, y in stars])
print(f"Cepheid markers found: {len(ceph)}")
# validate against the 11 tabulated Cepheids
for t, A, e in sorted(CEPH_KNOWN):
    best = min(ceph, key=lambda r: (np.log10(r[0]) - np.log10(t))**2 * 25 + (r[1] - A)**2)
    print(f"  table {t:.3f} Gyr A(P) {A:.2f}  ->  figure {best[0]:.3f} Gyr {best[1]:.3f}   dA = {best[1]-A:+.3f}")

# vertical error bars of each Cepheid: extent of light-orange pixels in the marker column
light = dist((255,191,134)) < 45   # tab:orange at alpha ~0.5 on white
for i, (t, A, x, y) in enumerate(ceph):
    col = light[:, max(0, x-1):x+2].any(axis=1)
    up = y
    while up > 0 and (col[up-1] or orange[up-1, x] > 0): up -= 1
    dn = y
    while dn < col.size - 1 and (col[dn+1] or orange[dn+1, x] > 0): dn += 1
    ceph[i] = (t, A, abs(to_A(up) - to_A(dn)) / 2)
json.dump(dict(oc=OC, ceph=[list(map(float, r)) for r in ceph], cal=[a0, b, c, d]), open("digitised.json", "w"), indent=1)
print("errors (dex):", [round(r[2], 2) for r in ceph])
