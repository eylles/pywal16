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
            [*magick_command.split(), img, *flags], stderr=subprocess.STDOUT
        ).splitlines()
    except subprocess.CalledProcessError as Err:
        logging.error("Imagemagick error: %s", Err)
        logging.error(
            "IM 7 disables stdout by default, check the manual or wiki to fix."
        )
        sys.exit(1)
    return output


def has_im():
    """Check to see if the user has im installed."""
    magick_commands = []

    if shutil.which("magick"):
        magick_commands.extend(["magick", "magick convert"])

    if shutil.which("convert"):
        magick_commands.append("convert")

    if len(magick_commands) > 0:
        return magick_commands

    logging.error("Imagemagick wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)


def gen_colors_with_command(img, magick_command, beginning_color_count=16, iteration_count = 20):
    max_color_count = beginning_color_count + iteration_count - 1
    for color_count in range(beginning_color_count, beginning_color_count + iteration_count):
        raw_colors = imagemagick(color_count, img, magick_command)

        if len(raw_colors) > 16:
            break

        if color_count == max_color_count:
            logging.error("Imagemagick couldn't generate a suitable palette.")
            logging.warning("will try to do palette concatenation, good results not guaranteed!")
            while not len(raw_colors) > 16:
                raw_colors = raw_colors + raw_colors
        else:
            logging.warning("Imagemagick couldn't generate a palette.")
            logging.warning("Trying a larger palette size %s", color_count)
    return raw_colors


def gen_colors(img):
    """Format the output from imagemagick into a list of hex colors."""
    magick_commands = has_im()

    for magick_command in magick_commands:
        logging.debug(f"Trying {magick_command}...")

        try:
            raw_colors = gen_colors_with_command(img, magick_command)
            hex_colors = [
                re.search("#.{6}", str(col)).group(0)
                for col in raw_colors[1:]
            ]

            if not hex_colors:
                logging.warning("Failed to generate colors.")
                continue

            while len(hex_colors) < 16:
                logging.warning("will try to do palette concatenation, good results not guaranteed!")
                hex_colors += hex_colors
            break
        except AttributeError:
            logging.warning(f"{magick_command} failed.")
            continue

    return hex_colors


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
