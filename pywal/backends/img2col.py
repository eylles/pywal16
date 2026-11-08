"""
Generate a colorscheme using img2colscheme
"""

import logging
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using img2colscheme."""
    cmd = ["img2colscheme"]
    lines = subprocess.check_output([*cmd, img]).splitlines()
    # Grab index 1 (the 2nd column), ignoring any empty lines
    return [line.split()[1] for line in lines if line.strip()]


def adjust(cols, light, **kwargs):
    """Create palette.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    vibrant = [
        util.saturate_color(util.foxify_color(col, 0.15), 0.34)
        for col in cols[8:]
    ]
    raw_colors = [*vibrant, *vibrant]
    raw_colors[0] = util.darken_color(raw_colors[0], 0.51)

    return colors.generic_adjust(raw_colors, light, c16=cols16)


def get(img, light=False, **kwargs):
    """Get colorscheme.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    if not shutil.which("img2colscheme"):
        logging.error("img2colscheme wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = [col.decode("UTF-8") for col in gen_colors(img)]
    return adjust(cols, light, c16=cols16)
