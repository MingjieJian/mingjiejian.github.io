import numpy as np, json
OC = json.load(open("digitised.json"))["oc"]
cand = json.load(open("ceph_digitised.json"))
# drop the two overlap artefacts identified by eye (x=383 at 0.055 Gyr, x=443/444 at 0.093 Gyr)
ceph = [c for c in cand if not (abs(c[0]-0.055) < 0.0015 and abs(c[1]-5.533) < 0.01) and not (abs(c[0]-0.0935) < 0.0015 and abs(c[1]-5.757) < 0.01)]
KNOWN = {  # star: (age, e_age, A, e_A) from the paper's Table (first 11 Cepheids)
 "SV Vul": (0.016,.003,5.88,.09), "DL Cas": (0.051,.009,5.52,.23), "CO Aur": (0.096,.009,5.73,.17), "RX Aur": (0.039,.007,5.61,.07),
 "V351 Cep": (0.080,.008,5.97,.08), "CD Cyg": (0.031,.006,5.65,.08), "V1334 Cyg": (0.075,.008,5.61,.13), "VZ Cyg": (0.071,.013,5.65,.25),
 "X Cyg": (0.031,.006,5.43,.07), "W Gem": (0.051,.009,5.39,.18), "RR Lac": (0.059,.011,5.54,.09)}
out_c = []
used = set()
for t, A, _ in ceph:
    m = [k for k, v in KNOWN.items() if k not in used and abs(np.log10(v[0]/t)) < 0.03 and abs(v[2]-A) < 0.02]
    if m:
        v = KNOWN[m[0]]; used.add(m[0]); out_c.append(dict(t=v[0], et=v[1], A=v[2], eA=v[3], src="table", name=m[0]))
    else:
        out_c.append(dict(t=round(t, 4), et=None, A=round(A, 3), eA=None, src="figure"))
print("Cepheids:", len(out_c), "from table:", sum(c["src"] == "table" for c in out_c), "digitised:", sum(c["src"] == "figure" for c in out_c))
D = np.load("maas.npy")
maas = [dict(t=r[0], tlo=r[1], thi=r[2], A=round(r[3]+r[4]+5.41, 3), eA=r[5]) for r in D if np.all(np.isfinite(r))]
# fits: A(P) vs log10(age), ordinary least squares
oc = np.array([(t, A) for t, A, e in OC])
def fit(t, A): return np.polyfit(np.log10(t), A, 1)
young, old = oc[oc[:,0] < 1], oc[oc[:,0] >= 1]
cy = np.array([(c["t"], c["A"]) for c in out_c])
f_by, f_bo = fit(*young.T), fit(*old.T)
both = np.vstack([young, cy]); f_o = fit(*both.T)
ev = lambda p, t: np.polyval(p, np.log10(t))
print(f"blue young: {ev(f_by,0.04):.3f} @0.04 -> {ev(f_by,0.68):.3f} @0.68   (paper figure ~5.50 -> ~5.41)")
print(f"blue old  : {ev(f_bo,1.17):.3f} @1.17 -> {ev(f_bo,4.27):.3f} @4.27   (paper figure ~5.35 -> ~5.65)")
print(f"orange    : {ev(f_o,0.012):.3f} @0.012 -> {ev(f_o,0.68):.3f} @0.68  (paper figure ~5.72 -> ~5.40)")
json.dump(dict(oc=[dict(t=t, A=A, eA=e) for t, A, e in OC], ceph=out_c, maas=maas,
               fits=dict(blue_young=dict(p=list(f_by), t=[min(young[:,0]), max(young[:,0])]),
                         blue_old=dict(p=list(f_bo), t=[min(old[:,0]), max(old[:,0])]),
                         orange=dict(p=list(f_o), t=[min(both[:,0]), max(both[:,0])]))),
          open("p_age_data.json", "w"), indent=1)
