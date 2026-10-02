"""PySME section: diagram under the code block, revealed line by line (data-s = code step).
  1 SME_Structure()      -> the PySME box
  2 teff, logg, monh     -> model atmosphere: a chain of radiative-transfer cells (deep -> surface)
  3 vmic, vmac, vsini    -> Voigt profile (lower left)
  4 linelist             -> line-list table (lower right; real entries from the VALD file used)
  5 wave                 -> wavelength axis
  6 synthesize_spectrum  -> cells light up one at a time, deepest first; each shows the PySME spectrum
                            computed with only the deepest 14, 18, 23, 31 and all 55 layers
                            (../codeanim/cells.py); earlier spectra stay as faint ghosts."""
import json, os, numpy as np
from gen_svg import path

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "codeanim", "cells.json")))   # one synthesis per cell (../codeanim/cells.py)
w = np.array(D["wave"])[::2]
frames = [np.array(f)[::2] for f in D["frames"]]
W, H = 560, 414
BX0, BX1, BY0, BY1 = 2, 558, 2, 260                  # PySME box
s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="Inside PySME: a model atmosphere of radiative-transfer cells, a Voigt line profile and a line list; '
     f'below, a wavelength axis and the synthetic spectrum around H-alpha.">']

# 1 -- box
s.append(f'<g data-s="1"><rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" class="pp-box"/>'
         f'<text x="{(BX0+BX1)/2}" y="{BY0+30}" class="pp-name" text-anchor="middle">PySME</text></g>')


# 2 -- model atmosphere: the radiative-transfer cell figure supplied by the author (rt_cell.png, white + alpha),
#      used as a mask so it takes the theme colour; copies overlap by one body length, as in the author's chain:
#      [c c] ... [c] ... [c c]
CW, CH, BODY = 338, 228, 199                     # cell image size and body length (image px)
cx0 = [0, BODY, 640, 1080, 1080 + BODY]
SC = 540 / (cx0[-1] + 321 - 16)                  # fit the visible extent (x 16..321 of the last cell) into 540 px
AX0, AY0 = 10 - 16 * SC, 40
atm = ['<g data-s="2">',
       f'<defs><mask id="rtcell" maskUnits="userSpaceOnUse" x="0" y="0" width="{CW}" height="{CH}">'
       f'<image href="rt_cell.png" width="{CW}" height="{CH}"/></mask></defs>']
for i, x0 in enumerate(cx0):
    atm.append(f'<g class="pp-cell" data-i="{i}" transform="translate({AX0 + x0 * SC:.2f},{AY0}) scale({SC:.4f})">'
               f'<rect x="63" y="31" width="204" height="125" rx="20" class="pp-glow"/>'   # tint behind the body when lit
               f'<rect width="{CW}" height="{CH}" mask="url(#rtcell)" class="pp-cellink"/></g>')
for xd in (590, 1030):                            # the author's "■■■" between groups
    for k in (-1, 0, 1):
        x = AX0 + (xd + k * 26) * SC
        atm.append(f'<rect x="{x - 3:.1f}" y="{AY0 + 100 * SC - 3:.1f}" width="6" height="6" class="pp-sq"/>')
atm.append('</g>')
s += ''
s += atm

# 3 -- Voigt profile (lower left)
VX0, VX1, VY0, VY1 = 22, 262, 160, 232
x = np.linspace(-6, 6, 241)
g = np.exp(-x**2 / (2 * 0.9**2)); lz = 1 / (1 + (x / 0.55) ** 2)
v = np.convolve(g, lz, mode="same"); v /= v.max()     # Voigt = Gaussian (x) Lorentzian
PX = lambda t: VX0 + (t + 6) / 12 * (VX1 - VX0)
PY = lambda y: VY1 - y * (VY1 - VY0 - 6)
s.append(f'<g data-s="3"><line x1="{VX0}" x2="{VX1}" y1="{VY1}" y2="{VY1}" class="pp-rule"/>'
         f'<path d="{path(PX(x), PY(g / g.max() * 0.92))}" class="pp-comp" stroke-dasharray="3 3"/>'
         f'<path d="{path(PX(x), PY(lz * 0.55))}" class="pp-comp" stroke-dasharray="1 2.5"/>'
         f'<path d="{path(PX(x), PY(v))}" class="pp-voigt"/>'
         f'<text x="{VX0}" y="{VY1+16}" class="pp-sub">Voigt profile</text></g>')

# 4 -- line list (lower right): real entries from the VALD file in the snippet's range
TX = [298, 354, 428, 490]; TY = 166
rows = [("species", "λ / Å", "E / eV", "log gf"), ("Ti I", "6556.062", "1.460", "−1.060"),
        ("H I", "6562.797", "10.199", "0.710"), ("Ca I", "6563.678", "5.049", "0.043"),
        ("Fe I", "6569.214", "4.733", "−0.127")]
tb = ['<g data-s="4">', f'<line x1="{TX[0]}" x2="540" y1="{TY+5}" y2="{TY+5}" class="pp-rule"/>']
for r, row in enumerate(rows):
    y = TY + r * 15 + (4 if r else 0)
    for c, txt in enumerate(row):
        tb.append(f'<text x="{TX[c]}" y="{y}" class="{"pp-sub" if r == 0 else "pp-cellt"}">{txt}</text>')
tb.append(f'<line x1="{TX[0]}" x2="540" y1="{TY+4*15+10}" y2="{TY+4*15+10}" class="pp-rule"/>')
tb.append('</g>')
s += tb

# 5 -- wavelength axis; 6 -- spectrum (frames morph from 1 to the final synthesis)
SY0, SY1, AX = 292, 378, 386
X = lambda l: 6 + (l - w[0]) / (w[-1] - w[0]) * (W - 12)
Y = lambda f: SY0 + (1 - f) / 0.7 * (SY1 - SY0)
ax = [f'<g data-s="5"><line x1="6" x2="{W-6}" y1="{AX}" y2="{AX}" class="pp-rule"/>']
for l in range(6550, 6576, 5):
    ax.append(f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{AX}" y2="{AX+5}" class="pp-rule"/>'
              f'<text x="{X(l):.1f}" y="{AX+19}" class="pp-sub" text-anchor="{"start" if l == 6550 else "end" if l == 6575 else "middle"}">{l}{" Å" if l == 6575 else ""}</text>')
ax.append('</g>')
s += ax
xs = X(w)
sp = ['<g data-s="6">']
for k, f in enumerate(frames):                   # deepest 14, 18, 23, 31, all 55 layers; earlier ones ghosted
    sp.append(f'<path d="{path(xs, Y(f))}" class="pp-spec pp-k{" pp-ghost" if k < len(frames) - 1 else ""}" data-k="{k}"/>')
sp.append('</g>')
s += sp
s.append('</svg>')
open(os.path.join(HERE, "svg_PIPE.svg"), "w").write("\n".join(s))
print("ok", len("\n".join(s)) // 1024, "KB; cells", i)
