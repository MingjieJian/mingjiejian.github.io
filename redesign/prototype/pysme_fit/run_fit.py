"""Real PySME fit for the homepage animation.
'Observed' = PySME solar synthesis + Gaussian noise (S/N 150).
Fit T_eff, log g, [M/H] from a deliberately poor start; every solver
iteration is recorded and re-synthesised for the animation frames."""
import json, os, numpy as np
from pysme.sme import SME_Structure
from pysme.linelist.vald import ValdFile
from pysme.synthesize import synthesize_spectrum
from pysme.solve import solve
from pysme.abund import Abund

HERE = os.path.dirname(os.path.abspath(__file__))
LL = ValdFile("/Users/mingjie/Documents/Research/PySME/worktrees/pysme-fix-marcs-h-he-abundance-scaling/test/testcase1.lin")
WAVE = np.arange(6550.5, 6574.5, 0.02)
TRUE = dict(teff=5772.0, logg=4.44, monh=0.0)
START = dict(teff=5250.0, logg=4.00, monh=-0.40)
SN = 150.0


def base(p):
    sme = SME_Structure()
    sme.abund = Abund.solar()            # set before monh: assigning abund resets monh
    sme.teff, sme.logg, sme.monh = p["teff"], p["logg"], p["monh"]
    sme.vmic, sme.vmac, sme.vsini = 1.0, 3.0, 1.6
    sme.linelist = LL
    sme.atmo.source, sme.atmo.method = "marcs2012.sav", "grid"
    sme.wave = WAVE.copy()
    sme.iptype, sme.ipres = "gauss", 60000
    sme.cscale_flag, sme.vrad_flag = "none", "none"
    return sme


def synth(p):
    return np.asarray(synthesize_spectrum(base(p)).synth[0], float)


truth = synth(TRUE)
rng = np.random.default_rng(42)
obs = truth + rng.normal(0, 1 / SN, truth.size)

sme = base(START)
sme.spec = [obs]
sme.uncs = [np.full(obs.size, 1 / SN)]
sme.mask = [np.ones(obs.size, int)]
fitfile = os.path.join(HERE, "fit.sme")
for f in ("fit_iter.json",):
    if os.path.exists(os.path.join(HERE, f)):
        os.remove(os.path.join(HERE, f))
print("start monh actually set:", sme.monh)
sme = solve(sme, ["teff", "logg", "monh"], filename=fitfile)

it = json.load(open(os.path.join(HERE, "fit_iter.json")))
steps = [dict(START)] + [dict(teff=v["teff"], logg=v["logg"], monh=v["monh"]) for k, v in sorted(it.items(), key=lambda kv: int(kv[0]))]
print("iterations recorded:", len(steps) - 1)
for k, s in enumerate(steps):
    print(k, {n: round(x, 3) for n, x in s.items()})
print("final:", {n: round(float(getattr(sme, n)), 3) for n in ("teff", "logg", "monh")})
print("fit uncertainties:", getattr(sme.fitresults, "fit_uncertainties", None))
out = dict(wave=WAVE.tolist(), obs=obs.tolist(), truth=truth.tolist(), true=TRUE, sn=SN,
           steps=[dict(params=s, flux=synth(s).tolist()) for s in steps])
json.dump(out, open(os.path.join(HERE, "fit_frames.json"), "w"))
print("saved", len(out["steps"]), "frames")
