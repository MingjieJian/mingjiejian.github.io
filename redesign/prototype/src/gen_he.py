"""He I 10830 panel: EW of the main He I component vs log R'HK, after Jian et al.
(2024, A&A 687, A189) Fig. "stock-2-Ca-He".
Stock 2: exact values from the paper's results table.
Smith+2016: marker positions read from the vector PDF figure in the arXiv source
(calibrated on the 9 Stock 2 stars: rms 0.003 dex, 0.2 mÅ) and rounded to the
tabulated precision. Fits: ordinary least squares of EW on log R'HK."""
import json, os, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "he_paper", "he_data.json")))
ST = [(s["logR"], s["EW"], s["eEW"]) for s in D["stock2"]]
SM = [(round(p["logR"], 2), float(round(p["EW"]))) for p in D["smith"]]

W, H = 420, 214
L, R, T, B = 46, 412, 10, 178
XLO, XHI = -5.58, -4.22
YLO, YHI = -30, 520
X = lambda v: L + (v - XLO) / (XHI - XLO) * (R - L)
Y = lambda v: B - (v - YLO) / (YHI - YLO) * (B - T)


def fit(pts):
    x, y = np.array(pts)[:, 0], np.array(pts)[:, 1]
    p = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    return p, r


def svg():
    p_st, r_st = fit([(a, b) for a, b, _ in ST])
    p_sm, r_sm = fit(SM)
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Equivalent width of the He I 10830 main component against the Ca II H and K activity index log R prime HK: '
         f'Stock 2 red-clump giants (r = {r_st:.2f}) lie above and follow a steeper relation than the dwarfs of Smith et al. 2016 (r = {r_sm:.2f})">']
    s.append(f'<defs><clipPath id="he-clip"><rect x="{L}" y="{T}" width="{R-L}" height="{B-T}"/></clipPath></defs>')
    s.append('<g clip-path="url(#he-clip)">')
    for k, (a, b) in enumerate(sorted(SM)):
        s.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="1.9" class="he-sm" data-t="{200 + k*12}"/>')
    for k, (a, b, e) in enumerate(sorted(ST)):
        s.append(f'<g class="he-st" data-t="{900 + k*60}"><circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="3"/></g>')
    # fit lines over the ranges used in the paper figure
    for p, (xa, xb), cls, t in ((p_sm, (-5.2, -4.3), "he-fit-sm", 1500), (p_st, (-5.4, -4.6), "he-fit-st", 1700)):
        draw = ' ph-draw" pathLength="1' if cls == "he-fit-st" else ""   # the dashed line fades in (draw-on would overwrite its dashes)
        s.append(f'<line x1="{X(xa):.1f}" y1="{Y(np.polyval(p, xa)):.1f}" x2="{X(xb):.1f}" y2="{Y(np.polyval(p, xb)):.1f}" '
                 f'class="{cls}{draw}" data-t="{t}"/>')
    s.append('</g>')
    s.append(f'<path d="M{L},{T}V{B}H{R}" class="pf-ax" fill="none"/>')
    for v in (-5.4, -5.0, -4.6):
        s.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{B}" y2="{B+4}" class="pf-ax"/>')
        s.append(f'<text x="{X(v):.1f}" y="{B+14}" class="pf-tk" text-anchor="middle">{v:.1f}</text>')
    s.append(f'<text x="{R}" y="{B+28}" class="pf-axl" text-anchor="end">log R′<tspan dy="2.5" font-size="7">HK</tspan></text>')
    for v in (0, 200, 400):
        s.append(f'<line x1="{L-4}" x2="{L}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="pf-ax"/>')
        s.append(f'<text x="{L-7}" y="{Y(v)+3.3:.1f}" class="pf-tk" text-anchor="end">{v}</text>')
    s.append(f'<text x="11" y="{(T+B)/2:.0f}" class="pf-axl" text-anchor="middle" transform="rotate(-90 11 {(T+B)/2:.0f})">EW (mÅ)</text>')
    # legend, upper left
    lx, ly = L + 10, T + 14
    s.append(f'<g class="he-st" data-t="200"><circle cx="{lx}" cy="{ly}" r="3"/></g>'
             f'<text x="{lx+9}" y="{ly+3.3}" class="ph-lg" data-t="200">Stock 2 giants</text>')
    s.append(f'<circle cx="{lx}" cy="{ly+14}" r="1.9" class="he-sm" data-t="200"/>'
             f'<text x="{lx+9}" y="{ly+17.3}" class="ph-lg" data-t="200">Smith+2016 dwarfs</text>')
    s.append('</svg>')
    return "\n".join(s), p_st, r_st, p_sm, r_sm


if __name__ == "__main__":
    out, p_st, r_st, p_sm, r_sm = svg()
    open(os.path.join(HERE, "svg_HE.svg"), "w").write(out)
    print(f"Stock 2  r = {r_st:.3f}  line {np.polyval(p_st, -5.4):.0f} -> {np.polyval(p_st, -4.6):.0f} mÅ  (paper figure: r 0.89, ~40 -> ~405)")
    print(f"Smith+16 r = {r_sm:.3f}  line {np.polyval(p_sm, -5.2):.0f} -> {np.polyval(p_sm, -4.3):.0f} mÅ  (paper figure: r 0.78, ~-20 -> ~220)")
