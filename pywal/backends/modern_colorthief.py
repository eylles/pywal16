"""
Generate a colorscheme using modern_colorthief.
"""

import logging
import sys

try:
    import modern_colorthief

except ImportError:
    logging.error("modern_colorthief wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)

from .. import util
from .. import colors


def gen_colors(img):
    """Ask backend to generate 16 colors."""
    raw_colors = modern_colorthief.get_palette(img, 16)

    return [util.rgb_to_hex(color) for color in raw_colors]


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
