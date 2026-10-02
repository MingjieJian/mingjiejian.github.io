"""Exactly the PySME snippet shown on the homepage (software section), run for real;
the result is drawn as the output spectrum of the pipeline diagram."""
import json, numpy as np
from pysme.sme import SME_Structure
from pysme.linelist.vald import ValdFile
from pysme.synthesize import synthesize_spectrum

sme = SME_Structure()
sme.teff, sme.logg, sme.monh = 5772, 4.44, 0.0
sme.vmic, sme.vmac, sme.vsini = 1.0, 3.6, 1.6
sme.linelist = ValdFile("/Users/mingjie/Documents/Research/PySME/worktrees/pysme-fix-marcs-h-he-abundance-scaling/test/testcase1.lin")
sme.wave = np.arange(6550, 6575, 0.02)

sme = synthesize_spectrum(sme)
print("atmo:", sme.atmo.source, sme.atmo.method, "ipres:", sme.ipres)
json.dump(dict(wave=np.round(sme.wave[0], 3).tolist(), flux=np.round(sme.synth[0], 4).tolist()), open("codeanim/snippet.json", "w"))
print("min flux", float(np.min(sme.synth[0])))
