"""4MOST section art: many spectra -> pipeline -> measured quantities.
svg_SURVEY.svg     : overlay (fan-in wires, the pipeline box, output labels)
svg_SURVEYDATA.svg : JSON with the base spectra (the 11 PySME syntheses of ../stack/stack.json,
                     4569-4581 A); the page draws a few hundred of them on a canvas with random
                     radial-velocity shifts and noise, so the stack reads as a survey."""
import json, os, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "stack", "stack.json")))
w = np.array(D["wave"]); sel = (w >= 4569.0) & (w <= 4581.0)
w = w[sel][::3]
base = [np.round(np.array(st["flux"])[sel][::3], 3).tolist() for st in D["stars"]]
open(os.path.join(HERE, "svg_SURVEYDATA.svg"), "w").write(
    json.dumps(dict(dw=round(float(w[1] - w[0]), 4), lam=round(float(w.mean()), 1), base=base), separators=(",", ":")))

W, H = 560, 400
SX1, SY0, SY1 = 214, 20, 380               # spectra stack (the canvas covers x 0..SX1, y SY0..SY1)
BX0, BX1, BY0, BY1 = 242, 384, 106, 294    # pipeline box: logo + caption
CY = (BY0 + BY1) / 2
OUT = [("RV", None), ("T", "eff"), ("log g", None), ("[Fe/H]", None), ("[X/Fe]", None)]
LW, LH = 92, round(92 * 300 / 231)         # logo size (4most_logo.png is 231 x 300)
s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="Hundreds of stellar spectra pass through the 4MOST pipeline and validation, giving radial velocities, effective temperatures, surface gravities and abundances.">']
for k in range(9):                         # fan-in
    y = SY0 + 20 + k * (SY1 - SY0 - 40) / 8
    ye = CY + (y - H / 2) * 0.42
    s.append(f'<path d="M{SX1+4},{y:.1f} C{SX1+20},{y:.1f} {BX0-18},{ye:.1f} {BX0},{ye:.1f}" class="pp-wire"/>')
s.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" class="pp-box"/>')
s.append(f'<image href="4most_logo.png" x="{(BX0+BX1-LW)/2:.1f}" y="{BY0+16}" width="{LW}" height="{LH}"><title>4MOST</title></image>')
s.append(f'<text x="{(BX0+BX1)/2}" y="{BY1-16}" class="pp-sub" text-anchor="middle">pipeline · validation</text>')
for k, (lab, sub) in enumerate(OUT):
    y = 90 + k * 60
    y0 = CY + (k - 2) * 14
    s.append(f'<path d="M{BX1},{y0:.1f} C{BX1+24},{y0:.1f} {BX1+22},{y-9} {BX1+44},{y-9}" class="pp-wire"/>')
    t = lab if sub is None else f'{lab}<tspan baseline-shift="sub" font-size="72%">{sub}</tspan>'
    s.append(f'<text x="{BX1+52}" y="{y}" class="sv-out">{t}</text>')
s.append('</svg>')
open(os.path.join(HERE, "svg_SURVEY.svg"), "w").write("\n".join(s))
print("ok", len(base), "base spectra,", len(w), "points")
