"""Spectrum frames for the synthesize step: the snippet's spectrum computed with the model atmosphere
truncated from the top (only the deepest layers kept), then with more and more layers added outward,
until the full atmosphere gives the final spectrum. Same PySME call each time, embedded atmosphere."""
import copy, json, numpy as np
from pysme.sme import SME_Structure
from pysme.linelist.vald import ValdFile
from pysme.synthesize import synthesize_spectrum

def base():
    sme = SME_Structure()
    sme.teff, sme.logg, sme.monh = 5772, 4.44, 0.0
    sme.vmic, sme.vmac, sme.vsini = 1.0, 3.6, 1.6
    sme.linelist = ValdFile("/Users/mingjie/Documents/Research/PySME/worktrees/pysme-fix-marcs-h-he-abundance-scaling/test/testcase1.lin")
    sme.wave = np.arange(6550, 6575, 0.02)
    return sme

full = synthesize_spectrum(base())
A = full.atmo
print("ndep", A.ndep, "logtau range", np.log10(A.tau[[0, -1]]))
frames, info = [], []
KEEP = (14, 18, 23, 31, 55)                   # deepest layers kept, one set per highlighted cell
for i0 in [A.ndep - n for n in KEEP]:
    sme = base()
    at = copy.deepcopy(A)
    for k in ("height", "rho", "rhox", "tau", "temp", "xna", "xne"):
        setattr(at, k, getattr(A, k)[i0:])
    at.ndep = A.ndep - i0
    at.method = "embedded"
    sme.atmo = at
    f = np.asarray(synthesize_spectrum(sme).synth[0], float)
    frames.append(np.round(f, 4).tolist()); info.append(float(np.log10(A.tau[i0])))
    print(i0, "top logtau %.2f" % np.log10(A.tau[i0]), "min %.3f" % f.min())
json.dump(dict(wave=np.round(full.wave[0], 3).tolist(), frames=frames, top_logtau=info, keep=list(KEEP),
               final=np.round(full.synth[0], 4).tolist()), open("cells.json", "w"))
