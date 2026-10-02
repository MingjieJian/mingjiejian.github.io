"""Assemble ../index.html from template.html and the generated fragments (svg_*.svg) in this folder.
Re-run the gen_*.py scripts first if a figure or data file changed."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(HERE, "template.html")).read()
html = re.sub(r"<!--SVG:(\w+)-->", lambda m: open(os.path.join(HERE, f"svg_{m.group(1)}.svg")).read(), html)
open(os.path.join(HERE, "..", "index.html"), "w").write(html)
print("index.html", len(html) // 1024, "KB")
