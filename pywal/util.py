"""
Misc helper functions.
"""

import colorsys
import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import hashlib
import copy

has_fcntl = False
fcntl_warning = ""

try:
    import fcntl

    has_fcntl = True
except ImportError:
    fcntl_warning = "{}, {}".format(
        "can't skip blocking io in current platform",
        "program could hang indefinitely",
    )


class Color:
    """Color formats."""

    alpha_num = "100"
    passed_alpha_num = None

    def __init__(self, hex_color):
        self.hex_color = hex_color

    def __str__(self):
        return self.hex_color

    @property
    def rgb(self):
        """Convert a hex color to rgb."""
        return "%s,%s,%s" % (*hex_to_rgb(self.hex_color),)

    @property
    def rgbspace(self):
        """Convert a hex color to rgb separated by spaces."""
        return "%s %s %s" % (*hex_to_rgb(self.hex_color),)

    @property
    def xrgba(self):
        """Convert a hex color to xrdb rgba."""
        return hex_to_xrgba(self.hex_color)

    @property
    def rgba(self):
        """Convert a hex color to rgba."""
        return "rgba(%s,%s,%s,%s)" % (
            *hex_to_rgb(self.hex_color),
            self.alpha_dec,
        )

    @property
    def hex_argb(self):
        """Convert an alpha hex color to argb hex."""
        al_val = alpha_integrify(self.alpha_num)
        return "#%02X%s" % (
            int(int(al_val) * 255 / 100),
            self.hex_color[1:],
        )

    @property
    def alpha(self):
        """Add URxvt alpha value to color."""
        al_val = alpha_integrify(self.alpha_num)
        return "[%s]%s" % (al_val, self.hex_color)

    @property
    def alpha_dec(self):
        """Export the alpha value as a decimal number in [0, 1]."""
        al_val = alpha_integrify(self.alpha_num)
        return int(al_val) / 100

    @property
    def alpha_hex(self):
        """Export the alpha value as a hexdecimal number in [00, FF]."""
        al_val = alpha_integrify(self.alpha_num)
        return "%02X" % (int(int(al_val) * 255 / 100))

    @property
    def decimal(self):
        """Export color in decimal."""
        return "%s%s" % ("#", int(self.hex_color[1:], 16))

    @property
    def decimal_strip(self):
        """Strip '#' from decimal color."""
        return int(self.hex_color[1:], 16)

    @property
    def octal(self):
        """Export color in octal."""
        return "%s%s" % ("#", oct(int(self.hex_color[1:], 16))[2:])

    @property
    def octal_strip(self):
        """Strip '#' from octal color."""
        return oct(int(self.hex_color[1:], 16))[2:]

    @property
    def strip(self):
        """Strip '#' from color."""
        return self.hex_color[1:]

    @property
    def red(self):
        """Red value as float between 0 and 1."""
        return "%.3f" % (hex_to_rgb(self.hex_color)[0] / 255.0)

    @property
    def green(self):
        """Green value as float between 0 and 1."""
        return "%.3f" % (hex_to_rgb(self.hex_color)[1] / 255.0)

    @property
    def blue(self):
        """Blue value as float between 0 and 1."""
        return "%.3f" % (hex_to_rgb(self.hex_color)[2] / 255.0)

    @property
    def red_hex(self):
        """Red value as hex."""
        return "%s" % (self.hex_color)[1:3]

    @property
    def green_hex(self):
        """Green value as hex."""
        return "%s" % (self.hex_color)[3:5]

    @property
    def blue_hex(self):
        """Blue value as hex."""
        return "%s" % (self.hex_color)[5:]

    @property
    def red_dec(self):
        """Red value as decimal."""
        return "%s" % hex_to_rgb(self.hex_color)[0]

    @property
    def green_dec(self):
        """Green value as decimal."""
        return "%s" % hex_to_rgb(self.hex_color)[1]

    @property
    def blue_dec(self):
        """Blue value as decimal."""
        return "%s" % hex_to_rgb(self.hex_color)[2]

    @property
    def w3_luminance(self):
        """Luminance value of the color according to W3 formula"""

        color_channels = [float(self.red), float(self.green), float(self.blue)]
        for index, channel in enumerate(color_channels):
            if channel <= 0.04045:
                color_channels[index] = channel / 12.92
            else:
                color_channels[index] = ((channel + 0.055) / 1.055) ** 2.4

        return (
            (0.2126 * color_channels[0])
            + (0.7152 * color_channels[1])
            + (0.0722 * color_channels[2])
        )

    def lighten(self, percent):
        """Lighten color by percent."""
        percent = float(re.sub(r"[\D\.]", "", str(percent)))
        return Color(lighten_color(self.hex_color, percent / 100))

    def darken(self, percent):
        """Darken color by percent."""
        percent = float(re.sub(r"[\D\.]", "", str(percent)))
        return Color(darken_color(self.hex_color, percent / 100))

    def saturate(self, percent):
        """Saturate a color."""
        percent = float(re.sub(r"[\D\.]", "", str(percent)))
        return Color(saturate_color(self.hex_color, percent / 100))

    def adjust_alpha(self, alpha="100"):
        adjusted = copy.copy(self)
        adjusted.alpha_num = alpha
        return adjusted


def read_file(input_file):
    """Read data from a file and trim newlines."""
    with open(input_file, "r") as file:
        return file.read().splitlines()


def read_file_json(input_file):
    """Read data from a json file."""
    with open(input_file, "r") as json_file:
        return json.load(json_file)


def read_file_raw(input_file):
    """Read data from a file as is, don't strip
    newlines or other special characters."""
    with open(input_file, "r") as file:
        return file.readlines()


def save_file(data, export_file):
    """Write data to a file."""
    create_dir(os.path.dirname(export_file))

    if has_fcntl:
        try:
            with open(export_file, "w") as file:
                # Get the current flags and add non-blocking mode
                # to skip TTYs suspended by Flow Control
                # https://www.gnu.org/software/libc/manual/html_node/Getting-File-Status-Flags.html
                # https://www.gnu.org/software/libc/manual/html_node/Open_002dtime-Flags.html
                flags = fcntl.fcntl(file, fcntl.F_GETFL)
                fcntl.fcntl(file, fcntl.F_SETFL, flags | os.O_NONBLOCK)
                file.write(data)
        except PermissionError:
            logging.warning("Couldn't write to %s.", export_file)
        except BlockingIOError:
            logging.warning(
                "Couldn't write to %s, not accepting data", export_file
            )
    else:
        try:
            with open(export_file, "w") as file:
                file.write(data)
        except PermissionError:
            logging.warning("Couldn't write to %s.", export_file)


def save_file_json(data, export_file):
    """Write data to a json file."""
    create_dir(os.path.dirname(export_file))

    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)


def get_img_checksum(img):
    checksum = hashlib.new("md5", usedforsecurity=False)
    with open(img, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def create_dir(directory):
    """Alias to create the cache dir."""
    os.makedirs(directory, exist_ok=True)


def setup_logging():
    """Logging config."""
    logging.basicConfig(
        format=(
            "[%(levelname)s\033[0m] "
            "\033[1;31m%(module)s\033[0m: "
            "%(message)s"
        ),
        level=logging.INFO,
        stream=sys.stdout,
    )
    logging.addLevelName(logging.ERROR, "\033[1;31mE")
    logging.addLevelName(logging.INFO, "\033[1;32mI")
    logging.addLevelName(logging.WARNING, "\033[1;33mW")


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    return tuple(bytes.fromhex(color.strip("#")))


def hex_to_xrgba(color):
    """Convert a hex color to xrdb rgba."""
    col = color.lower().strip("#")
    return "%s%s/%s%s/%s%s/ff" % (*col,)


def rgb_to_hex(color):
    """Convert an rgb color to hex."""
    return "#%02x%02x%02x" % (*color,)


def darken_color(color, amount):
    """Darken a hex color."""
    color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def lighten_color(color, amount):
    """Lighten a hex color."""
    color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def alpha_integrify(alpha_value):
    """
    ensure the alpha string is an int between 0 and 100

    return: int string between 0 an 100
    """
    # could be a string containing a float like 0.7
    a = float(alpha_value)
    if a < 0:
        a = abs(a)
    if a < 1:
        a = a * 100
    if a > 100:
        a = 100
    a = int(a)
    a = str(a)
    return a


def blend_color(color, color2):
    """Blend two colors together."""
    r1, g1, b1 = hex_to_rgb(color)
    r2, g2, b2 = hex_to_rgb(color2)

    r3 = int(0.5 * r1 + 0.5 * r2)
    g3 = int(0.5 * g1 + 0.5 * g2)
    b3 = int(0.5 * b1 + 0.5 * b2)

    return rgb_to_hex((r3, g3, b3))


def saturate_color(color, amount):
    """Change saturation of a hex color to passed value.

    new_saturation = amount"""
    r, g, b = hex_to_rgb(color)
    r, g, b = [x / 255.0 for x in (r, g, b)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = amount
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [x * 255.0 for x in (r, g, b)]

    return rgb_to_hex((int(r), int(g), int(b)))


def add_saturation(color, amount):
    """Add saturation to a hex color.

    new_saturation = color_saturation + amount"""
    r, g, b = hex_to_rgb(color)
    r, g, b = [x / 255.0 for x in (r, g, b)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = s + amount
    if s > 1.0:
        s = 1
    if s < -1.0:
        s = -1
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [x * 255.0 for x in (r, g, b)]

    return rgb_to_hex((int(r), int(g), int(b)))


def rgb_to_yiq(color):
    """Sort a list of colors."""
    return colorsys.rgb_to_yiq(*hex_to_rgb(color))


def disown(cmd):
    """Call a system command in the background,
    disown it and hide it's output."""
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_pid(name):
    """Check if process is running by name."""
    if not shutil.which("pidof"):
        return False

    try:
        if platform.system() != "Darwin":
            subprocess.check_output(["pidof", "-s", name])
        else:
            subprocess.check_output(["pidof", name])

    except subprocess.CalledProcessError:
        return False

    return True


def has_im():
    """Check to see if the user has im installed."""
    if shutil.which("magick"):
        return "magick"

    if shutil.which("convert"):
        return "convert"

    logging.error("Problem running image averaging command.")
    logging.error("Imagemagick wasn't found on your system.")
    sys.exit(1)


def image_average_color(img):
    """Get the average color of an image using imagemagick
    by resizing to 1x1"""
    # Attempt to run the imagemagick command
    # Resizes to 1x1 and enumerates all pixel data (one pixel) to stdout
    # Command adapted from a stackoverflow thread, but tinkered with because the
    # thread was a decade old:
    # # https://stackoverflow.com/questions/25488338/how-to-find-average-color-of-an-image-with-imagemagick
    cmd_flags = [
        "-resize",
        "1x1!",
        "-format",
        '"%[fx:int(255*r+.5)],%[fx:int(255*g+.5)],%[fx:int(255*b+.5)]"',
        "txt:-",
    ]
    magick_command = has_im()
    try:
        magick_output = subprocess.run(
            [magick_command, img] + cmd_flags, stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as Err:
        logging.error(
            "Problem running image averaging command. Is imagemagick installed?"
        )
        logging.error("Imagemagick error: %s", Err)
        return ""

    # Regex hex code from the command output
    return re.search("#[0-9A-Fa-f]{6}", magick_output.stdout.decode("utf-8"))[0]
