"""Schematic for the 'High-n H lines' panel: a selection of hydrogen levels on a
log-n axis (E_n = -13.6 eV / n^2 is linear in log n). On play, each high level
cross-fades from a sharp line to a Gaussian-blurred band whose width grows
with n. Schematic only; no physical model is implied by the widths."""
import numpy as np, os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 420, 250
LEVELS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30]
NTOP = 30
YLIM = 30                            # ionisation limit, drawn above the top level with an axis break
YTOP, YBOT = 50, 206                 # y of n = NTOP and n = 2
X0, X1 = 64, 300
Y = lambda n: YBOT - (np.log(n) - np.log(2)) / (np.log(NTOP) - np.log(2)) * (YBOT - YTOP)
NSTAR = 11.0


def w(n):
    """Fraction of a level that stays 'sharp' (schematic)."""
    return float(np.exp(-(n / NSTAR) ** 3))


def svg():
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Schematic energy-level diagram of hydrogen on a logarithmic n axis, with Balmer transitions from n = 2; '
         f'the highest levels blur">']
    s.append('<defs><linearGradient id="hl-cont" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" class="hl-cont-a"/><stop offset="1" class="hl-cont-b"/></linearGradient>')
    blurs = {}
    for n in LEVELS:
        if n >= 7:
            sd = round(0.6 + (1 - w(n)) * 3.2, 2)
            blurs[n] = sd
            s.append(f'<filter id="hl-b{n}" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                     f'<feGaussianBlur stdDeviation="0 {sd}"/></filter>')
    s.append('</defs>')
    s.append(f'<rect x="{X0}" y="8" width="{X1-X0}" height="{YLIM-8+12}" fill="url(#hl-cont)"/>')
    s.append(f'<line x1="{X0}" x2="{X1}" y1="{YLIM}" y2="{YLIM}" class="hl-limit"/>')
    for n in LEVELS:
        y = Y(n)
        # ink budget: a blurred level ends with the same total "ink" as the Balmer arrow to it
        # (0.25 + 0.75 w_n); blurring only spreads that ink, it never adds to it.
        total = 0.25 + 0.75 * w(n)
        sharp = w(n) ** 2 if n in blurs else 1.0          # what stays as a crisp line
        if n in blurs:
            band = round(1.2 + (1 - w(n)) * 7.0, 2)
            fuzz = min(1.0, 2.0 * max(total - sharp, 0.0) / band)   # x2: perceptual allowance for the blur
            s.append(f'<line x1="{X0}" x2="{X1}" y1="{y:.2f}" y2="{y:.2f}" class="hl-fuzz" stroke-width="{band}" '
                     f'filter="url(#hl-b{n})" data-o="{fuzz:.3f}"/>')
        s.append(f'<line x1="{X0}" x2="{X1}" y1="{y:.2f}" y2="{y:.2f}" class="hl-lev" data-o="{sharp:.3f}"/>')
    # n axis
    s.append(f'<line x1="{X0-10}" x2="{X0-10}" y1="{YTOP}" y2="{YBOT}" class="pf-ax"/>')
    for n in LEVELS:
        if n in (7, 9):
            continue
        s.append(f'<line x1="{X0-14}" x2="{X0-10}" y1="{Y(n):.1f}" y2="{Y(n):.1f}" class="pf-ax"/>')
        s.append(f'<text x="{X0-17}" y="{Y(n)+3.3:.1f}" class="pf-tk" text-anchor="end">{n}</text>')
    s.append(f'<text x="{X0-17}" y="{YLIM+3.3}" class="pf-tk" text-anchor="end">∞</text>')
    s.append(f'<path d="M{X0-13},{YLIM+6} l6,-3 M{X0-13},{YLIM+10} l6,-3" class="pf-ax"/>')
    s.append(f'<text x="12" y="{(YTOP+YBOT)/2:.0f}" class="pf-axl" text-anchor="middle" transform="rotate(-90 12 {(YTOP+YBOT)/2:.0f})">n (log scale)</text>')
    # Balmer transitions from n = 2
    trans = [(3, "Hα"), (4, "Hβ"), (5, "Hγ"), (6, "Hδ"), (8, "H8"), (12, "H12"), (20, "H20")]
    y2 = Y(2)
    for k, (n, lab) in enumerate(trans):
        x = 88 + k * 32
        yt = Y(n) + 1.5
        o = 0.25 + 0.75 * w(n)
        s.append(f'<g class="hl-tr" data-o="{o:.2f}">'
                 f'<line x1="{x}" x2="{x}" y1="{y2-1.5:.1f}" y2="{yt+4:.1f}" class="hl-arrow"/>'
                 f'<path d="M{x-3},{yt+6:.1f} L{x},{yt:.1f} L{x+3},{yt+6:.1f}" class="hl-head"/>'
                 f'<text x="{x}" y="{y2+14:.1f}" class="hl-t" text-anchor="middle">{lab}</text></g>')
    xr = X1 + 12
    s.append(f'<text x="{xr}" y="{YLIM-8}" class="hl-r">continuum</text>')
    s.append(f'<text x="{xr}" y="{YLIM+3.5}" class="hl-r">limit</text>')
    s.append(f'<text x="{xr}" y="{Y(2)+3.5:.1f}" class="hl-r">E<tspan dy="2" font-size="7">n</tspan><tspan dy="-2"> = −13.6/n² eV</tspan></text>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    open(os.path.join(HERE, "svg_HL.svg"), "w").write(svg())
    print("ok", {n: round(w(n), 2) for n in LEVELS})
