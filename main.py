#!/usr/bin/env python3
"""news-image-20261122 entry (Python 3.13, standard library only).

The image is the entry.png beside this file, drawn beforehand by draw.py;
the program copies it to /output/entry.png. The grader runs with standard
library only, so this file imports nothing beyond it.

Outside the grader's container, OUT stands in for /output/entry.png:
    OUT=output/entry.png python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get(
    "OUT", os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
)

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
# A plain copy, so two runs write byte-for-byte the same file.
shutil.copyfile(SRC, OUT)
