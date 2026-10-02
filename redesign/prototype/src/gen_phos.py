"""Phosphorus panel: (top) [P/Fe]–age trend redrawn after the talk figure;
(bottom) simplified single-zone chemical-evolution schematic.
TOP-PANEL POINTS ARE TRACED BY EYE FROM A SCREENSHOT — replace with real data
before publishing. Elements carry data-t (ms) for the reveal sequence."""
import os, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(3)

# ---------------------------------------------------------------- trend plot
# A(P) vs age, after Jian et al. (2025) Fig. "age-P" (top panel).
# Data: open clusters and 11 Cepheids from the paper's tables; 8 Cepheids digitised
# from the paper figure (calibrated on the clusters, rms 0.003 dex; no error bars);
# Maas+2019 from VizieR J/AJ/158/219 with A(P)_sun = 5.41. Fits: OLS of A(P) on log age.
import json
PD = json.load(open(os.path.join(HERE, "..", "p_paper", "p_age_data.json")))
PW, PH = 420, 168
PL, PR, PT, PB = 40, 412, 8, 140
TLO, THI = 0.008, 18.0
ALO, AHI = 4.78, 6.08
sx = lambda t: PL + (np.log10(t) - np.log10(TLO)) / (np.log10(THI) - np.log10(TLO)) * (PR - PL)
sy = lambda a: PB - (a - ALO) / (AHI - ALO) * (PB - PT)


def starpts(cx, cy, r=3.4):
    return " ".join(f"{cx + rr*np.sin(a):.1f},{cy - rr*np.cos(a):.1f}" for a, rr in zip(np.arange(10) * np.pi / 5, [r, r*0.42] * 5))


def plot():
    s = [f'<svg viewBox="0 0 {PW} {PH}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Phosphorus abundance A(P) against age for open clusters and Cepheids, with Maas et al. 2019 field stars for '
         f'reference: a mild decrease with age below 1 Gyr and an increase with age above 1 Gyr">']
    s.append(f'<defs><clipPath id="ph-clip"><rect x="{PL}" y="{PT}" width="{PR-PL}" height="{PB-PT}"/></clipPath></defs>')
    s.append('<g clip-path="url(#ph-clip)">')
    for m in PD["maas"]:
        x, y = sx(m["t"]), sy(m["A"])
        s.append(f'<g class="ph-grey" data-t="200"><path d="M{sx(m["tlo"]):.1f},{y:.1f}H{sx(m["thi"]):.1f}M{x:.1f},{sy(m["A"]-m["eA"]):.1f}V{sy(m["A"]+m["eA"]):.1f}" class="ph-eb"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.5"/></g>')
    for k, o in enumerate(sorted(PD["oc"], key=lambda o: o["t"])):
        x, y = sx(o["t"]), sy(o["A"])
        s.append(f'<g class="ph-blue" data-t="{350 + k*30}"><path d="M{x:.1f},{sy(o["A"]-o["eA"]):.1f}V{sy(o["A"]+o["eA"]):.1f}" class="ph-eb"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5"/></g>')
    for k, c in enumerate(sorted(PD["ceph"], key=lambda c: c["t"])):
        x, y = sx(c["t"]), sy(c["A"])
        eb = ""
        if c["eA"] is not None:
            eb = f'<path d="M{sx(c["t"]-c["et"]):.1f},{y:.1f}H{sx(c["t"]+c["et"]):.1f}M{x:.1f},{sy(c["A"]-c["eA"]):.1f}V{sy(c["A"]+c["eA"]):.1f}" class="ph-eb"/>'
        s.append(f'<g class="ph-orange" data-t="{350 + k*30}">{eb}<polygon points="{starpts(x, y)}"/></g>')
    for key, cls, t0 in (("orange", "ph-o-fit", 1100), ("blue_young", "ph-b-fit", 1250), ("blue_old", "ph-b-fit", 1400)):
        f = PD["fits"][key]; ta, tb = f["t"]
        ya, yb = np.polyval(f["p"], np.log10(ta)), np.polyval(f["p"], np.log10(tb))
        s.append(f'<line x1="{sx(ta):.1f}" y1="{sy(ya):.1f}" x2="{sx(tb):.1f}" y2="{sy(yb):.1f}" class="{cls} ph-draw" pathLength="1" data-t="{t0}"/>')
    s.append('</g>')
    s.append(f'<path d="M{PL},{PT}V{PB}H{PR}" class="pf-ax" fill="none"/>')
    for tv, lab in ((0.01, "0.01"), (0.1, "0.1"), (1, "1"), (10, "10")):
        s.append(f'<line x1="{sx(tv):.1f}" x2="{sx(tv):.1f}" y1="{PB}" y2="{PB+4}" class="pf-ax"/>')
        s.append(f'<text x="{sx(tv):.1f}" y="{PB+14}" class="pf-tk" text-anchor="middle">{lab}</text>')
    s.append(f'<text x="{PR}" y="{PB+26}" class="pf-axl" text-anchor="end">age (Gyr)</text>')
    for av in (5.0, 5.5, 6.0):
        s.append(f'<line x1="{PL-4}" x2="{PL}" y1="{sy(av):.1f}" y2="{sy(av):.1f}" class="pf-ax"/>')
        s.append(f'<text x="{PL-7}" y="{sy(av)+3.3:.1f}" class="pf-tk" text-anchor="end">{av:.1f}</text>')
    s.append(f'<text x="10" y="{(PT+PB)/2:.0f}" class="pf-axl" text-anchor="middle" transform="rotate(-90 10 {(PT+PB)/2:.0f})">A(P)</text>')
    lx, ly = PL + 8, sy(5.08)
    s.append(f'<g class="ph-orange" data-t="200"><polygon points="{starpts(lx+3, ly)}"/></g><text x="{lx+11}" y="{ly+3.3:.1f}" class="ph-lg" data-t="200">Cepheids</text>')
    s.append(f'<g class="ph-blue" data-t="200"><circle cx="{lx+3}" cy="{ly+12:.1f}" r="2.5"/></g><text x="{lx+11}" y="{ly+15.3:.1f}" class="ph-lg" data-t="200">open clusters</text>')
    s.append(f'<g class="ph-grey" data-t="200"><circle cx="{lx+3}" cy="{ly+24:.1f}" r="1.5"/></g><text x="{lx+11}" y="{ly+27.3:.1f}" class="ph-lg" data-t="200">Maas+2019</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- schematic
# Layout follows the talk figure (1632 x 350 px frame): element coordinates are
# taken from it directly; only the two horizontal flow arrows are shortened.
SW, SH = 1360, 356
DY = 0
DX2 = -70                    # shift of the second cloud (first flow arrow shortened)
TEL = 1270                   # telescope x (second flow arrow shortened)


def cloud(cx, cy, rx, ry, cls, t):
    """Bumpy cloud: a filled ellipse with overlapping circles around its rim."""
    parts = [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-40}" ry="{ry-40}"/>']
    for k in range(16):
        a = 2 * np.pi * k / 16 + 0.2
        r = 58 + 10 * np.sin(3 * a + 1)
        parts.append(f'<circle cx="{cx + (rx-50)*np.cos(a):.0f}" cy="{cy + (ry-50)*np.sin(a):.0f}" r="{r:.0f}"/>')
    return f'<g class="{cls}" data-t="{t}">{"".join(parts)}</g>'


def star(cx, cy, r, cls, t):
    pts = " ".join(f"{cx + rr*np.sin(a):.1f},{cy - rr*np.cos(a):.1f}" for a, rr in zip(np.arange(8) * np.pi / 4, [r, r*0.2] * 4))
    return f'<polygon points="{pts}" class="{cls}" data-t="{t}"/>'


def arrow(x1, y1, x2, y2, cls, t, head=16):
    a = np.arctan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - head*np.cos(a - .5), y2 - head*np.sin(a - .5)
    hx2, hy2 = x2 - head*np.cos(a + .5), y2 - head*np.sin(a + .5)
    return (f'<g class="{cls}" data-t="{t}"><line x1="{x1}" y1="{y1}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
            f'<path d="M{hx1:.1f},{hy1:.1f} L{x2:.1f},{y2:.1f} L{hx2:.1f},{hy2:.1f}"/></g>')


def txt(x, y, s_, cls, t, anchor="start", rot=None):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" data-t="{t}"{tr}>{s_}</text>'


def telescope(x, y, t):
    """Outline telescope after the icon supplied: tilted tube with rings, eyepiece, pivot, tripod."""
    tube = (f'<g transform="rotate(-32 {x+30} {y})">'
            f'<rect x="{x}" y="{y-11}" width="62" height="22" rx="3"/>'
            f'<line x1="{x+14}" y1="{y-11}" x2="{x+14}" y2="{y+11}"/><line x1="{x+20}" y1="{y-11}" x2="{x+20}" y2="{y+11}"/>'
            f'<rect x="{x+62}" y="{y-14}" width="10" height="28" rx="2"/>'
            f'<rect x="{x-12}" y="{y-6}" width="12" height="12" rx="2"/></g>')
    mount = (f'<circle cx="{x+30}" cy="{y+22}" r="5"/>'
             f'<line x1="{x+30}" y1="{y+27}" x2="{x+30}" y2="{y+44}"/>'
             f'<path d="M{x+30},{y+44} L{x+14},{y+82} M{x+30},{y+44} L{x+30},{y+84} M{x+30},{y+44} L{x+46},{y+82}"/>')
    return f'<g class="ph-scope" data-t="{t}">{tube}{mount}</g>'


def schematic():
    T0 = 1700
    P = lambda x, y: (x, y + DY)                 # cloud 1: talk-figure coordinates
    Q = lambda x, y: (x + DX2, y + DY)           # cloud 2: shifted left
    s = [f'<svg viewBox="0 0 {SW} {SH}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Schematic: in a low-metallicity cloud, massive stars produce much iron and phosphorus and AGB stars a '
         f'little phosphorus; in a later, metal-rich cloud, massive stars produce less and AGB stars more phosphorus, so the '
         f'clusters we observe are slightly enriched in phosphorus">']
    # ---- cloud 1 (low Z)
    s.append(cloud(228, 172 + DY, 228, 172, "ph-cloud-lo", T0))
    s.append(txt(*P(70, 128), "Massive stars", "ph-sm", T0 + 150, rot=-27))
    s.append(star(*P(205, 100), 44, "ph-star", T0 + 150)); s.append(star(*P(115, 160), 44, "ph-star", T0 + 150))
    s.append(arrow(*P(262, 103), *P(326, 120), "ph-ar", T0 + 350))
    s.append(txt(*P(338, 108), "Fe↑↑,", "ph-yl", T0 + 350)); s.append(txt(*P(346, 142), "P↑↑", "ph-yl", T0 + 350))
    s.append(arrow(*P(370, 160), *P(376, 222), "ph-ar", T0 + 500))
    s.append(star(*P(210, 205), 30, "ph-star", T0 + 200)); s.append(star(*P(160, 245), 30, "ph-star", T0 + 200))
    s.append(arrow(*P(244, 205), *P(287, 186), "ph-ar", T0 + 450))
    s.append(txt(*P(296, 190), "P↑", "ph-yl", T0 + 450))
    s.append(arrow(*P(314, 208), *P(330, 246), "ph-ar", T0 + 550))
    s.append(txt(*P(150, 306), "AGB stars", "ph-sm", T0 + 200, rot=-27))
    # ---- flow 1
    s.append(arrow(*P(458, 172), *Q(662, 172), "ph-flow", T0 + 750, head=18))
    # ---- cloud 2 (high Z)
    s.append(cloud(890 + DX2, 172 + DY, 225, 172, "ph-cloud-hi", T0 + 950))
    s.append(star(*Q(770, 160), 44, "ph-star2", T0 + 1100))
    s.append(arrow(*Q(834, 152), *Q(986, 123), "ph-ar", T0 + 1300))
    s.append(txt(*Q(1000, 108), "Fe↑,", "ph-yl", T0 + 1300)); s.append(txt(*Q(1008, 142), "P↑", "ph-yl", T0 + 1300))
    s.append(arrow(*Q(1028, 156), *Q(1034, 218), "ph-ar", T0 + 1450))
    for xy in ((865, 205), (815, 245), (885, 258)):
        s.append(star(*Q(*xy), 28, "ph-star2", T0 + 1150))
    s.append(arrow(*Q(904, 203), *Q(946, 186), "ph-ar", T0 + 1400))
    s.append(txt(*Q(952, 190), "P↑↑", "ph-yl", T0 + 1400))
    s.append(arrow(*Q(972, 206), *Q(986, 246), "ph-ar", T0 + 1500))
    # ---- flow 2 and observer
    x0 = 1118 + DX2
    s.append(arrow(x0, 172 + DY, TEL - 14, 172 + DY, "ph-flow", T0 + 1700, head=18))
    xm = (x0 + TEL - 14) / 2
    s.append(txt(xm, 172 + DY + 46, "P slightly", "ph-yl2", T0 + 1850, "middle"))
    s.append(txt(xm, 172 + DY + 80, "enriched", "ph-yl2", T0 + 1850, "middle"))
    s.append(telescope(TEL, 150 + DY, T0 + 1700))
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    open(os.path.join(HERE, "svg_PH1.svg"), "w").write(plot())
    open(os.path.join(HERE, "svg_PH2.svg"), "w").write(schematic())
    print("ok")
