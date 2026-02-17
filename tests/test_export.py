"""Test export functions."""

import unittest
import shutil
import os

from pywal import export
from pywal import util


COLORS = util.read_file_json("tests/test_files/test_file3.json")
COLORS["colors"].update(COLORS["special"])

TMP_DIR = "/tmp/wal"
TEMPLATES = "pywal/templates"


class TestExportColors(unittest.TestCase):
    """Test the export functions."""

    def setUp(self):
        """> Setup export tests."""
        util.create_dir(TMP_DIR)
        # copy template files to tmp dir
        shutil.copytree(TEMPLATES, TMP_DIR, dirs_exist_ok=True)

    def tearDown(self):
        """> Clean up export tests."""
        shutil.rmtree(TMP_DIR, ignore_errors=True)

    def is_file(self, tmp_file):
        """> Test is something is a file."""
        result = os.path.isfile(tmp_file)
        self.assertTrue(result)

    def is_file_contents(self, tmp_file, pattern):
        """> Check for pattern in file."""
        content = util.read_file(tmp_file)
        self.assertEqual(content[6], pattern)

    def test_all_templates(self):
        """> Test substitutions in template file."""
        tmp_file = os.path.join(TMP_DIR, "colors.sh")
        export.every(COLORS, TMP_DIR)

        self.is_file(tmp_file)
        self.is_file_contents(tmp_file, "foreground='#F5F1F4'")

    def test_css_template(self):
        """> Test substitutions in template file (css)."""
        tmp_file = os.path.join(TMP_DIR, "test.css")
        export.color(COLORS, "css", tmp_file)

        self.is_file(tmp_file)
        self.is_file_contents(tmp_file, "    --background: #1F211E;")


class TestParser(unittest.TestCase):
    """Test the Parser class."""

    def test_parse_name(self):
        """> Test parsing function names."""
        result = export.Parser.parse_name("func_name(arg1, arg2)", 0)
        self.assertEqual(result, ("func_name", 9))

        result = export.Parser.parse_name("  spacing_not_allowed  (arg1, arg2)", 0)
        self.assertIsNone(result)

        result = export.Parser.parse_name("123invalid(arg1, arg2)", 0)
        self.assertIsNone(result)

    def test_parse_args(self):
        """> Test parsing function arguments."""
        result = export.Parser.parse_args("(100,20.0)", 0)
        self.assertEqual(result, ([100, 20.0], 10))

        result = export.Parser.parse_args("(-100.0, -20)", 0)
        self.assertEqual(result, ([-100.0, -20], 13))

        result = export.Parser.parse_args("invalid_arg_format", 0)
        self.assertIsNone(result)

        result = export.Parser.parse_args("( non_numeric, args )", 0)
        self.assertIsNone(result)

        result = export.Parser.parse_args("()", 0)
        self.assertEqual(result, ([], 2))

    def test_parse_function(self):
        """> Test parsing functions."""
        result = export.Parser.parse_function("func_name(1, 2) .func2()", 0)
        self.assertEqual(
            result,
            (("func_name", [1, 2]), 15),
        )

        result = export.Parser.parse_function(
            "  again_no_spaces ( 1 , 2 ) . func2 ( ) ", 0
        )
        self.assertIsNone(result)

        result = export.Parser.parse_function("invalid_func_format", 0)
        self.assertIsNone(result)

    def test_parse_marker(self):
        """> Test parsing markers."""
        result = export.Parser.parse_marker("color0.func_name(1, 2).func2().rgb")
        self.assertEqual(
            result,
            (
                (
                    "color0",
                    [
                        ("func_name", [1, 2]),
                        ("func2", []),
                    ],
                    "rgb",
                ),
                34,
            ),
        )

        result = export.Parser.parse_marker("background.lighten(1)")
        self.assertEqual(
            result,
            (
                ("background", [("lighten", [1])], None),
                21,
            ),
        )

        result = export.Parser.parse_marker("color0")
        self.assertEqual(result, (("color0", [], None), 6))

        result = export.Parser.parse_marker("!invalid_marker_format")
        self.assertIsNone(result)
        result = export.Parser.parse_marker("color0.invalid-func()")
        self.assertIsNone(result)
        result = export.Parser.parse_marker("color0.func(1, invalid_arg)")
        self.assertIsNone(result)

    def test_execute_marker(self):
        """> Test executing markers."""
        colors = {
            "color0": util.Color("#000000"),
            "color1": util.Color("#FFFFFF"),
            "color2": util.Color("#F5F1F4"),
            "color3": util.Color("#1F211E"),
            "color4": util.Color("#262826"),
            "color5": util.Color("#D0D0D1"),
            "color6": util.Color("#A3A3A4"),
            "background": util.Color("#1F211E"),
            "foreground": util.Color("#F5F1F4"),
            "cursor": util.Color("#31282F"),
            "color15": util.Color("#000000"),
        }

        tests = [
            ("color0.lighten(100).rgb", "255,255,255"),
            ("color1.darken(100)", "#000000"),
            ("color2.adjust_alpha(50).hex_argb", "#7FF5F1F4"),
            ("color3.saturate(50).decimal", "#1715983"),
            ("color3.saturate(50).decimal_strip", "1715983"),
            ("color4.saturate(-50).octal", "#4635023"),
            ("color4.saturate(-50).octal_strip", "4635023"),
            ("color5.lighten(20)", "#d9d9da"),
            ("color6.darken(20).strip", "828283"),
            ("background", "#1F211E"),
            ("background.lighten(10).darken(10).octal", "#13630456"),
            ("background.lighten(10).darken(10)", "#2f312e"),
            ("foreground.lighten(10)", "#f6f2f5"),
            ("cursor.darken(10)", "#2c242a"),
        ]

        for marker_str, expected in tests:
            marker = (
                parsed[0]
                if (parsed := export.Parser.parse_marker(marker_str)) is not None
                else self.fail("Parsing marker failed")
            )
            result = export.Parser.execute_marker(colors, marker)
            self.assertEqual(result, expected)


class TestIssue13(unittest.TestCase):
    TEMPLATE = r"""
# Special
background='{background}'
foreground='{foreground}'
cursor='{cursor}'

# background colors
backgroundl1='#{background.lighten(1)}'
backgroundl2='#{background.lighten(2)}'
backgroundl3='#{background.lighten(3)}'
backgroundl4='#{background.lighten(4)}'
backgroundl5='#{background.lighten(5)}'
backgroundl6='#{background.lighten(10)}'
backgroundd1='#{background.darken(1)}'
backgroundd2='#{background.darken(2)}'
backgroundd3='#{background.darken(3)}'
backgroundd4='#{background.darken(4)}'
backgroundd5='#{background.darken(5)}'
backgroundd6='#{background.darken(10)}'

# colors
color0='{color0}'
color1='{color1}'
color2='{color2}'
color3='{color3}'
color4='{color4}'
color5='{color5}'
color6='{color6}'
color7='{color7}'
color8='{color8}'
color9='{color9}'
color10='{color10}'
color11='{color11}'
color12='{color12}'
color13='{color13}'
color14='{color14}'
color15='{color15}'

# colors rgbspce
color0='{color0.rgbspace}'
color1='{color1.rgbspace}'
color2='{color2.rgbspace}'
color3='{color3.rgbspace}'
color4='{color4.rgbspace}'
color5='{color5.rgbspace}'
color6='{color6.rgbspace}'
color7='{color7.rgbspace}'
color8='{color8.rgbspace}'
color9='{color9.rgbspace}'
color10='{color10.rgbspace}'
color11='{color11.rgbspace}'
color12='{color12.rgbspace}'
color13='{color13.rgbspace}'
color14='{color14.rgbspace}'
color15='{color15.rgbspace}'

# Colors float
color0='{color0.red} {color0.green} {color0.blue}'
color1='{color1.red} {color1.green} {color1.blue}'
color2='{color2.red} {color2.green} {color2.blue}'
color3='{color3.red} {color3.green} {color3.blue}'
color4='{color4.red} {color4.green} {color4.blue}'
color5='{color5.red} {color5.green} {color5.blue}'
color6='{color6.red} {color6.green} {color6.blue}'
color7='{color7.red} {color7.green} {color7.blue}'
color8='{color8.red} {color8.green} {color8.blue}'
color9='{color9.red} {color9.green} {color9.blue}'
color10='{color10.red} {color10.green} {color10.blue}'
color11='{color11.red} {color11.green} {color11.blue}'
color12='{color12.red} {color12.green} {color12.blue}'
color13='{color13.red} {color13.green} {color13.blue}'
color14='{color14.red} {color14.green} {color14.blue}'
color15='{color15.red} {color15.green} {color15.blue}'

# Colors hex
color0='{color0.red_hex} {color0.green_hex} {color0.blue_hex}'
color1='{color1.red_hex} {color1.green_hex} {color1.blue_hex}'
color2='{color2.red_hex} {color2.green_hex} {color2.blue_hex}'
color3='{color3.red_hex} {color3.green_hex} {color3.blue_hex}'
color4='{color4.red_hex} {color4.green_hex} {color4.blue_hex}'
color5='{color5.red_hex} {color5.green_hex} {color5.blue_hex}'
color6='{color6.red_hex} {color6.green_hex} {color6.blue_hex}'
color7='{color7.red_hex} {color7.green_hex} {color7.blue_hex}'
color8='{color8.red_hex} {color8.green_hex} {color8.blue_hex}'
color9='{color9.red_hex} {color9.green_hex} {color9.blue_hex}'
color10='{color10.red_hex} {color10.green_hex} {color10.blue_hex}'
color11='{color11.red_hex} {color11.green_hex} {color11.blue_hex}'
color12='{color12.red_hex} {color12.green_hex} {color12.blue_hex}'
color13='{color13.red_hex} {color13.green_hex} {color13.blue_hex}'
color14='{color14.red_hex} {color14.green_hex} {color14.blue_hex}'
color15='{color15.red_hex} {color15.green_hex} {color15.blue_hex}'

# Colors dec
color0='{color0.red_dec} {color0.green_dec} {color0.blue_dec}'
color1='{color1.red_dec} {color1.green_dec} {color1.blue_dec}'
color2='{color2.red_dec} {color2.green_dec} {color2.blue_dec}'
color3='{color3.red_dec} {color3.green_dec} {color3.blue_dec}'
color4='{color4.red_dec} {color4.green_dec} {color4.blue_dec}'
color5='{color5.red_dec} {color5.green_dec} {color5.blue_dec}'
color6='{color6.red_dec} {color6.green_dec} {color6.blue_dec}'
color7='{color7.red_dec} {color7.green_dec} {color7.blue_dec}'
color8='{color8.red_dec} {color8.green_dec} {color8.blue_dec}'
color9='{color9.red_dec} {color9.green_dec} {color9.blue_dec}'
color10='{color10.red_dec} {color10.green_dec} {color10.blue_dec}'
color11='{color11.red_dec} {color11.green_dec} {color11.blue_dec}'
color12='{color12.red_dec} {color12.green_dec} {color12.blue_dec}'
color13='{color13.red_dec} {color13.green_dec} {color13.blue_dec}'
color14='{color14.red_dec} {color14.green_dec} {color14.blue_dec}'
color15='{color15.red_dec} {color15.green_dec} {color15.blue_dec}'
    """

    EXPECTED = """
# Special
background='#1F211E'
foreground='#F5F1F4'
cursor='#F5F1F4'

# background colors
backgroundl1='##212320'
backgroundl2='##232522'
backgroundl3='##252724'
backgroundl4='##272927'
backgroundl5='##2a2c29'
backgroundl6='##353734'
backgroundd1='##1e201d'
backgroundd2='##1e201d'
backgroundd3='##1e201d'
backgroundd4='##1d1f1c'
backgroundd5='##1d1f1c'
backgroundd6='##1b1d1b'

# colors
color0='#1F211E'
color1='#4B7A85'
color2='#CC6A93'
color3='#5C9894'
color4='#A0A89B'
color5='#D1B9A9'
color6='#E3D6D8'
color7='#F5F1F4'
color8='#666666'
color9='#4B7A85'
color10='#CC6A93'
color11='#5C9894'
color12='#A0A89B'
color13='#D1B9A9'
color14='#E3D6D8'
color15='#F5F1F4'

# colors rgbspce
color0='31 33 30'
color1='75 122 133'
color2='204 106 147'
color3='92 152 148'
color4='160 168 155'
color5='209 185 169'
color6='227 214 216'
color7='245 241 244'
color8='102 102 102'
color9='75 122 133'
color10='204 106 147'
color11='92 152 148'
color12='160 168 155'
color13='209 185 169'
color14='227 214 216'
color15='245 241 244'

# Colors float
color0='0.122 0.129 0.118'
color1='0.294 0.478 0.522'
color2='0.800 0.416 0.576'
color3='0.361 0.596 0.580'
color4='0.627 0.659 0.608'
color5='0.820 0.725 0.663'
color6='0.890 0.839 0.847'
color7='0.961 0.945 0.957'
color8='0.400 0.400 0.400'
color9='0.294 0.478 0.522'
color10='0.800 0.416 0.576'
color11='0.361 0.596 0.580'
color12='0.627 0.659 0.608'
color13='0.820 0.725 0.663'
color14='0.890 0.839 0.847'
color15='0.961 0.945 0.957'

# Colors hex
color0='1F 21 1E'
color1='4B 7A 85'
color2='CC 6A 93'
color3='5C 98 94'
color4='A0 A8 9B'
color5='D1 B9 A9'
color6='E3 D6 D8'
color7='F5 F1 F4'
color8='66 66 66'
color9='4B 7A 85'
color10='CC 6A 93'
color11='5C 98 94'
color12='A0 A8 9B'
color13='D1 B9 A9'
color14='E3 D6 D8'
color15='F5 F1 F4'

# Colors dec
color0='31 33 30'
color1='75 122 133'
color2='204 106 147'
color3='92 152 148'
color4='160 168 155'
color5='209 185 169'
color6='227 214 216'
color7='245 241 244'
color8='102 102 102'
color9='75 122 133'
color10='204 106 147'
color11='92 152 148'
color12='160 168 155'
color13='209 185 169'
color14='227 214 216'
color15='245 241 244'
    """

    def setUp(self) -> None:
        util.create_dir(TMP_DIR)
        # copy TEMPLATE to a tmp file
        with open(os.path.join(TMP_DIR, "issue13_template.txt"), "w") as f:
            f.write(self.TEMPLATE)
        return super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
        return super().tearDown()

    def test_issue_13(self):
        """
        Test issue #13.
        just make sure this doesn't crash, and produces sane output
        """
        self.maxDiff = None
        tmp_file = os.path.join(TMP_DIR, "issue13_template.txt")
        out_file = os.path.join(TMP_DIR, "issue13_output.txt")

        colors = export.flatten_colors(COLORS)

        export.template(colors, tmp_file, out_file)

        self.assertTrue(os.path.isfile(out_file))

        with open(out_file, "r") as f:
            content = f.read()

        self.assertEqual(content, self.EXPECTED)


if __name__ == "__main__":
    unittest.main()
