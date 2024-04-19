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
    """Generate a colorscheme using Colorz."""
    cmd = ["okthief", "--num-colors", "8", "--file"]
    out = subprocess.check_output([*cmd, img])
    cols = [x["hex"] for x in json.loads(out)]
    white, black, rest = (cols[0], cols[1], cols[2:])
    cols = [black]
    cols.extend(rest)
    cols.append(white)
    cols.extend(cols.copy())
    return cols

def adjust(cols, light):
    """Create palette."""
    return cols

def get(img, light=False):
    """Get colorscheme."""
    if not shutil.which("okthief"):
        logging.error("okthief wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = gen_colors(img)
    return adjust(cols, light)
