"""A small 'survey': PySME syntheses of a line-rich blue window (4560-4585 A) for a sequence of FGK stars (sorted by Teff),
at a 4MOST-HR-like resolution, for the research card II art."""
import json, numpy as np
from pysme.sme import SME_Structure
from pysme.linelist.vald import ValdFile
from pysme.synthesize import synthesize_spectrum
from pysme.abund import Abund

WAVE = np.arange(4560.0, 4585.0, 0.02)
_ll = ValdFile("/Users/mingjie/Documents/Research/Collaboration/jie_lin/codex_workspace/results/fe_fullrange_compare_ts/debug_row01_fullmode/run_20260306_073007/work/vald_trimmed.lin")
_w = np.asarray(_ll["wlcent"])
LL = _ll[(_w > WAVE[0] - 3) & (_w < WAVE[-1] + 3)]
print("lines in window:", len(LL))
STARS = [  # teff, logg, monh, vsini
    (4400, 2.2, -0.3, 3), (4650, 4.6, 0.2, 2), (4800, 2.7, -0.6, 3), (5050, 3.4, 0.0, 4),
    (5300, 4.5, -0.2, 2), (5550, 4.0, -1.0, 5), (5772, 4.44, 0.0, 1.6), (5950, 4.2, 0.25, 6),
    (6150, 3.9, -0.5, 9), (6350, 4.3, -0.1, 12), (6550, 4.1, -0.3, 18)]
rng = np.random.default_rng(5)
out = []
for teff, logg, monh, vsini in STARS:
    sme = SME_Structure()
    sme.abund = Abund.solar()
    sme.teff, sme.logg, sme.monh = teff, logg, monh
    sme.vmic, sme.vmac, sme.vsini = 1.0, 3.0, vsini
    sme.linelist = LL
    sme.atmo.source, sme.atmo.method = "marcs2012.sav", "grid"
    sme.wave = WAVE.copy()
    sme.iptype, sme.ipres = "gauss", 20000
    sme.cscale_flag, sme.vrad_flag = "none", "none"
    f = np.asarray(synthesize_spectrum(sme).synth[0], float)
    f = f + rng.normal(0, 1 / 120, f.size)          # survey-like S/N
    out.append(dict(teff=teff, logg=logg, monh=monh, vsini=vsini, flux=f.round(4).tolist()))
    print(teff, logg, monh, "min %.2f" % f.min())
json.dump(dict(wave=WAVE.round(3).tolist(), stars=out), open("stack/stack.json", "w"))
