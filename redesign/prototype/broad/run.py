"""One Ca I 6162 line in the solar model, broadening switched on step by step (PySME)."""
import json, numpy as np
from pysme.sme import SME_Structure
from pysme.linelist.vald import ValdFile
from pysme.synthesize import synthesize_spectrum
from pysme.abund import Abund

WAVE = np.arange(6159.7, 6164.65, 0.005)

def synth(pressure, vsini, ipres):
    sme = SME_Structure()
    sme.abund = Abund.solar()
    sme.teff, sme.logg, sme.monh = 5772.0, 4.44, 0.0
    sme.vmic, sme.vmac, sme.vsini = 0.0, 0.0, vsini
    sme.linelist = ValdFile("ca6162.lin" if pressure else "ca6162_nodamp.lin")
    sme.atmo.source, sme.atmo.method = "marcs2012.sav", "grid"
    sme.wave = WAVE.copy()
    if ipres: sme.iptype, sme.ipres = "gauss", ipres
    else: sme.ipres = 0
    sme.cscale_flag, sme.vrad_flag = "none", "none"
    return np.asarray(synthesize_spectrum(sme).synth[0], float)

steps = {"thermal": synth(False, 0, 0), "pressure": synth(True, 0, 0),
         "rotation": synth(True, 12, 0), "instrument": synth(True, 12, 15000)}
for k, f in steps.items():
    ew = np.trapezoid(1 - f, WAVE) * 1000
    print(k, "min %.3f  EW %.0f mA" % (f.min(), ew))
json.dump(dict(wave=WAVE.tolist(), **{k: v.tolist() for k, v in steps.items()}), open("broad.json", "w"))
