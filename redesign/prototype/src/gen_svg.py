"""Generate placeholder spectrum SVGs for the three homepage previews.

Line positions are real (air wavelengths); profiles and strengths are crude
approximations. All figures are labelled as synthetic placeholders.
"""
import numpy as np, os

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)


def vac2air(l):
    s2 = (1e4 / l) ** 2
    n = 1 + 0.0000834254 + 0.02406147 / (130 - s2) + 0.00015998 / (38.9 - s2)
    return l / n


def voigt(x, c, s, g):
    """Pseudo-Voigt with unit peak."""
    fg, fl = 2.3548 * s, 2 * g
    f = (fg**5 + 2.69269*fg**4*fl + 2.42843*fg**3*fl**2 + 4.47163*fg**2*fl**3
         + 0.07842*fg*fl**4 + fl**5) ** 0.2
    r = fl / f
    eta = 1.36603*r - 0.47719*r**2 + 0.11116*r**3
    lor = 1 / (1 + ((x - c) / (f / 2)) ** 2)
    gau = np.exp(-0.5 * ((x - c) / (f / 2.3548)) ** 2)
    return eta * lor + (1 - eta) * gau


def absorb(x, lines):
    tau = np.zeros_like(x)
    for c, d, s, g in lines:
        tau += -np.log(1 - min(d, 0.97)) * voigt(x, c, s, g)
    return np.exp(-tau)


def weak_lines(lo, hi, n, sigma, blue_power=0.0, dmax=0.5):
    lam = rng.uniform(lo, hi, n * 3)
    if blue_power:
        keep = rng.uniform(0, 1, lam.size) < (lam / lo) ** (-blue_power)
        lam = lam[keep]
    lam = lam[:n]
    d = dmax * rng.uniform(0, 1, lam.size) ** 3
    return [(c, dd, sigma, 0.02) for c, dd in zip(lam, d)]


def path(xs, ys):
    pts = [f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys)]
    return "M" + " L".join(pts)


# ---------------------------------------------------------------- A: solar
def make_a():
    W, H = 1200, 210
    top, bot = 70, 200            # y for flux 1.0 and 0.0
    lo, hi = 3880, 6720
    x = np.arange(lo, hi, 1.0)
    inst = 1.1
    strong = [
        (3933.66, .92, 1.0, 7), (3968.47, .90, 1.0, 6),
        (4101.74, .65, 1.0, 2.2), (4226.73, .65, 1.0, .8),
        (4340.47, .68, 1.0, 2.3), (4383.55, .55, 1.0, .4),
        (4861.34, .72, 1.0, 2.4), (5167.32, .55, 1.0, .5),
        (5172.68, .62, 1.0, .5), (5183.60, .66, 1.0, .5),
        (5269.54, .45, 1.0, .3), (5889.95, .72, 1.0, .5),
        (5895.92, .66, 1.0, .5), (6562.80, .78, 1.0, 2.8),
    ]
    gband = [(rng.uniform(4296, 4316), .35, 1.0, .1) for _ in range(40)]
    f = absorb(x, strong + gband + weak_lines(lo, hi, 650, inst, 3.0, .30))
    px = (x - lo) / (hi - lo) * W
    py = bot - f * (bot - top)
    svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
           f'role="img" aria-label="Normalised solar-type spectrum, 3880 to 6720 Angstrom, '
           f'with Fraunhofer lines labelled">']
    svg.append(f'<line x1="0" x2="{W}" y1="{top}" y2="{top}" class="cont"/>')
    svg.append(f'<path d="{path(px, py)}" class="glow"/>')
    svg.append(f'<path d="{path(px, py)}" class="spec"/>')
    # Fraunhofer letters
    labels = [(3933.66, "K", "Ca II"), (3968.47, "H", "Ca II"), (4101.74, "h", "Hδ"),
              (4307.0, "G", "CH"),
              (4861.34, "F", "Hβ"), (5175.0, "b", "Mg I"),
              (5892.9, "D", "Na I"), (6562.80, "C", "Hα")]
    for lam, letter, sp in labels:
        xx = (lam - lo) / (hi - lo) * W
        dx = -8 if letter == "K" else (8 if letter == "H" else 0)
        svg.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="44" y2="58" class="tick"/>')
        if letter:
            svg.append(f'<text x="{xx+dx:.1f}" y="22" class="fl">{letter}</text>')
        svg.append(f'<text x="{xx+dx:.1f}" y="38" class="sp">{sp}</text>')
    svg.append('</svg>')
    return "\n".join(svg)


# ---------------------------------------------------------------- B: Balmer
def make_b():
    W, H = 640, 430
    L, R, T, B = 56, 620, 62, 372
    lo, hi = 3638, 3905
    ylo, yhi = 0.30, 1.10
    x = np.arange(lo, hi, 0.05)
    RH = 109677.58
    lim = vac2air(1e8 / (RH / 4))
    ns = np.arange(8, 70)
    lam_n = vac2air(1e8 / (RH * (0.25 - 1 / ns**2)))

    def model(dissolve):
        if dissolve:
            w = np.exp(-(ns / 17.0) ** 5)
            D = np.where(x < lim, 1.0, np.exp(-(x - lim) / 16.0))
        else:
            w = np.ones_like(ns, float)
            D = np.where(x < lim, 1.0, 0.0)
        cont = 1 - 0.52 * D
        tau = np.zeros_like(x)
        spacing = np.abs(np.gradient(lam_n))
        for n, ln, ww, sp in zip(ns, lam_n, w, spacing):
            g = min(0.28 * (n / 8) ** 2.1, 0.35 * sp)
            tau += 0.95 * ww * voigt(x, ln, 0.25, g)
        return cont * np.exp(-tau)

    hm, nod = model(True), model(False)
    X = lambda l: L + (l - lo) / (hi - lo) * (R - L)
    Y = lambda f: B - (f - ylo) / (yhi - ylo) * (B - T)
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Convergence of the Balmer series towards the series limit at 3646 Angstrom; '
         f'model with and without hydrogen level dissolution compared with observations">']
    # frame + ticks
    s.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" class="frame"/>')
    for l in range(3650, 3901, 10):
        major = l % 50 == 0
        s.append(f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{B}" y2="{B-(7 if major else 4)}" class="ax"/>')
        if major:
            s.append(f'<text x="{X(l):.1f}" y="{B+18}" class="tk" text-anchor="middle">{l}</text>')
    for f in (0.4, 0.6, 0.8, 1.0):
        s.append(f'<line x1="{L}" x2="{L+6}" y1="{Y(f):.1f}" y2="{Y(f):.1f}" class="ax"/>')
        s.append(f'<text x="{L-8}" y="{Y(f)+4:.1f}" class="tk" text-anchor="end">{f:.1f}</text>')
    s.append(f'<text x="{(L+R)/2}" y="{B+42}" class="axl" text-anchor="middle">λ<tspan class="unit"> air [Å]</tspan></text>')
    s.append(f'<text x="18" y="{(T+B)/2}" class="axl" text-anchor="middle" transform="rotate(-90 18 {(T+B)/2})">F / F<tspan dy="3" font-size="8">c</tspan></text>')
    s.append(f'<defs><clipPath id="clipB"><rect x="{L}" y="{T}" width="{R-L}" height="{B-T}"/></clipPath></defs>')
    s.append(f'<g clip-path="url(#clipB)">')
    s.append(f'<line x1="{X(lim):.1f}" x2="{X(lim):.1f}" y1="{T}" y2="{B}" class="limit"/>')
    s.append(f'<path d="{path(X(x), Y(nod))}" class="m-nod"/>')
    # observed: HM + noise, sparse points
    sel = np.arange(0, x.size, 22)
    obs = hm[sel] + rng.normal(0, 0.007, sel.size)
    for xo, yo in zip(X(x[sel]), Y(obs)):
        s.append(f'<circle cx="{xo:.1f}" cy="{yo:.1f}" r="1.25" class="obs"/>')
    s.append(f'<path d="{path(X(x), Y(hm))}" class="m-hm"/>')
    s.append('</g>')
    # line IDs above frame
    for n, ln in zip(ns, lam_n):
        if n > 16:
            break
        xx = X(ln)
        s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{T-12}" y2="{T-3}" class="id"/>')
        s.append(f'<text x="{xx:.1f}" y="{T-17}" class="idt" text-anchor="middle">{n}</text>')
    s.append(f'<text x="{X(3895):.1f}" y="{T-34}" class="idh" text-anchor="end">H<tspan dy="0">n</tspan>  upper level n →</text>')
    s.append(f'<text x="{X(lim)+5:.1f}" y="{T+16}" class="lim">n → ∞</text>')
    s.append(f'<text x="{X(lim)+5:.1f}" y="{T+29}" class="lim">{lim:.1f} Å</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- C: atlas
def make_c_panel(lo, hi, strong, ids, emission=(), step=0.01, nweak=120, tick=1, major=5,
                 hl=None):
    W, H = 1000, 150
    T, B = 46, 136        # flux 1 at T, 0 at B
    x = np.arange(lo, hi, step)
    f = absorb(x, strong + weak_lines(lo, hi, nweak, 0.06, 0, .45))
    for c, a, sg in emission:
        f = f + a * np.exp(-0.5 * ((x - c) / sg) ** 2)
    X = lambda l: (l - lo) / (hi - lo) * W
    Y = lambda v: B - v * (B - T)
    s = [f'<svg viewBox="0 0 {W} {H+16}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Atlas panel {lo} to {hi} Angstrom">']
    if hl:
        s.append(f'<rect x="{X(hl[0]):.1f}" y="{T-6}" width="{X(hl[1])-X(hl[0]):.1f}" height="{B-T+6}" class="hl"/>')
    s.append(f'<line x1="0" x2="{W}" y1="{T}" y2="{T}" class="cont"/>')
    s.append(f'<path d="{path(X(x), Y(np.clip(f, 0, 1.2)))}" class="spec"/>')
    s.append(f'<line x1="0" x2="{W}" y1="{B}" y2="{B}" class="base"/>')
    l = np.ceil(lo / tick) * tick
    while l <= hi:
        mj = abs(l / major - round(l / major)) < 1e-6
        s.append(f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{B}" y2="{B+(6 if mj else 3)}" class="base"/>')
        if mj and 25 < X(l) < W - 25:
            s.append(f'<text x="{X(l):.1f}" y="{B+17}" class="tk" text-anchor="middle">{l:.0f}</text>')
        l += tick
    for k, (lam, lab, cls) in enumerate(ids):
        xx = X(lam)
        row = 14 if k % 2 == 0 else 28
        s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{row+3}" y2="{T-4}" class="id"/>')
        s.append(f'<text x="{xx+3:.1f}" y="{row}" class="idt {cls}">{lab}</text>')
    s.append('</svg>')
    return "\n".join(s)


def make_c():
    panels = []
    panels.append(make_c_panel(
        3925, 3980,
        [(3933.66, .80, .1, 5), (3933.66, .97, .6, .05), (3968.47, .78, .1, 4.5), (3968.47, .96, .55, .05), (3970.07, .45, .1, .9),
         (3944.01, .7, .1, .15), (3961.52, .72, .1, .15)],
        [(3933.66, "Ca II K", "acc"), (3944.01, "Al I", ""), (3961.52, "Al I", ""),
         (3968.47, "Ca II H", "acc"), (3970.07, "Hε", "")],
        emission=[(3933.66, .24, .14), (3968.47, .19, .14)], step=0.03, nweak=110, tick=1, major=10))
    panels.append(make_c_panel(
        5160, 5190,
        [(5167.32, .78, .07, .35), (5172.68, .84, .07, .4), (5183.60, .87, .07, .45),
         (5168.90, .55, .07, .05), (5171.60, .68, .07, .06)],
        [(5167.32, "Mg I", ""), (5168.90, "Fe I", ""), (5171.60, "Fe I", ""),
         (5172.68, "Mg I", ""), (5183.60, "Mg I", "")],
        step=0.015, nweak=150, tick=1, major=5))
    panels.append(make_c_panel(
        5884, 5900,
        [(5889.95, .84, .06, .22), (5895.92, .8, .06, .2), (5892.87, .25, .06, .03),
         (5886.0, .12, .03, .01), (5887.2, .18, .03, .01), (5891.2, .1, .03, .01), (5898.2, .14, .03, .01)],
        [(5887.2, "⊕", "tel"), (5889.95, "Na I D₂", ""), (5892.87, "Ni I", ""),
         (5895.92, "Na I D₁", ""), (5898.2, "⊕", "tel")],
        step=0.008, nweak=70, tick=1, major=2))
    panels.append(make_c_panel(
        6700, 6720,
        [(6703.57, .32, .09, .02), (6705.10, .28, .09, .02), (6707.81, .42, .12, .02),
         (6710.32, .14, .09, .02), (6717.68, .58, .09, .06)],
        [(6703.57, "Fe I", ""), (6705.10, "Fe I", ""), (6707.81, "Li I", "acc"),
         (6710.32, "Fe I", ""), (6717.68, "Ca I", "")],
        step=0.01, nweak=60, tick=1, major=5, hl=(6707.2, 6708.4)))
    return panels


if __name__ == "__main__":
    out = {"A": make_a(), "B": make_b()}
    for i, p in enumerate(make_c()):
        out[f"C{i+1}"] = p
    for k, v in out.items():
        with open(os.path.join(HERE, f"svg_{k}.svg"), "w") as fh:
            fh.write(v)
    print({k: len(v) for k, v in out.items()})
