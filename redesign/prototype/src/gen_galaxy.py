"""Card III art: an edge-on Milky Way drawn as a star field sampled from simple density laws
(thin + thick exponential disks, bulge/bar, flattened power-law halo). A sparse 'observed' sample
is picked out in the accent colour; the Sun is marked. Points are zero-length round-capped
path segments, grouped by brightness, to keep the SVG small."""
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)
W, H = 420, 210; cx, cy = 210, 105
KX, KZ = 13.5, 15.0                       # px per kpc (vertical slightly stretched so the disks read)


def disk(n, hr, hz, rmax=16):
    R = rng.gamma(2, hr, n); R = R[R < rmax]
    phi = rng.uniform(0, 2 * np.pi, R.size)
    z = rng.laplace(0, hz, R.size)
    return R * np.cos(phi), z, R * np.sin(phi)


def bulge(n):
    return rng.normal(0, 1.1, n), rng.normal(0, 0.55, n), rng.normal(0, 0.6, n)


def halo(n):
    r = 2.5 * (1 - rng.uniform(0, 0.985, n)) ** (-1 / 2.0)  # ~ r^-3 density
    r = r[r < 22]
    v = rng.normal(size=(r.size, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
    return r * v[:, 0], 0.75 * r * v[:, 1], r * v[:, 2]


parts = [disk(6000, 2.8, 0.2), disk(1300, 2.3, 0.65), bulge(950), halo(280)]
x = np.concatenate([p[0] for p in parts]); z = np.concatenate([p[1] for p in parts])
y = np.concatenate([p[2] for p in parts])
X, Z = cx + x * KX, cy - z * KZ
ok = (X > 4) & (X < W - 4) & (Z > 4) & (Z < H - 4)
X, Z, y = X[ok], Z[ok], y[ok]
# brightness: nearer side (y < 0) a little brighter, plus scatter; 4 bins
b = np.clip(0.5 - 0.02 * y + rng.normal(0, 0.2, X.size), 0, 1)
bins = np.digitize(b, [0.35, 0.55, 0.75])


def pts(sel):
    return "".join(f"M{round(a * 2)} {round(c * 2)}h0" for a, c in zip(X[sel], Z[sel]))   # half-px grid


s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="Schematic edge-on Milky Way drawn as a field of stars, with a sample of observed stars and the Sun marked.">']
for k, (op, sw) in enumerate([(.16, .9), (.28, .95), (.42, 1.0), (.6, 1.1)]):
    s.append(f'<path d="{pts(bins == k)}" class="gx-star" stroke-width="{2 * sw}" opacity="{op}" transform="scale(.5)"/>')
# lines of sight from the Sun, with the stars a spectroscopic survey picks up along each
sx = cx + 8.2 * KX
for ang, L in ((146, 96), (161, 128), (176, 168), (191, 132), (207, 100)):
    t = np.deg2rad(ang); ex, ez = sx + L * np.cos(t), cy - L * np.sin(t)
    s.append(f'<line x1="{sx:.1f}" y1="{cy}" x2="{ex:.1f}" y2="{ez:.1f}" class="gx-los"/>')
    d = np.sort(rng.uniform(12, L, max(3, int(L / 22))))
    s.append(f'<path d="{"".join(f"M{sx + u * np.cos(t):.1f} {cy - u * np.sin(t):.1f}h0" for u in d)}" class="gx-obs"/>')
s += [f'<circle cx="{sx:.1f}" cy="{cy}" r="3.6" class="gx-sun"/>',
      f'<circle cx="{sx:.1f}" cy="{cy}" r=".9" class="gx-sund"/>',
      f'<text x="{sx:.1f}" y="{cy + 20}" class="art-lab" text-anchor="middle">Sun</text>']
s.append('</svg>')
out = "\n".join(s)
open(os.path.join(HERE, "svg_D_galaxy.svg"), "w").write(out)
print("ok", len(out) // 1024, "KB", X.size, "stars")
