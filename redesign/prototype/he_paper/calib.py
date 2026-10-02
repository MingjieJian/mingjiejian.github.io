import re, numpy as np, json
txt = open("content.txt").read()
def series(sym):
    """cumulative translations inside each q ... Q block that draws symbol `sym`"""
    pts = []
    for blk in re.findall(r"q\n(.*?)\nQ", txt, re.S):
        if f"/{sym} Do" not in blk: continue
        x = y = 0.0; first = True
        for a, b, s in re.findall(r"([-\d.]+) ([-\d.]+) cm\s*/(M\d+) Do", blk):
            x, y = (float(a), float(b)) if first else (x + float(a), y + float(b)); first = False
            pts.append((x, y))
    return np.array(pts)
s2, sm = series("M0"), series("M1")
print("stock2", len(s2), "smith", len(sm))
ST = {"g1":(-5.42,103,16),"g2":(-4.62,356,15),"g3":(-5.15,112,13),"g4":(-5.14,63,13),"g5":(-4.85,399,23),
      "g6":(-5.05,136,11),"g7":(-5.44,84,15),"g9":(-5.17,90,17),"g10":(-4.58,472,13)}
vals = np.array(list(ST.values()))
# match by rank: sort both by x, then fit linear maps
order_p = np.argsort(s2[:,0]); order_v = np.argsort(vals[:,0])
P, V = s2[order_p], vals[order_v]
ax, bx = np.polyfit(P[:,0], V[:,0], 1); ay, by = np.polyfit(P[:,1], V[:,1], 1)
rx = V[:,0] - (ax*P[:,0]+bx); ry = V[:,1] - (ay*P[:,1]+by)
print(f"x residual rms {np.sqrt((rx**2).mean()):.4f} dex ; y residual rms {np.sqrt((ry**2).mean()):.2f} mA")
sm_v = np.column_stack([ax*sm[:,0]+bx, ay*sm[:,1]+by])
for r in sorted(sm_v.tolist()): print(f"  {r[0]:.3f} {r[1]:.1f}")
json.dump(dict(stock2=[dict(name=k, logR=v[0], EW=v[1], eEW=v[2]) for k, v in ST.items()],
               smith=[dict(logR=round(a, 3), EW=round(b, 1)) for a, b in sm_v]), open("he_data.json", "w"), indent=1)
