"""Animated PySME fit for the PySME panel, built from a real PySME run
(../pysme_fit/fit_frames.json). 'Observed' is a PySME solar synthesis plus
noise; each model curve is the synthesis at one recorded solver iteration."""
import json, os, numpy as np
from gen_svg import path

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "pysme_fit", "fit_frames.json")))
wave, obs = np.array(D["wave"]), np.array(D["obs"])
SN = D["sn"]
FRAMES = [0, 2, 3, 4, 5]                   # every recorded solver iteration
ITER_LABEL = [1, 2, 3, 4, 5]                  # solver iteration numbers, as recorded by PySME

W, H = 420, 238
L, R, T, B = 46, 410, 16, 196
LO, HI = wave[0], wave[-1]
YLO, YHI = 0.26, 1.06
X = lambda l: L + (l - LO) / (HI - LO) * (R - L)
Y = lambda f: B - (f - YLO) / (YHI - YLO) * (B - T)


def chi2(model):
    return float(np.sum(((model - obs) * SN) ** 2) / (obs.size - 3))


def svg():
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Animation of a PySME fit to a noisy solar H-alpha spectrum: synthetic spectra from successive solver '
         f'iterations converge onto the observed points">']
    s.append(f'<defs><clipPath id="fa-clip"><rect x="{L}" y="{T}" width="{R-L}" height="{B-T}"/></clipPath></defs>')
    s.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" class="pf-frame"/>')
    s.append('<g clip-path="url(#fa-clip)">')
    s.append(f'<line x1="{L}" x2="{R}" y1="{Y(1):.1f}" y2="{Y(1):.1f}" class="pf-cont"/>')
    sel = np.arange(0, wave.size, 3)
    dots = " ".join(f"M{X(w):.1f},{Y(f):.1f}h0" for w, f in zip(wave[sel], obs[sel]))
    s.append(f'<path d="{dots}" class="fa-obs"/>')
    for k, fi in enumerate(FRAMES):
        fl = np.array(D["steps"][fi]["flux"])
        s.append(f'<path d="{path(X(wave[::2]), Y(fl[::2]))}" class="fa-model" pathLength="1" data-step="{k}"/>')
    s.append('</g>')
    for l in range(6552, 6575, 4):
        s.append(f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{B}" y2="{B+5}" class="pf-ax"/>')
        s.append(f'<text x="{X(l):.1f}" y="{B+17}" class="pf-tk" text-anchor="middle">{l}</text>')
    for f in (0.4, 0.6, 0.8, 1.0):
        s.append(f'<line x1="{L-5}" x2="{L}" y1="{Y(f):.1f}" y2="{Y(f):.1f}" class="pf-ax"/>')
        s.append(f'<text x="{L-8}" y="{Y(f)+3.5:.1f}" class="pf-tk" text-anchor="end">{f:.1f}</text>')
    s.append(f'<text x="{(L+R)/2:.0f}" y="{H-4}" class="pf-axl" text-anchor="middle">Wavelength (Å)</text>')
    s.append(f'<text x="11" y="{(T+B)/2:.0f}" class="pf-axl" text-anchor="middle" transform="rotate(-90 11 {(T+B)/2:.0f})">Normalised flux</text>')
    s.append('</svg>')
    return "\n".join(s)


def steps_json():
    out = []
    for k, fi in enumerate(FRAMES):
        st = D["steps"][fi]
        p = st["params"]
        out.append(dict(it=ITER_LABEL[k], teff=round(p["teff"]), logg=round(p["logg"], 2), monh=round(p["monh"], 2),
                        chi2=round(chi2(np.array(st["flux"])), 2)))
    return json.dumps(out)


if __name__ == "__main__":
    open(os.path.join(HERE, "svg_FA.svg"), "w").write(svg())
    open(os.path.join(HERE, "svg_FAsteps.svg"), "w").write(steps_json())
    print(steps_json())
