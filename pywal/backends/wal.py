"""
Generate a colorscheme using imagemagick.
"""

import logging
import re
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def imagemagick(color_count, img, magick_command):
    """Call Imagemagick to generate a scheme."""
    flags = [
        "-resize",
        "25%",
        "-colors",
        str(color_count),
        "-unique-colors",
        "txt:-",
    ]
    img += "[0]"

    try:
        output = subprocess.check_output(
            [*magick_command, img, *flags], stderr=subprocess.STDOUT
        ).splitlines()
    except subprocess.CalledProcessError as Err:
        logging.error("Imagemagick error: %s", Err)
        logging.error(
            "IM 7 disables stdout by default, check the wiki for the fix."
        )
        sys.exit(1)
    return output


def has_im():
    """Check to see if the user has im installed."""
    if shutil.which("magick"):
        return ["magick", "convert"]

    if shutil.which("convert"):
        return ["convert"]

    logging.error("Imagemagick wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)


def try_gen_in_range(img, magick_command):
    for i in range(0, 20, 1):
        raw_colors = imagemagick(16 + i, img, magick_command)

        if len(raw_colors) > 16:
            break

        if i == 19:
            logging.error("Imagemagick couldn't generate a suitable palette.")
            sys.exit(1)

        else:
            logging.warning("Imagemagick couldn't generate a palette.")
            logging.warning("Trying a larger palette size %s", 16 + i)
    return raw_colors


def gen_colors(img):
    """Format the output from imagemagick into a list
    of hex colors."""
    magick_command = has_im()

    raw_colors = try_gen_in_range(img, magick_command)

    try:
        out = [re.search("#.{6}", str(col)).group(0) for col in raw_colors[1:]]
    except AttributeError:
        if magick_command == ["magick", "convert"]:
            logging.warning("magick convert failed, using only magick")
            magick_command = ["magick"]
            raw_colors = try_gen_in_range(img, magick_command)
            out = [
                re.search("#.{6}", str(col)).group(0) for col in raw_colors[1:]
            ]

    return out


def adjust(cols, light, **kwargs):
    """Adjust the generated colors and store them in a dict that
    we will later save in json format.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    raw_colors = cols[:1] + cols[8:16] + cols[8:-1]

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
    colors = gen_colors(img)
    # it is possible we could have picked garbage data
    garbage = "# Image"
    if garbage in colors:
        colors.remove(garbage)
    return adjust(colors, light, c16=cols16)
