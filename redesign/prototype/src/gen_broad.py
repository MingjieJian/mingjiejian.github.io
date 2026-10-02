"""Card I art: one Ca I 6162 line synthesised with PySME, broadening switched on step by step
(data: ../broad/broad.json from broad/run.py), all four profiles overlaid on one axis."""
import json, os, numpy as np
from gen_svg import path

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "broad", "broad.json")))
w = np.array(D["wave"]); C = 6162.173; HW = 1.8
sel = np.abs(w - C) <= HW
STEPS = [("thermal", "thermal", "art-c1"), ("pressure", "+ pressure", "art-c2"),
         ("rotation", "+ rotation", "art-c3"), ("instrument", "+ instrument", "art-prof")]
W, H = 600, 312
X0, X1, TOP, AX = 6, 594, 34, 268
X = lambda l: X0 + (l - (C - HW)) / (2 * HW) * (X1 - X0)
Y = lambda f: TOP + (1 - f) * (AX - 14 - TOP) / 0.78

s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="One Ca I absorption line synthesised with PySME: thermal broadening only, then adding pressure, rotational and instrumental broadening.">',
     f'<line x1="{X0}" x2="{X1}" y1="{TOP}" y2="{TOP}" class="art-base"/>',
     f'<line x1="{X0}" x2="{X1}" y1="{AX}" y2="{AX}" class="art-base"/>']
for d in (-1.5, -1, -0.5, 0, 0.5, 1, 1.5):
    x = X(C + d)
    s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{AX}" y2="{AX + (6 if d % 1 == 0 else 3)}" class="art-base"/>')
    if d % 1 == 0:
        lab = "0" if d == 0 else f"{'+' if d > 0 else '−'}{abs(d):.0f} Å"
        s.append(f'<text x="{x:.1f}" y="{AX + 20}" class="art-lab" text-anchor="middle">{lab}</text>')
for key, lab, cls in STEPS:
    s.append(f'<path d="{path(X(w[sel]), Y(np.array(D[key])[sel]))}" class="{cls}"/>')
# legend, lower right (the far wing is at the continuum there)
lx, ly = 452, 128
for k, (key, lab, cls) in enumerate(STEPS):
    y = ly + k * 22
    s.append(f'<line x1="{lx}" x2="{lx + 26}" y1="{y - 4}" y2="{y - 4}" class="{cls}"/>')
    s.append(f'<text x="{lx + 36}" y="{y}" class="art-lab">{lab}</text>')
s.append(f'<text x="{X0}" y="{TOP - 12}" class="art-lab">Ca I 6162 Å · solar model · PySME</text>')
s.append('</svg>')
open(os.path.join(HERE, "svg_D_broad.svg"), "w").write("\n".join(s))
print("ok")
