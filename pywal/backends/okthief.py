"""
Generate a colorscheme using okthief.
"""

import logging
import shutil
import subprocess
import sys
import json

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using okthief."""
    cmd = ["okthief", "--num-colors", "8", "--file"]
    out = subprocess.check_output([*cmd, img])
    cols = [x["hex"] for x in json.loads(out)]
    white, black, rest = (cols[0], cols[1], cols[2:])
    cols = [black]
    cols.extend(rest)
    cols.append(white)
    cols.extend(cols.copy())
    return cols


def adjust(cols, light, **kwargs):
    """Create palette.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    return colors.generic_adjust(cols, light, c16=cols16)


def get(img, light=False, **kwargs):
    """Get colorscheme.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    if not shutil.which("okthief"):
        logging.error("okthief wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = gen_colors(img)
    cols[0] = util.darken_color(cols[0], 0.80)
    return adjust(cols, light, c16=cols16)
