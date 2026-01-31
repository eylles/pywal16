"""
Generate a colorscheme using imagemagick.
"""

import logging
import re
import shutil
import subprocess
import sys

from .. import colors


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


def gen_colors_with_command(
        img, magick_command, beginning_color_count=16, iteration_count=20
        ):
    """Iteratively attempt to generate a 16-color palette
    using a specific Imagemagick command."""
    hex_pattern = re.compile(r"#[A-F0-9]{6}", re.IGNORECASE)

    max_color_count = beginning_color_count + iteration_count - 1
    for color_count in range(
            beginning_color_count, beginning_color_count + iteration_count
            ):
        raw_output = imagemagick(color_count, img, magick_command)
        hex_colors = [
            hex_pattern.search(str(col)).group()
            for col in raw_output
            if hex_pattern.search(str(col))
        ]

        if len(hex_colors) >= 16:
            break

        if color_count < max_color_count:
            logging.warning(
                    "Imagemagick couldn't generate a "
                    f"palette with {magick_command}."
                    )
            logging.warning(
                    f"Trying a larger palette size {color_count}."
                    )
        else:
            logging.error(
                    "Imagemagick couldn't generate a suitable palette "
                    f"with {magick_command}."
                    )
            logging.warning(
                    "Will try to do palette concatenation, "
                    "good results not guaranteed!"
                    )
            while len(hex_colors) < 16:
                hex_colors.extend(hex_colors)
    return hex_colors


def gen_colors(img):
    """Try each Imagemagick command until a color palette
    is successfully generated."""
    magick_commands = has_im()

    for magick_command in magick_commands:
        logging.debug(f"Trying {magick_command}...")

        hex_colors = gen_colors_with_command(img, magick_command)

        if not hex_colors:
            logging.warning(
                    f"Failed to generate colors with {magick_command}."
                    )
            continue

        return hex_colors

    raise RuntimeError(
            "Failed to generate color palette from "
            f"{img} with these commands: {magick_commands}"
            )


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
