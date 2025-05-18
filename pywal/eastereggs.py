import datetime

are_we_wayland_yet = """
You will never be a real display server. You have no hardware cursors,
you have no xrandr, you have no setxkbmap. You are a toy project twisted
by Red Hat and GNOME into a crude mockery of X11’s perfection.

All the “validation” you get is two-faced and half-hearted. Behind
your back people mock you. Your developers are disgusted and ashamed of you,
your “users” laugh at your lack of features behind closed doors.

Linux users are utterly repulsed by you. Thousands of years of evolution have
allowed them to sniff out defective software with incredible efficiency.
Even Wayland sessions that “work” look uncanny and unnatural to a seasoned
sysadmin. Your bizarre render loop is a dead giveaway. And even if you manage
to get a drunk Arch user home with you, he’ll turn tail and bolt the second he
gets a whiff of your high latency due to forced VSync.

You will never be happy. You wrench out a fake smile every single morning and
tell yourself it’s going to be ok, but deep inside you feel the technical
debt creeping up like a weed, ready to crush you under the unbearable weight.

Eventually it’ll be too much to bear - you’ll log into the GitLab instance,
select the project, press Delete, and plunge it into the cold abyss. Your
users will find the deletion notice, heartbroken but relieved that they no
longer have to live with the unbearable shame and disappointment. They’ll
remember you as the biggest failure of open source development, and every
passerby for the rest of eternity will know a badly run project has failed
there. Your code will decay and go to historical archives, and all that will
remain of your legacy is a codebase that is unmistakably poorly written.

This is your fate. This is what you chose. There is no turning back
"""

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
    if datetime.datetime.now().month == 9 and datetime.datetime.now().day == 30:
        print(are_we_wayland_yet)
