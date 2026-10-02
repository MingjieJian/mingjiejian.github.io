"""Kitt Peak FTS solar flux atlas (Kurucz et al. 1984), residual flux -> R~6000 on a log-lambda grid."""
import numpy as np
from scipy import ndimage
# fixed-width records: 6-char flux (x1e5) + 10-char air wavelength (nm x1e6), 5 per line
recs = []
for line in open("solarflux.asc"):
    line = line.rstrip("\n")
    for k in range(0, len(line) - 15, 16):
        r = line[k:k + 16]
        try: f_, w_ = int(r[:6]), int(r[6:])
        except ValueError: continue
        if 295_000_000 < w_ < 1_301_000_000 and 0 <= f_ < 130_000: recs.append((f_, w_))
vals = np.array(recs, dtype=np.int64)
flux, wl_nm = vals[:, 0] / 1e5, vals[:, 1] / 1e6
wl = wl_nm * 10                                     # air wavelength, Angstrom
o = np.argsort(wl); wl, flux = wl[o], flux[o]
print("points", len(wl), "range", wl[0].round(1), wl[-1].round(1), "flux median", np.median(flux).round(3))
LO, HI = 3560.0, 6562.80 ** 2 / 3560.0
sel = (wl > LO - 30) & (wl < HI + 30); wl, flux = wl[sel], flux[sel]
# uniform log-lambda grid at R_grid = 300000, smooth to R = 6000, resample to 7000 points
lg = np.arange(np.log(LO - 20), np.log(HI + 20), 1 / 300000)
f = np.interp(lg, np.log(wl), flux)
sig = (300000 / 6000) / 2.3548
fs = ndimage.gaussian_filter1d(f, sig)
out = np.exp(np.linspace(np.log(LO), np.log(HI), 7000))
fo = np.clip(np.interp(np.log(out), lg, fs), 0, 1.05)
np.save("solar_R6000.npy", np.vstack([out, fo]))
for c in (3933.66, 4861.34, 5889.95, 6562.8, 6870, 7600, 10827.09, 10830.3):
    print(c, round(float(np.interp(c, out, fo)), 3))
