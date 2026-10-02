"""Publish the prototype as the site's root index.html (no front matter: Jekyll copies it as is,
without Liquid). Assets live in /assets/home/. Run after rebuilding the prototype."""
import os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "redesign", "prototype")
ASSETS = ["portrait_round.jpg", "rt_cell.png", "4most_logo.png", "Mingjie_Jian_CV.pdf"]
html = open(os.path.join(P, "index.html")).read()
for a in ASSETS:
    for q in ('"', "'"):
        html = html.replace(f"{q}{a}{q}", f"{q}/assets/home/{a}{q}")
    shutil.copy(os.path.join(P, a), os.path.join(ROOT, "assets", "home", a))
assert not html.startswith("---")
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("index.html", len(html) // 1024, "KB")
