"""
Reload programs.
"""

import logging
import os
import shutil
import subprocess
import time

from .settings import CACHE_DIR, MODULE_DIR, OS
from . import util


def tty(tty_reload):
    """Load colors in tty."""
    tty_script = os.path.join(CACHE_DIR, "colors-tty.sh")
    term = os.environ.get("TERM")

    if tty_reload and term == "linux":
        subprocess.Popen(["sh", tty_script])


def xrdb(xrdb_files=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_files = xrdb_files or [os.path.join(CACHE_DIR, "colors.Xresources")]

    if shutil.which("xrdb") and OS != "Darwin":
        for file in xrdb_files:
            subprocess.run(["xrdb", "-merge", "-quiet", file], check=False)


def i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg") and util.get_pid("i3"):
        util.disown(["i3-msg", "reload"])


def bspwm():
    """Reload bspwm colors."""
    if shutil.which("bspc") and util.get_pid("bspwm"):
        util.disown(["bspc", "wm", "-r"])


def kitty():
    """Reload kitty colors."""
    if shutil.which("kitty") and util.get_pid("kitty"):
        if os.getenv("TERM") == "xterm-kitty":
            subprocess.call(
                [
                    "kitty",
                    "@",
                    "set-colors",
                    "--all",
                    os.path.join(CACHE_DIR, "colors-kitty.conf"),
                ]
            )
        else:
            subprocess.call(
                [
                    "kitty",
                    "@",
                    "--to",
                    "unix:/tmp/kitty_pywal",
                    "set-colors",
                    "--all",
                    os.path.join(CACHE_DIR, "colors-kitty.conf"),
                ]
            )


def polybar():
    """Reload polybar colors."""
    if shutil.which("polybar") and util.get_pid("polybar"):
        util.disown(["pkill", "-USR1", "polybar"])


def sway():
    """Reload sway colors."""
    if shutil.which("swaymsg") and util.get_pid("sway"):
        util.disown(["swaymsg", "reload"])


def firefox():
    """reload pywalfox."""
    if shutil.which("pywalfox"):
        util.disown(["pywalfox", "update"])


def waybar():
    """Reload waybar colors."""
    if shutil.which("waybar") and util.get_pid("waybar"):
        util.disown(["pkill", "-USR2", "waybar"])


def colors(cache_dir=CACHE_DIR):
    """Reload colors. (Deprecated)"""
    sequences = os.path.join(cache_dir, "sequences")

    logging.error("'wal -r' is deprecated: " "Use 'cat %s' instead.", sequences)

    if os.path.isfile(sequences):
        print("".join(util.read_file(sequences)), end="")


def termux():
    """reload termux colors."""
    if shutil.which("termux-reload-settings"):
        util.disown(["termux-reload-settings"])


def mako():
    """Reload mako colors."""
    if shutil.which("mako") and util.get_pid("mako"):
        util.disown(["makoctl", "reload"])


def nvim():
    """Reload nvim colors."""
    if shutil.which("nvim-colo-reload") and util.get_pid("nvim"):
        util.disown(["nvim-colo-reload"])


def env(xrdb_file=None, tty_reload=True):
    """Reload environment."""
    xrdb(xrdb_file)
    i3()
    bspwm()
    kitty()
    sway()
    polybar()
    nvim()
    waybar()
    termux()
    mako()
    firefox()
    logging.info("Reloaded environment.")
    tty(tty_reload)
