"""Card II art: a column of PySME syntheses of a line-rich window (4560-4585 A) (data: ../stack/stack.json
from stack/run.py), one star per row, sorted by Teff."""
import json, os, numpy as np
from gen_svg import path

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "stack", "stack.json")))
w = np.array(D["wave"]); SEL = (w >= 4569.0) & (w <= 4581.0)   # a 12 A slice of the synthesis
w = w[SEL]; lo, hi = w[0], w[-1]
W, H = 420, 238
X0, X1, Y0, DY, AMP = 2, 418, 6, 20.5, 24
X = lambda l: X0 + (l - lo) / (hi - lo) * (X1 - X0)
s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="Synthetic spectra of eleven FGK stars, computed with PySME and stacked by effective temperature.">']
n = len(D["stars"])
for k, st in enumerate(D["stars"]):
    f = np.array(st["flux"])[SEL]; y0 = Y0 + k * DY
    s.append(f'<path d="{path(X(w), y0 + (1 - f) * AMP)}" class="art-spec" opacity="{1 - k * 0.055:.2f}"/>')
s.append('</svg>')
open(os.path.join(HERE, "svg_D_stack.svg"), "w").write("\n".join(s))
print("ok")
