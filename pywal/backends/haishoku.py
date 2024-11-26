"""
Generate a colorscheme using Haishoku.
"""

import logging
import sys

try:
    from haishoku.haishoku import Haishoku

except ImportError:
    logging.error("Haishoku wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    palette = Haishoku.getPalette(img)
    return [util.rgb_to_hex(col[1]) for col in palette]


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
    raw_colors = [*cols, *cols]
    raw_colors[0] = util.lighten_color(cols[0], 0.40)
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
    cols = gen_colors(img)
    return adjust(cols, light, c16=cols16)
