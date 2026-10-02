"""Wide hero spectrum: Balmer limit -> near-IR on a log-lambda axis (Kitt Peak solar
flux atlas), plus the HTML hotspot overlay for research works."""
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
    """Real data: Kitt Peak FTS solar flux atlas (Kurucz et al. 1984), residual flux,
    smoothed to R ~ 6000 on a log-lambda grid (../solar/prep_solar.py). Ground-based, so the
    telluric O2 (Fraunhofer A, B) and H2O bands are real."""
    lam, f = np.load(os.path.join(HERE, "..", "solar", "solar_R6000.npy"))
    RH = 109677.58
    lim = vac2air(1e8 / (RH / 4))
    return lam, f, lim


def svg():
    lam, f, lim = spectrum()
    px, py = X(lam), BOT - f * (BOT - TOP)
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Solar flux spectrum (Kitt Peak FTS atlas) from the Balmer limit at 3646 Angstrom to 1.1 micron, log wavelength axis">']
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


BALMER_LIMIT = vac2air(1e8 / (109677.58 / 4))     # band starts exactly at the series limit (same value as the dashed marker)
WORKS = [  # key, lo, hi, title, subtitle, row, anchor
    ("dissolution", BALMER_LIMIT, 3800, "High-n H lines", "Balmer limit · Hummer–Mihalas", 0, "left"),
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
