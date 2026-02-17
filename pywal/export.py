"""
Export colors in various formats.
"""

import logging
import os
import re
import shutil
from typing import List, Tuple, Union, Optional

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


class Parser:
    Name = str
    Number = Union[int, float]
    Argument = Number
    Property = Name
    Function = Tuple[Name, List[Argument]]
    Color = Name
    Marker = Tuple[Color, List[Function], Optional[Property]]

    @staticmethod
    def parse_name(s: str, i: int) -> Tuple[Name, int] | None:
        """Parse a name from the given substring

        Args:
            s (str): The substring to parse the name from.
            i (int): The starting index in the substring.

        Returns:
            (str,int): The name and the position after the name.
            None: If a valid name is not found.
        """
        match = re.match(r"^[a-zA-Z][a-zA-Z0-9_]*", s[i:])
        if match:
            return match.group(0), match.end() + i
        return None

    @staticmethod
    def parse_property(s: str, i: int) -> Tuple[Property, int] | None:
        """Parse a property from a template file.

        BNF Grammar of a property (the text after the last dot):

        property ::= name
        name ::= [a-zA-Z][a-zA-Z0-9_]*
        """
        return Parser.parse_name(s, i)

    @staticmethod
    def parse_number(s: str, i: int) -> Tuple[Number, int] | None:
        """Parse a number (integer or float) from the given substring."""
        match = re.match(r"^-?\d+(\.\d+)?", s[i:])
        if match:
            num_str = match.group(0)
            if "." in num_str:
                return float(num_str), match.end() + i
            else:
                return int(num_str), match.end() + i
        return None

    @staticmethod
    def parse_argument(s: str, i: int) -> Tuple[Argument, int] | None:
        return Parser.parse_number(s, i)

    @staticmethod
    def parse_args(s: str, i: int) -> Tuple[List[Argument], int] | None:
        """Parse a list of arguments from a template file.

        BNF Grammar of a list of arguments (the text inside the parentheses):

        arguments ::= argument (',' argument)*
        argument ::= number
        """
        match = re.match(r"^\(([^\)]*)\)", s[i:])
        if not match:
            return None
        args_str = match.group(1)
        args = []
        if args_str:
            for arg in args_str.split(","):
                if (parsed := Parser.parse_argument(arg.strip(), 0)) is not None:
                    args.append(parsed[0])  # the parsed number, ignore the position
                else:
                    return None  # an argument could not be parsed

        if len(args) == 0 and args_str.strip():
            return None  # there were arguments but none could be parsed

        return args, match.end() + i

    @staticmethod
    def parse_function(s: str, i: int) -> Tuple[Function, int] | None:
        """Parse a function from a template file.

        BNF Grammar of a function (the text after the last dot):

        function ::= name '(' (argument (',' argument)*)? ')'
        """
        # parse the function name
        name = None
        after_name_pos = i
        if (parsed := Parser.parse_name(s, i)) is not None:
            name, after_name_pos = parsed
        else:
            return None

        # parse the arguments
        args = None
        if (parsed := Parser.parse_args(s, after_name_pos)) is not None:
            args, match_end = parsed
            return (name, args), match_end

        return None

    @staticmethod
    def parse_marker(s: str) -> Tuple[Marker, int] | None:
        """Parse a marker from a template file.

        BNF Grammar of a marker (the text inside the curly braces):

        marker ::= color ('.' function)* ('.' property)?
        color ::= name
        function ::= name arguments
        arguments ::= '(' (argument (',' argument)*)? ')'
        property ::= name
        name ::= [a-zA-Z][a-zA-Z0-9_]*
        argument ::= number
        """
        i = 0
        # parse the color
        color = None
        after_color_pos = i
        if (parsed := Parser.parse_name(s, i)) is not None:
            color, after_color_pos = parsed
        else:
            return None

        # parse functions and property
        functions = []
        prop = None
        i = after_color_pos
        while i < len(s):
            if s[i] == ".":
                i += 1
                # try to parse a function first
                if (parsed := Parser.parse_function(s, i)) is not None:
                    func, after_func_pos = parsed
                    functions.append(func)
                    i = after_func_pos
                # if no function, try to parse a property
                elif (parsed := Parser.parse_property(s, i)) is not None:
                    prop, after_prop_pos = parsed
                    i = after_prop_pos
                    break  # property must be the last element
                else:
                    return None  # neither function nor property found
            else:
                break  # no more functions or properties

        if i != len(s):
            return None  # not all input was consumed

        return (color, functions, prop), i

    @staticmethod
    def execute_marker(colors: dict, marker: Marker) -> str:
        """Execute a parsed marker and return the resulting color string."""
        cname, funcs, prop = marker
        if cname not in colors:
            raise ValueError(f"Color '{cname}' not found in colors dictionary.")

        new_color = util.Color(colors[cname].hex_color)

        for func in funcs:
            fname, args = func
            if not hasattr(new_color, fname):
                raise ValueError(f"Function '{fname}' not found in Color class.")
            function = getattr(new_color, fname)
            if callable(function):
                new_color = function(*args) if args else function()
            else:
                raise ValueError(
                    f"The {fname} attribute of the Color class is not callable"
                )

        if prop:
            if not hasattr(new_color, prop):
                raise ValueError(f"Property '{prop}' not found in Color class.")
            new_color = getattr(new_color, prop)

        return (
            str(new_color).strip()
            if isinstance(new_color, util.Color)
            else str(new_color)
        )


def template(colors, input_file, output_file=None):
    """Read template file, substitute markers and
    save the file elsewhere."""
    # pylint: disable-msg=too-many-locals
    template_data = util.read_file_raw(input_file)
    for i, line in enumerate(template_data):
        for match in re.finditer(
            r"(?<=(?<!\{))(\{([^{}]+)\})(?=(?!\}))", line
        ):  # find all {...} not surrounded by {}, and parse them
            marker = None
            if (parsed := Parser.parse_marker(match.group(2))) is not None:
                marker, _ = parsed
            if marker is None:
                logging.error(
                    "Syntax error in template file '%s' on line '%s'",
                    input_file,
                    i,
                )
                return

            # attempt to execute the marker
            replace_str = match.group(1)  # the full {marker}
            try:
                # execute the marker
                new_color = Parser.execute_marker(colors, marker)
                # replace the marker with its result
                template_data[i] = line.replace(replace_str, new_color, 1)
                line = template_data[i] # update the line for further replacements
            except ValueError as exc:
                logging.error(
                    "Error executing marker in template file '%s' on line '%s': %r",
                    input_file,
                    i,
                    exc,
                )
                continue
    # template_data is of type list, so we create template_string to do string
    # replacement operations
    template_string = "".join(template_data)
    template_string = template_string.replace("{{", "{")
    template_string = template_string.replace("}}", "}")

    util.save_file("".join(template_string), output_file)


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


def get_export_type(export_type: str):
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

            img = Image.new("RGB", (16, 1))
            for i, color in enumerate(colors["colors"].values()):
                img.paste(Image.new("RGB", (1, 1), color), (i, 0))
            img.save(os.path.join(destdir, "colors.png"))
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
