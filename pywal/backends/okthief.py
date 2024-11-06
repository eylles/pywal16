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


def adjust(cols, light, cols16):
    """Create palette."""
    return colors.generic_adjust(cols, light, cols16)


def get(img, light=False, cols16=False):
    """Get colorscheme."""
    if not shutil.which("okthief"):
        logging.error("okthief wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = gen_colors(img)
    cols[0] = util.darken_color(cols[0], 0.80)
    return adjust(cols, light, cols16)
