import datetime

ricing_feels_soulless = """
Holy shit I just realized why ricing feels so soulless in the age of hyprland,
it's because nobody respects color schemes anymore.

Gone are the days of base16 or even base8, now everything is pywal (or whatever
derivative is the current meta) with poorly recolored wallpapers. People don't
care about color balance or variety anymore, that's why everything looks so
samey and why it feels like there's a "hyprland aesthetic" -- it's
transparency+blur with a wallpaper and colorscheme that have no variety;
they're almost entirely monochrome or otherwise poorly created by a program
rather than someone with an actual eye.

On top of this, I think another major part is how people don't respect pairing
wallpapers and color schemes anymore. It's always premade wallpapers to match
the theme (catppuccin/gruvbox), wallpapers recolored by a program to match the
theme (aster or equivalent), or themes created by a program to match the
wallpaper (pywal or equivalent). There used to be an art to this, but people
don't care about it anymore.

And even when people don't use pywal, it's going to be gruvbox or catppuccin or
whatever other soulless theme is the meta. I remember hating nord when it was
popular, but I would give anything to see some nord rices instead of the same
catppuccin and gruvbox ones.

TLDR people don't care about color schemes anymore and would prefer to use a
poorly cobbled together one from a program or a premade theme rather than
putting any form of effort in.
"""

gimp = """
GIMP = Green Is My Pepper
"""


def eemsg():
    if datetime.datetime.now().month == 4 and datetime.datetime.now().day == 1:
        print(ricing_feels_soulless)
    if datetime.datetime.now().month == 3 and datetime.datetime.now().day == 16:
        print(gimp)
