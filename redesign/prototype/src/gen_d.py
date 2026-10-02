"""SVG art for preview D (dark 'observatory' variant)."""
import numpy as np, os
from gen_svg import absorb, weak_lines, path, vac2air, rng

HERE = os.path.dirname(os.path.abspath(__file__))


def hero():
    W, H = 1440, 186
    top, bot = 50, 172
    lo, hi = 3860, 6760
    x = np.arange(lo, hi, 1.0)
    strong = [(3933.66, .9, 1, 7), (3968.47, .88, 1, 6), (4101.74, .65, 1, 2.2), (4226.73, .6, 1, .8),
              (4340.47, .68, 1, 2.3), (4861.34, .72, 1, 2.4), (5167.32, .5, 1, .5), (5172.68, .58, 1, .5),
              (5183.60, .62, 1, .5), (5889.95, .72, 1, .5), (5895.92, .66, 1, .5), (6562.80, .78, 1, 2.8)]
    gband = [(rng.uniform(4296, 4316), .3, 1, .1) for _ in range(30)]
    f = absorb(x, strong + gband + weak_lines(lo, hi, 380, 1.1, 3.0, .22))
    X = (x - lo) / (hi - lo) * W
    Y = bot - f * (bot - top)
    s = [f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    for l in range(4000, 6800, 100):
        xx = (l - lo) / (hi - lo) * W
        s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{top-30}" y2="{bot}" class="grid"/>')
        if l % 500 == 0:
            s.append(f'<text x="{xx+4:.1f}" y="{bot-4}" class="gl">{l}</text>')
    s.append(f'<path d="{path(X, Y)}" class="glow"/>')
    s.append(f'<path d="{path(X, Y)}" class="spec"/>')
    for lam, lab in [(3933.66, "Ca II K"), (4101.74, "Hδ"), (4340.47, "Hγ"), (4861.34, "Hβ"),
                     (5172.7, "Mg I b"), (5892.9, "Na I D"), (6562.80, "Hα")]:
        xx = (lam - lo) / (hi - lo) * W
        s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{top-24}" y2="{top-8}" class="tick"/>')
        s.append(f'<text x="{xx:.1f}" y="{top-30}" class="lab" text-anchor="middle">{lab}</text>')
    s.append('</svg>')
    return "\n".join(s)


def balmer_art():
    W, H = 560, 300
    RH = 109677.58
    lim = vac2air(1e8 / (RH / 4))
    lo, hi = 3630, 4120
    X = lambda l: 30 + (l - lo) / (hi - lo) * (W - 60)
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    s.append(f'<line x1="20" x2="{W-20}" y1="250" y2="250" class="art-base"/>')
    for n in range(6, 60):
        l = vac2air(1e8 / (RH * (0.25 - 1 / n**2)))
        a = max(0.12, 1 - (n - 6) / 30)
        h = 40 + 150 * a
        s.append(f'<line x1="{X(l):.1f}" x2="{X(l):.1f}" y1="{250-h:.0f}" y2="250" class="art-line" opacity="{a:.2f}"/>')
        if n <= 12:
            lab = {6: "Hδ", 7: "Hε"}.get(n, f"H{n}")
            s.append(f'<text x="{X(l):.1f}" y="{250-h-8:.0f}" class="art-lab" text-anchor="middle">{lab}</text>')
    s.append(f'<line x1="{X(lim):.1f}" x2="{X(lim):.1f}" y1="40" y2="262" class="art-lim"/>')
    s.append(f'<text x="{X(lim)+6:.1f}" y="52" class="art-lab">n → ∞</text>')
    s.append(f'<text x="{X(lim)+6:.1f}" y="275" class="art-lab">3646 Å</text>')
    s.append('</svg>')
    return "\n".join(s)


def stack_art():
    W, H = 420, 210
    x = np.linspace(5160, 5190, 500)
    base = [(5167.32, .7, .08, .35), (5172.68, .75, .08, .4), (5183.60, .78, .08, .45)]
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    for k in range(11):
        f = absorb(x, base + weak_lines(5160, 5190, 14, .1, 0, .3)) + rng.normal(0, .004, x.size)
        y0 = 16 + k * 16
        Xp = 20 + (x - 5160) / 30 * (W - 40)
        s.append(f'<path d="{path(Xp, y0 + 22 - f*22)}" class="art-spec" opacity="{1 - k*0.075:.2f}"/>')
    s.append('</svg>')
    return "\n".join(s)


def star_art():
    W, H = 420, 210
    cx, cy = 210, 105
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="180" ry="26" class="art-disk"/>')
    s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="130" ry="18" class="art-disk" opacity=".6"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="52" class="art-star"/>')
    for dx, dy, r in [(-18, -20, 7), (14, 8, 5), (-4, 26, 4)]:
        s.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" class="art-spot"/>')
    s.append(f'<path d="M{cx-52},{cy} A52,14 0 0 0 {cx+52},{cy}" class="art-eq"/>')
    s.append(f'<line x1="{cx}" y1="{cy-78}" x2="{cx}" y2="{cy-58}" class="art-eq"/>')
    s.append(f'<path d="M{cx-12},{cy-70} q12,-8 24,0" class="art-eq"/>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for k, fn in {"D_hero": hero, "D_balmer": balmer_art, "D_stack": stack_art, "D_star": star_art}.items():
        open(os.path.join(HERE, f"svg_{k}.svg"), "w").write(fn())
    print("ok")
