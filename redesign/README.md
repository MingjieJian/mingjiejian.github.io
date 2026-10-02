# Homepage redesign — prototype

Work in progress; the live site (Jekyll, repository root) is untouched.

Open `prototype/index.html` through a local server (the portrait canvas reads image pixels, which browsers block on `file://`):

```bash
python3 -m http.server 8765 --directory redesign/prototype
```

## What is here

- **Design**: serif editorial layout (Spectral / Spectral SC / JetBrains Mono); paper theme by default, night theme follows the system, with an Auto / Light / Dark toggle. Switching theme must not move any text.
- **Hero**: "Between physics / *and the sky.*", a log-λ spectrum strip (Balmer limit → 1.21 μm, Hα at the centre) that pans opposite to the pointer, and four work bands that open figures in the right-hand panel:
  - **High-n H lines** — level-dissolution schematic (ongoing work; no claims stated)
  - **PySME** — animated real PySME fit (`pysme_fit/run_fit.py`)
  - **Phosphorus** — A(P)–age from Jian et al. 2025 (`p_paper/`) + chemical-evolution schematic
  - **He I 10830** — EW vs log R'HK from Jian et al. 2024 (`he_paper/`)
- **Research**: three rows (physics → tools → astrophysics) with figures computed for the page:
  - broadening sequence of one Ca I 6162 line (PySME; `broad/run.py`)
  - a column of PySME syntheses of 11 FGK stars, 4569–4581 Å, R = 20000 (`stack/run.py`)
  - edge-on Milky Way star field sampled from simple density laws, with sightlines from the Sun (`src/gen_galaxy.py`)
- **Software (PySME)**: the code snippet drives a step-by-step diagram (click a line to jump to it). The model atmosphere is drawn with the author's radiative-transfer cell figure (`rt_cell.png`); the synthesis step shows real PySME spectra computed with only the deepest 14, 18, 23, 31 and all 55 layers (`codeanim/cells.py`); the final spectrum is the snippet run as written (`codeanim/run.py`).
- **Survey (4MOST)**: ~110 spectra drawn on a canvas from the 11 PySME syntheses with random RV shifts and noise, feeding the 4MOST box (`4most_logo.png`) and the measured quantities (`src/gen_survey.py`).
- **Publications / About**: five selected papers linked to SciX; full CV is `Mingjie_Jian_CV.pdf` (a copy — re-copy when the CV changes).
- **Portrait**: objective-prism plate drawn from `portrait_round.jpg`; appears 3 s after load and 3 s after a panel closes; hover reveals the photo.

## Rebuild

```bash
cd redesign/prototype/src
python3 gen_wide.py        # hero spectrum + bands (needs numpy)
python3 gen_phos.py        # etc. for the other figures
python3 build.py           # assemble ../index.html from template.html + svg_*.svg
```

## Still to do

- Hero spectrum now uses the Kitt Peak solar flux atlas (Kurucz et al. 1984) smoothed to R ≈ 6000 (`solar/prep_solar.py`; the 25 MB `solarflux.asc` is not committed — download from kurucz.harvard.edu/sun/fluxatlas/). Telluric H₂O bands are real but unlabelled.
- `pysme_fit/run_fit.py` and `stack/run.py` read line lists from absolute local paths.
- Ca I 6162 atomic data in `broad/ca6162.lin` were entered by hand — check against VALD.
- Phosphorus plot: 8 Cepheids are digitised from the paper figure without error bars; one of the 20 Cepheids is hidden by overlap — replace with the CDS table.
- Sections below the hero (research, software, publications, about) still carry earlier placeholder copy and facts to confirm (dates, "25+ papers", PySME snippet, selected papers).
- Port to the production structure (Jekyll layout or static build), clean unused code (isophote renderer), retire the old theme and its service worker.

## Live site

The root `index.html` is the published homepage: run `python3 redesign/deploy.py` after rebuilding the prototype (it rewrites asset paths to `/assets/home/` and copies the assets). The page has no front matter, so Jekyll copies it unchanged. The blog (`/blog/`, posts, tags, feed) still uses the old Hux-blog layouts. `sw.js` now only clears the old caches and unregisters itself; `service-worker: false` in `_config.yml` stops new registrations. `redesign/` is excluded from the Jekyll build.
