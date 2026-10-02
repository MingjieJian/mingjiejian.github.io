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
- **Portrait**: objective-prism plate drawn from `portrait_round.jpg`; appears 3 s after load and 3 s after a panel closes; hover reveals the photo.

## Rebuild

```bash
cd redesign/prototype/src
python3 gen_wide.py        # hero spectrum + bands (needs numpy)
python3 gen_phos.py        # etc. for the other figures
python3 build.py           # assemble ../index.html from template.html + svg_*.svg
```

## Still to do

- Replace the **synthetic hero spectrum** with real data (weak-line forest and O₂ A/B bands are placeholders; candidate: NSO/Kitt Peak solar flux atlas).
- Phosphorus plot: 8 Cepheids are digitised from the paper figure without error bars; one of the 20 Cepheids is hidden by overlap — replace with the CDS table.
- Sections below the hero (research, software, publications, about) still carry earlier placeholder copy and facts to confirm (dates, "25+ papers", PySME snippet, selected papers).
- Port to the production structure (Jekyll layout or static build), clean unused code (isophote renderer), retire the old theme and its service worker.
