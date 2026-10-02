import re, zlib
raw = open("figure/stock-2-Ca-He.pdf", "rb").read()
streams = []
for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
    try: streams.append(zlib.decompress(m.group(1)))
    except Exception: pass
print("streams:", len(streams))
main = max(streams, key=len).decode("latin1")
# markers: "1 0 0 1 x y cm /Mk Do"
marks = re.findall(r"([-\d.]+) ([-\d.]+) cm\s*/(M\d+) Do", main)
from collections import Counter
print("markers per symbol:", Counter(m[2] for m in marks))
open("content.txt", "w").write(main)
# tick text: matplotlib draws tick labels as glyphs; find tick marks positions instead (short lines in axes)
