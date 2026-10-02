"""Wide hero spectrum: Balmer limit -> near-IR on a log-lambda axis, plus the
HTML hotspot overlay for research works. Synthetic placeholder: line positions
are real (air wavelengths), profiles and strengths are approximate."""
import numpy as np, os
from gen_svg import absorb, path, vac2air, voigt

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)

LO = 3560.0
HI = 6562.80 ** 2 / LO          # Hα sits at the log-midpoint of the axis (~1.21 μm)
W, H = 4400, 214
TOP, BOT = 66, 192            # y of flux 1 and flux 0
L0, L1 = np.log(LO), np.log(HI)
X = lambda lam: (np.log(lam) - L0) / (L1 - L0) * W
FRAC = lambda lam: (np.log(lam) - L0) / (L1 - L0)

R = 4500.0                    # display resolution


def spectrum():
    lam = np.exp(np.linspace(L0, L1, 7000))
    sig = lambda c: c / R / 2.3548
    lines = []
    # Balmer series with level dissolution (HM-like suppression of high n)
    RH = 109677.58
    lim = vac2air(1e8 / (RH / 4))
    for n in range(3, 60):
        c = vac2air(1e8 / (RH * (0.25 - 1 / n**2)))
        w = np.exp(-(n / 17.0) ** 5)
        g = 2.6 if n == 3 else min(0.3 * (n / 8) ** 2.1 + 0.6, 0.35 * abs(c - lim) + 0.2)
        lines.append((c, 0.72 * w if n < 14 else 0.6 * w, sig(c), g))
    strong = [(3933.66, .9, 7), (3968.47, .88, 6), (4226.73, .6, .8), (5167.32, .5, .5), (5172.68, .58, .5),
              (5183.60, .62, .5), (5889.95, .72, .5), (5895.92, .66, .5), (8498.02, .5, 1.4), (8542.09, .62, 2.0),
              (8662.14, .58, 1.8), (10827.09, .32, .3), (10830.30, .55, .45),
]
    # P I lines from Jian et al. (2025), Table "List of P I lines" (air wavelengths, within the axis range)
    P_LINES = [9609.036, 9676.222, 9734.755, 9750.748, 9790.194, 9796.828, 9903.671, 9976.681, 10084.277, 10204.716,
               10511.588, 10529.524, 10581.577, 10596.903, 10681.406, 10769.511, 10813.141, 10932.724, 10967.373, 11183.240]
    lines += [(c, d, sig(c), g) for c, d, g in strong]
    lines += [(c, .09, sig(c), .1) for c in P_LINES]
    lines += [(rng.uniform(4296, 4316), .3, sig(4300), .1) for _ in range(30)]          # G band (CH)
    # Paschen series (weak in a solar-type star)
    for n in range(7, 22):
        c = vac2air(1e8 / (RH * (1 / 9 - 1 / n**2)))
        lines.append((c, .12 * np.exp(-(n / 16) ** 4), sig(c), .6))
    # telluric O2 A and B bands (Fraunhofer A, B)
    for start, n_, step, d in ((7594, 34, 1.15, .55), (6867, 24, 1.05, .45)):
        lines += [(start + k * step, d * np.exp(-k / 14), sig(start), .02) for k in range(n_)]
    # weak metal-line forest, denser in the blue
    cand = np.exp(rng.uniform(L0, L1, 9000))
    cand = cand[rng.uniform(0, 1, cand.size) < (cand / LO) ** -3.2][:1100]
    lines += [(c, .3 * rng.uniform() ** 3, sig(c), .02) for c in cand]
    f = absorb(lam, lines)
    jump = np.where(lam < lim, 0.62, 1 - 0.38 * np.exp(-(lam - lim) / 14.0))   # Balmer jump, smeared by dissolution
    return lam, f * jump, lim


def svg():
    lam, f, lim = spectrum()
    px, py = X(lam), BOT - f * (BOT - TOP)
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Synthetic stellar spectrum from the Balmer limit at 3646 Angstrom to 1.1 micron, log wavelength axis">']
    s.append(f'<line x1="0" x2="{W}" y1="{TOP}" y2="{TOP}" class="cont"/>')
    s.append(f'<defs><path id="wide-spec" d="{path(px, py)}"/></defs>')
    s.append('<use href="#wide-spec" class="glow"/><use href="#wide-spec" class="spec"/>')
    # axis
    s.append(f'<line x1="0" x2="{W}" y1="{BOT+6}" y2="{BOT+6}" class="axis"/>')
    for l in range(3700, 12100, 100):
        major = l % 500 == 0
        s.append(f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{BOT+6}" y2="{BOT+(12 if major else 9)}" class="axis"/>')
        if major:
            lab = f"{l} Å" if l < 10000 else f"{l/1e4:.2f} μm"
            s.append(f'<text x="{X(l)+4:.1f}" y="{BOT+22}" class="tkl">{lab}</text>')
    # line identifications: Fraunhofer letter (optional) + species
    ids = [(3933.66, "K", "Ca II", -9), (3968.47, "H", "Ca II", 9), (4101.74, "h", "Hδ", 0), (4307.0, "G", "CH", 0),
           (4340.47, "", "Hγ", 0), (4861.34, "F", "Hβ", 0), (5175.0, "b", "Mg I", 0), (5892.9, "D", "Na I", 0),
           (6562.80, "C", "Hα", 0), (6870.0, "B", "O₂ ⊕", 0), (7600.0, "A", "O₂ ⊕", 0),
           (8542.09, "", "Ca II triplet", 0), (10049.4, "", "Pa δ", 0), (10827.09, "", "Si I", -14), (10938.1, "", "Pa γ", 0)]
    for lam_, letter, sp, dx in ids:
        xx = X(lam_)
        s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{TOP-22}" y2="{TOP-8}" class="tick"/>')
        if letter:
            s.append(f'<text x="{xx+dx:.1f}" y="{TOP-40}" class="fl">{letter}</text>')
        s.append(f'<text x="{xx+dx:.1f}" y="{TOP-26}" class="sp">{sp}</text>')
    s.append(f'<line x1="{X(lim):.1f}" x2="{X(lim):.1f}" y1="{TOP-20}" y2="{BOT}" class="lim"/>')
    s.append('</svg>')
    return "\n".join(s)


WORKS = [  # key, lo, hi, title, subtitle, row, anchor
    ("dissolution", 3640, 3800, "High-n H lines", "Balmer limit · Hummer–Mihalas", 0, "left"),
    ("pysme", 6449, 6679, "PySME", "spectrum synthesis · Hα", 0, "left"),
    ("phosphorus", 9650, 10045, "Phosphorus", "P I 0.97–1.00 μm", 0, "left"),
    ("helium", 10826.3, 10834.3, "He I 10830", "helium in cluster giants", 0, "left"),   # centred on 10830.3
]


def hotspots():
    out, ticks = [], []
    for key, lo, hi, title, sub, row, anchor in WORKS:
        a, b = FRAC(lo), FRAC(hi)
        if b - a < 0.004:                      # very narrow features get a minimum hit width
            m = (a + b) / 2; a, b = m - 0.002, m + 0.002
        out.append(f'<button class="hs row{row} {anchor}" type="button" data-work="{key}" style="left:{a*100:.3f}%;width:{(b-a)*100:.3f}%">'
                   f'<span class="hs-label"><span class="hs-t">{title}</span></span></button>')
        ticks.append(f'<span class="rt" style="left:{(a+b)/2*100:.3f}%"></span>')
    return "\n".join(out), "\n".join(ticks)


if __name__ == "__main__":
    open(os.path.join(HERE, "svg_W.svg"), "w").write(svg())
    hs, rt = hotspots()
    open(os.path.join(HERE, "svg_Whs.svg"), "w").write(hs)
    open(os.path.join(HERE, "svg_Wrt.svg"), "w").write(rt)
    print("ok", FRAC(5175), FRAC(10600))
