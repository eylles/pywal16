"""
Export colors in various formats.
"""

import logging
import os
import re
import shutil

from . import util
from .settings import CACHE_DIR, CONF_DIR, MODULE_DIR


class ExportFile:
    """A simple class for representing the few things
    needed to read a file and exporting it.
    """

    def __init__(self, abs_path, base_dir):
        self.name = os.path.basename(abs_path)
        self.path = abs_path
        self.relative_path = os.path.relpath(abs_path, base_dir)


def template(colors, input_file, output_file=None):
    """Read template file, substitute markers and
    save the file elsewhere."""
    # pylint: disable-msg=too-many-locals
    template_data = util.read_file_raw(input_file)
    for i, l in enumerate(template_data):
        for match in re.finditer(r"(?<=(?<!\{))(\{([^{}]+)\})(?=(?!\}))", l):
            # Get the color, and the functions associated with it
            cname, _, funcs = match.group(2).partition(".")
            # Check that functions are needed for this color
            if len(funcs) == 0:
                continue
            # Build up a string which will be replaced with the new color
            replace_str = cname
            # Color to be modified copied into new one
            new_color = util.Color(colors[cname].hex_color)
            # Execute each function to be done
            for func in filter(None, re.split(r"\)|\.", funcs)):
                # Get function name and arguments
                func = func.split("(")
                fname = func[0]
                if fname[0] == ".":
                    fname = fname[1:]
                if not hasattr(new_color, fname):
                    logging.error(
                        "Syntax error in template file '%s' on line '%s'",
                        input_file,
                        i,
                    )
                function = getattr(new_color, fname)

                # If the function is callable, call it
                if callable(function):
                    if len(func) > 1:
                        new_color = function(*func[1].split(","))
                    else:
                        new_color = function()
                    # string to replace generated colors
                    if func[0] != ".":
                        replace_str += "."
                    replace_str += "(".join(func) + ")"
                else:
                    # if it is an attribute i.e. rgb
                    replace_str += "." + fname
                    new_color = function

            if isinstance(new_color, util.Color):
                new_color = new_color.strip
            # If replace the format placeholder with the new color
            if new_color is not colors[cname]:
                new_color = str(new_color)
                template_data[i] = l.replace("{" + replace_str + "}", new_color)
    try:
        template_data = "".join(template_data).format(**colors)
    except (ValueError, KeyError, AttributeError) as exc:
        logging.error(
            "Syntax error in template file '%s': %r.", input_file, exc
        )
        return
    util.save_file(template_data, output_file)


def flatten_colors(colors):
    """Prepare colors to be exported.
    Flatten dicts and convert colors to util.Color()"""
    all_colors = {
        "wallpaper": colors["wallpaper"],
        "checksum": colors["checksum"],
        "alpha": colors["alpha"],
        **colors["special"],
        **colors["colors"],
    }
    return {k: util.Color(v) for k, v in all_colors.items()}


def get_export_type(export_type):
    """Convert template type to the right filename."""
    return {
        "css": "colors.css",
        "dmenu": "colors-wal-dmenu.h",
        "dwm": "colors-wal-dwm.h",
        "dwm_urg": "colors-wal-dwm-urg.h",
        "st": "colors-wal-st.h",
        "tabbed": "colors-wal-tabbed.h",
        "gtk2": "colors-gtk2.rc",
        "json": "colors.json",
        "konsole": "colors-konsole.colorscheme",
        "kitty": "colors-kitty.conf",
        "nqq": "colors-nqq.css",
        "plain": "colors",
        "putty": "colors-putty.reg",
        "rofi": "colors-rofi.Xresources",
        "scss": "colors.scss",
        "shell": "colors.sh",
        "fishshell": "colors.fish",
        "speedcrunch": "colors-speedcrunch.json",
        "sway": "colors-sway",
        "tty": "colors-tty.sh",
        "vscode": "colors-vscode.json",
        "waybar": "colors-waybar.css",
        "polybar": "colors-polybar",
        "xresources": "colors.Xresources",
        "haskell": "Colors.hs",
        "xmonad": "colors.hs",
        "yaml": "colors.yml",
    }.get(export_type, export_type)


def walk(directory):
    """Walks a directory tree and yields files for export"""
    for root, _, files in os.walk(directory):
        for file in files:
            yield (ExportFile(os.path.join(root, file), directory))


def generate_color_images(colors, destdir):
    """Save palette colors as an image"""
    if shutil.which("ultrakill-wal"):
        util.disown(["ultrakill-wal"])
    else:
        # Dynamically import.
        # This keeps the dependencies "optional".
        try:
            from PIL import Image
            img = Image.new('RGB', (16, 1))
            for i, color in enumerate(colors['colors'].values()):
                img.paste(Image.new('RGB', (1, 1), color), (i, 0))
            img.save(os.path.join(destdir, 'colors.png'))
        except ImportError:
            # we do not want to do anything here
            pass


def every(colors, output_dir=CACHE_DIR):
    """Export all template files."""
    join = os.path.join  # Minor optimization.
    generate_color_images(colors, output_dir)
    colors = flatten_colors(colors)
    template_dir = join(MODULE_DIR, "templates")
    template_dir_user = join(CONF_DIR, "templates")
    util.create_dir(template_dir_user)

    logging.info("Reading system templates from: %s", template_dir)
    logging.info("Reading user templates from: %s", template_dir_user)
    for file in [*walk(template_dir), *walk(template_dir_user)]:
        if file.name != ".DS_Store" and not file.name.endswith(".swp"):
            template(colors, file.path, join(output_dir, file.relative_path))

    logging.info("Exported all files.")
    logging.info("Exported all user files to %s", output_dir)


def color(colors, export_type, output_file=None):
    """Export a single template file."""
    all_colors = flatten_colors(colors)

    template_name = get_export_type(export_type)

    if template_name == export_type:
        template_file = os.path.join(CONF_DIR, "templates", template_name)
    else:
        template_file = os.path.join(MODULE_DIR, "templates", template_name)

    output_file = output_file or os.path.join(CACHE_DIR, template_name)

    if os.path.isfile(template_file):
        template(all_colors, template_file, output_file)
        logging.info("Exported %s.", export_type)
    else:
        logging.warning("Template '%s' doesn't exist.", export_type)
