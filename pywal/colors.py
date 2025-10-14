"""
Generate a palette using various backends.
"""

import colorsys
import logging
import os
import random
import re
import sys

from . import theme
from . import util
from .settings import CACHE_DIR, MODULE_DIR, __cache_version__


def list_backends():
    """List color backends."""
    return [
        b.name.replace(".py", "")
        for b in os.scandir(os.path.join(MODULE_DIR, "backends"))
        if "__" not in b.name
    ]


def normalize_img_path(img: str):
    """Normalizes the image path for output."""
    if os.name == "nt":
        # On Windows, the JSON.dump ends up outputting un-escaped backslash
        # breaking the ability to read colors.json. Windows supports forward
        # slash, so we can use that for now
        return img.replace("\\", "/")
    return img


def colors_to_dict(colors, img):
    """Convert list of colors to pywal format."""
    return {
        "checksum": util.get_img_checksum(img),
        "wallpaper": normalize_img_path(img),
        "alpha": util.Color.alpha_num,
        "special": {
            "background": colors[0],
            "foreground": colors[15],
            "cursor": colors[15],
        },
        "colors": {
            "color0": colors[0],
            "color1": colors[1],
            "color2": colors[2],
            "color3": colors[3],
            "color4": colors[4],
            "color5": colors[5],
            "color6": colors[6],
            "color7": colors[7],
            "color8": colors[8],
            "color9": colors[9],
            "color10": colors[10],
            "color11": colors[11],
            "color12": colors[12],
            "color13": colors[13],
            "color14": colors[14],
            "color15": colors[15],
        },
    }


def get_color_names_list(colors_dict):
    ret_list = []
    # detect dict type
    if "color0" in colors_dict:
        ret_list = [
                "color0", "color1", "color2", "color3",
                "color4", "color5", "color6", "color7",
                "color8", "color9", "color10", "color11",
                "color12", "color13", "color14", "color15",
              ]
    else:
        ret_list = [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
              ]
    return ret_list


def shade_darken(colors, light):
    k_v = []
    k_v = get_color_names_list(colors)
    if light:
        colors[k_v[1]] = util.darken_color(colors[k_v[1]], 0.25)
        colors[k_v[2]] = util.darken_color(colors[k_v[2]], 0.25)
        colors[k_v[3]] = util.darken_color(colors[k_v[3]], 0.25)
        colors[k_v[4]] = util.darken_color(colors[k_v[4]], 0.25)
        colors[k_v[5]] = util.darken_color(colors[k_v[5]], 0.25)
        colors[k_v[6]] = util.darken_color(colors[k_v[6]], 0.25)
    else:
        colors[k_v[1]] = util.darken_color(colors[k_v[1]], 0.25)
        colors[k_v[2]] = util.darken_color(colors[k_v[2]], 0.25)
        colors[k_v[3]] = util.darken_color(colors[k_v[3]], 0.25)
        colors[k_v[4]] = util.darken_color(colors[k_v[4]], 0.25)
        colors[k_v[5]] = util.darken_color(colors[k_v[5]], 0.25)
        colors[k_v[6]] = util.darken_color(colors[k_v[6]], 0.25)


def shade_lighten(colors, light):
    k_v = []
    k_v = get_color_names_list(colors)
    if light:
        colors[k_v[9]] = util.lighten_color(colors[k_v[1]], 0.25)
        colors[k_v[10]] = util.lighten_color(colors[k_v[2]], 0.25)
        colors[k_v[11]] = util.lighten_color(colors[k_v[3]], 0.25)
        colors[k_v[12]] = util.lighten_color(colors[k_v[4]], 0.25)
        colors[k_v[13]] = util.lighten_color(colors[k_v[5]], 0.25)
        colors[k_v[14]] = util.lighten_color(colors[k_v[6]], 0.25)
    else:
        colors[k_v[9]] = util.lighten_color(colors[k_v[1]], 0.25)
        colors[k_v[10]] = util.lighten_color(colors[k_v[2]], 0.25)
        colors[k_v[11]] = util.lighten_color(colors[k_v[3]], 0.25)
        colors[k_v[12]] = util.lighten_color(colors[k_v[4]], 0.25)
        colors[k_v[13]] = util.lighten_color(colors[k_v[5]], 0.25)
        colors[k_v[14]] = util.lighten_color(colors[k_v[6]], 0.25)
        for i in range(9, 15):
            colors[k_v[i]] = util.saturate_color(colors[k_v[i]], 0.40)


def shade_16(colors, light, cols16):
    """Generic 16 color shading
    this function will apply the 16 color shading
    to any color dict it is passed

    colors: dict
    light:  boolean - werether the colorscheme is light
    cols16: str [lighten|darken] - method to generate the shades"""

    k_v = []
    k_v = get_color_names_list(colors)

    if cols16:
        if light:
            colors[k_v[7]] = util.darken_color(colors[k_v[0]], 0.50)
            colors[k_v[8]] = util.darken_color(colors[k_v[0]], 0.25)
            colors[k_v[15]] = util.darken_color(colors[k_v[0]], 0.75)
            if cols16 == "lighten" or cols16 == "dual":
                shade_lighten(colors, light)
            if cols16 == "darken" or cols16 == "dual":
                shade_darken(colors, light)
        else:
            colors[k_v[7]] = util.lighten_color(colors[k_v[0]], 0.55)
            colors[k_v[7]] = util.saturate_color(colors[k_v[7]], 0.05)
            colors[k_v[8]] = util.lighten_color(colors[k_v[0]], 0.35)
            colors[k_v[8]] = util.saturate_color(colors[k_v[8]], 0.10)
            colors[k_v[15]] = util.lighten_color(colors[k_v[0]], 0.75)
            if cols16 == "lighten" or cols16 == "dual":
                shade_lighten(colors, light)
            if cols16 == "darken" or cols16 == "dual":
                shade_darken(colors, light)


def generic_adjust(colors, light, **kwargs):
    """Generic color adjustment for themers.
    :keyword-args:
    -    c16 - [ "lighten" | "darken" ]
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False

    if light:
        for color in colors:
            color = util.saturate_color(color, 0.60)
            color = util.darken_color(color, 0.5)

        colors[0] = util.lighten_color(colors[0], 0.95)
        if cols16:
            shade_16(colors, light, cols16)
        else:
            colors[7] = util.darken_color(colors[0], 0.75)
            colors[8] = util.darken_color(colors[0], 0.25)
            colors[15] = colors[7]

    else:
        if colors[0][1] != "0":  # the color may already be dark enough
            colors[0] = util.darken_color(colors[0], 0.40)  # just a bit darker

        saturate_more = False
        if colors[0][1] == "0":  # the color may not be saturated enough
            saturate_more = True
        if colors[0][3] == "0":  # the color may not be saturated enough
            saturate_more = True
        if colors[0][5] == "0":  # the color may not be saturated enough
            saturate_more = True

        if saturate_more:
            colors[0] = util.lighten_color(colors[0], 0.03)
            colors[0] = util.saturate_color(colors[0], 0.40)

        if cols16:
            shade_16(colors, light, cols16)
        else:
            colors[7] = util.lighten_color(colors[0], 0.75)
            colors[8] = util.lighten_color(colors[0], 0.35)
            colors[8] = util.saturate_color(colors[8], 0.10)
            colors[15] = colors[7]

    return colors


def saturate_colors(colors, amount):
    """Saturate all colors."""
    if amount and (float(amount) <= 1.0 and float(amount) >= -1.0):
        for i, _ in enumerate(colors):
            if i not in [7, 15]:
                colors[i] = util.add_saturation(colors[i], float(amount))

    return colors


def ensure_contrast(colors, contrast, light, image):
    """Ensure user-specified W3 contrast of colors
    depending on dark or light theme."""
    # If no contrast checking was specified, do nothing
    if not contrast or contrast == "":
        return colors

    # Contrast must be within a predefined range
    if float(contrast) < 1 or float(contrast) > 21:
        logging.error("Specified contrast ratio is too extreme")
        return colors

    # Get the image background color
    background_color = util.Color(util.image_average_color(image))
    background_luminance = background_color.w3_luminance

    # Calculate the required W3 luminance for the desired contrast ratio
    # This will modify all of the colors to be brighter or darker than the
    # background image depending on whether the user has specified for a
    # dark or light theme
    try:
        if light:
            luminance_desired = (background_luminance + 0.05) / float(
                contrast
            ) - 0.05
        else:
            luminance_desired = (background_luminance + 0.05) * float(
                contrast
            ) - 0.05
    except ValueError:
        logging.error("ensure_contrast(): Contrast valued could not be parsed")
        return colors

    if luminance_desired >= 0.99:
        print("Can't contrast this palette without changing colors to white")
        return colors
    if luminance_desired <= 0.01:
        print("Can't contrast this palette without changing colors to black")
        return colors

    # Determine which colors should be modified / checked
    # ! For the time being this is just going to modify all the colors except
    # 0 and 15
    colors_to_contrast = range(1, 15)

    # Modify colors
    for index in colors_to_contrast:
        color = util.Color(colors[index])

        # If the color already has sufficient contrast, do nothing
        if light and color.w3_luminance <= luminance_desired:
            continue
        elif color.w3_luminance >= luminance_desired:
            continue

        h, s, v = colorsys.rgb_to_hsv(
            float(color.red), float(color.green), float(color.blue)
        )

        # Determine how to modify the color based on its HSV characteristics

        # If the color is to be lighter than background, and the HSV color
        # with value 1 has sufficient luminance, adjust by increasing value
        if (
            not light
            and util.Color(
                util.rgb_to_hex(
                    [
                        int(channel * 255)
                        for channel in colorsys.hsv_to_rgb(h, s, 1)
                    ]
                )
            ).w3_luminance
            >= luminance_desired
        ):
            colors[index] = binary_luminance_adjust(
                luminance_desired, h, s, s, v, 1
            )
        # If the color is to be lighter than background and increasing value
        # to 1 doesn't produce the desired luminance, additionally decrease
        # saturation
        elif not light:
            colors[index] = binary_luminance_adjust(
                luminance_desired, h, 0, s, 1, 1
            )
        # If the color is to be darker than background, produce desired
        # luminance by decreasing value, and raising saturation
        else:
            colors[index] = binary_luminance_adjust(
                luminance_desired, h, s, 1, 0, v
            )

    return colors


def binary_luminance_adjust(
    luminance_desired, hue, s_min, s_max, v_min, v_max, iterations=10
):
    """Use a binary method to adjust a color's value and/or
    saturation to produce the desired luminance"""
    for i in range(iterations):
        # Obtain a new color by averaging saturation and value
        s = (s_min + s_max) / 2
        v = (v_min + v_max) / 2

        # Compare the luminance of this color to the target luminance
        # If the color is too light, clamp the minimum saturation
        # and maximum value
        if (
            util.Color(
                util.rgb_to_hex(
                    [
                        int(channel * 255)
                        for channel in colorsys.hsv_to_rgb(hue, s, v)
                    ]
                )
            ).w3_luminance
            >= luminance_desired
        ):
            s_min = s
            v_max = v
        # If the color is too dark, clamp the maximum saturation
        # and minimum value
        else:
            s_max = s
            v_min = v

    return util.rgb_to_hex(
        [int(channel * 255) for channel in colorsys.hsv_to_rgb(hue, s, v)]
    )


def cache_fname(img, backend, light, cache_dir, sat="", **kwargs):
    """Create the cache file name.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    -    cst: palette contrast ratio - float
    """
    color_type = "light" if light else "dark"
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    if "cst" in kwargs:
        contrast = kwargs["cst"]
    else:
        contrast = False
    color_num = "16" if cols16 else "9"
    file_name = re.sub("[/|\\|.]", "_", img)
    file_size = os.path.getsize(img)

    if cols16 and contrast:
        file_parts = [
            file_name,
            color_num,
            cols16,
            color_type,
            backend,
            sat,
            contrast,
            file_size,
            __cache_version__,
        ]
        return [
            cache_dir,
            "schemes",
            "%s_%s_%s_%s_%s_%s_%s_%s_%s.json" % (*file_parts,),
        ]
    if cols16 and (not contrast):
        file_parts = [
            file_name,
            color_num,
            cols16,
            color_type,
            backend,
            sat,
            file_size,
            __cache_version__,
        ]
        return [
            cache_dir,
            "schemes",
            "%s_%s_%s_%s_%s_%s_%s_%s.json" % (*file_parts,),
        ]
    if (not cols16) and contrast:
        file_parts = [
            file_name,
            color_type,
            backend,
            sat,
            contrast,
            file_size,
            __cache_version__,
        ]
        return [
            cache_dir,
            "schemes",
            "%s_%s_%s_%s_%s_%s_%s.json" % (*file_parts,),
        ]
    else:
        file_parts = [
            file_name,
            color_type,
            backend,
            sat,
            file_size,
            __cache_version__,
        ]
        return [
            cache_dir,
            "schemes",
            "%s_%s_%s_%s_%s_%s.json" % (*file_parts,),
        ]


def get_backend(backend):
    """Figure out which backend to use."""
    if backend == "random":
        backends = list_backends()
        random.shuffle(backends)
        return backends[0]

    return backend


def palette():
    """Generate a palette from the colors."""
    for i in range(0, 16):
        if i % 8 == 0:
            print()

        if i > 7:
            i = "8;5;%s" % i

        print("\033[4%sm%s\033[0m" % (i, " " * (80 // 20)), end="")

    print("\n")


def get(
    img,
    light=False,
    backend="wal",
    cache_dir=CACHE_DIR,
    sat="",
    **kwargs,
):
    """Generate a palette.
    :keyword-args:
    -    c16: use 16 colors through specified method - [ "lighten" | "darken" ]
    -    cst: apply contrast ratio to palette        - float
    """
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False
    if "cst" in kwargs:
        contrast = kwargs["cst"]
    else:
        contrast = ""

    # home_dylan_img_jpg_backend_1.2.2.json
    if not contrast or contrast == "":
        cache_name = cache_fname(
            img, backend, light, cache_dir, sat,
            c16=cols16
        )
    else:
        cache_name = cache_fname(
            img, backend, light, cache_dir, sat,
            c16=cols16, cst=float(contrast)
        )

    cache_file = os.path.join(*cache_name)

    # Check the wallpaper's checksum against the cache'
    if os.path.isfile(cache_file) and theme.parse(cache_file)[
        "checksum"
    ] == util.get_img_checksum(img):
        colors = theme.file(cache_file)
        logging.info("Found cached colorscheme.")

    else:
        logging.info("Generating a colorscheme.")
        backend = get_backend(backend)

        # Dynamically import the backend we want to use.
        # This keeps the dependencies "optional".
        try:
            __import__("pywal.backends.%s" % backend)
        except ImportError:
            __import__("pywal.backends.wal")
            backend = "wal"

        logging.info("Using %s backend.", backend)
        backend = sys.modules["pywal.backends.%s" % backend]
        colors = getattr(backend, "get")(img, light, c16=cols16)

        # Post-processing steps from command-line arguments
        colors = saturate_colors(colors, sat)
        colors = ensure_contrast(colors, contrast, light, img)

        colors = colors_to_dict(colors, img)

        util.save_file_json(colors, cache_file)
        logging.info("Generation complete.")

    return colors


def file(input_file):
    """Deprecated: symbolic link to --> theme.file"""
    return theme.file(input_file)
