"""
Generate a colorscheme using Schemer2.
"""

import logging
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    cmd = ["schemer2", "-format", "img::colors", "-minBright", "75", "-in"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(cols, light, **kwargs):
    """Create palette.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    cols.sort(key=util.rgb_to_yiq)
    raw_colors = [*cols[8:], *cols[8:]]
    raw_colors[0] = util.darken_color(cols[0], 0.80)

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
    if not shutil.which("schemer2"):
        logging.error("Schemer2 wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = [col.decode("UTF-8") for col in gen_colors(img)]
    return adjust(cols, light, c16=cols16)
