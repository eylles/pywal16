"""Set the wallpaper."""

import ctypes
import logging
import os
import re
import shutil
import subprocess
import urllib.parse
import plistlib
import datetime
import tempfile

from .settings import HOME, OS, CACHE_DIR
from . import util


def get_desktop_env():
    """Identify the current running desktop environment."""
    desktop = os.environ.get("XDG_CURRENT_DESKTOP")
    if desktop:
        return desktop

    desktop = os.environ.get("DESKTOP_SESSION")
    if desktop:
        return desktop

    desktop = os.environ.get("GNOME_DESKTOP_SESSION_ID")
    if desktop:
        return "GNOME"

    desktop = os.environ.get("MATE_DESKTOP_SESSION_ID")
    if desktop:
        return "MATE"

    desktop = os.environ.get("SWAYSOCK")
    if desktop:
        return "SWAY"

    desktop = os.environ.get("DESKTOP_STARTUP_ID")
    if desktop and "awesome" in desktop:
        return "AWESOME"

    return None


def detect_display_protocol():
    """Detect the active display protocol (X11 or Wayland)."""
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"

    if os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        return "x11"

    return None


def xfconf(img):
    """Call xfconf to set the wallpaper on XFCE."""
    xfconf_re = re.compile(
        r"^/backdrop/screen\d/monitor(?:0|\w*)/"
        r"(?:(?:image-path|last-image)|workspace\d/last-image)$",
        flags=re.M,
    )
    xfconf_data = subprocess.check_output(
        ["xfconf-query", "--channel", "xfce4-desktop", "--list"],
        stderr=subprocess.DEVNULL,
    ).decode("utf8")
    paths = xfconf_re.findall(xfconf_data)
    for path in paths:
        util.disown(
            [
                "xfconf-query",
                "--channel",
                "xfce4-desktop",
                "--property",
                path,
                "--set",
                img,
            ]
        )


def set_wm_wallpaper(img):
    """Set the wallpaper for non desktop environments."""
    session_type = os.getenv('XDG_SESSION_TYPE')
    if not session_type:
        logging.error(
            "The XDG_SESSION_TYPE env var is not set "
            "falling back to Display protocol detection."
        )
        session_type = detect_display_protocol()

    if not session_type:
        logging.error(
            "Display protocol could not be determined. "
            "Detection requires either WAYLAND_DISPLAY (for Wayland) "
            "or DISPLAY (for X11) environment variables to be set. "
            "Only x11 and wayland display protocols are supported."
        )

    if session_type == "x11":
        # setters for x11
        if shutil.which("feh"):
            util.disown(["feh", "--bg-fill", img])

        elif shutil.which("xwallpaper"):
            util.disown(["xwallpaper", "--zoom", img])

        elif shutil.which("nitrogen"):
            util.disown(["nitrogen", "--set-zoom-fill", img])

        elif shutil.which("bgs"):
            util.disown(["bgs", "-z", img])

        elif shutil.which("hsetroot"):
            util.disown(["hsetroot", "-fill", img])

        elif shutil.which("habak"):
            util.disown(["habak", "-mS", img])

        elif shutil.which("display"):
            util.disown(["display", "-backdrop", "-window", "root", img])

        else:
            logging.error("No wallpaper setter found.")
            return

    elif session_type == "wayland":
        # setters for wayland
        if shutil.which("swww"):
            util.disown(["swww", "img", img])

        elif shutil.which("awww"):
            util.disown(["awww", "img", img])

        elif shutil.which("swaybg"):
            subprocess.call(["killall", "swaybg"])
            util.disown(["swaybg", "-m", "fill", "-i", img])

        elif shutil.which("wbg"):
            subprocess.call(["killall", "wbg"])
            util.disown(["wbg", img])

        else:
            logging.error("No wallpaper setter found.")
            return

    elif session_type:
        logging.error(
            "Wallpaper setting not supported for"
            f" '{session_type}' session type."
        )
    else:
        logging.error("Cannot set wallpaper for this session.")

        return


def set_desktop_wallpaper(desktop, img):
    """Set the wallpaper for the desktop environment."""
    desktop = str(desktop).lower()

    if "xfce" in desktop or "xubuntu" in desktop:
        xfconf(img)

    elif "muffin" in desktop or "cinnamon" in desktop:
        util.disown(
            [
                "gsettings",
                "set",
                "org.cinnamon.desktop.background",
                "picture-uri",
                "file://" + urllib.parse.quote(img),
            ]
        )

    elif "gnome" in desktop or "unity" in desktop:
        util.disown(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri-dark",
                "file://" + urllib.parse.quote(img),
            ]
        )
        util.disown(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                "file://" + urllib.parse.quote(img),
            ]
        )

    elif "mate" in desktop:
        util.disown(
            ["gsettings", "set", "org.mate.background", "picture-filename", img]
        )

    elif "sway" in desktop:
        util.disown(["swaymsg", "output", "*", "bg", img, "fill"])

    elif "awesome" in desktop:
        util.disown(
            [
                "awesome-client",
                "require('gears').wallpaper.maximized('{img}')".format(
                    **locals()
                ),
            ]
        )

    elif "kde" in desktop:
        string = """
            var allDesktops = desktops();for (i=0;i<allDesktops.length;i++){
            d = allDesktops[i];d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper", "org.kde.image",
            "General");d.writeConfig("Image", "%s")};
        """
        if shutil.which("qdbus6"):
            use_qdbus = "qdbus6"
        elif shutil.which("qdbus5"):
            use_qdbus = "qdbus5"
        elif shutil.which("qdbus"):
            use_qdbus = "qdbus"
        else:
            logging.error("No qdbus6, qdbus5 or qdbus binary found")
            return
        util.disown(
            [
                use_qdbus,
                "org.kde.plasmashell",
                "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript",
                string % img,
            ]
        )

    elif "hyprland" in desktop and shutil.which("hyprpaper"):
        util.disown(["hyprctl", "hyprpaper", "preload ", img])
        util.disown(["hyprctl", "hyprpaper", "wallpaper", ", " + img])
    else:
        set_wm_wallpaper(img)


def set_mac_wallpaper(img):
    """Set the wallpaper on macOS."""
    db_file = "Library/Application Support/Dock/desktoppicture.db"
    db_path = os.path.join(HOME, db_file)

    # Fresh installs of Sonoma will not have this file.
    # Check if file exists to make backwards compatibility forwards compatible.
    if os.path.isfile(db_path):

        # Put the image path in the database
        sql = 'insert into data values("%s"); ' % img
        subprocess.call(["sqlite3", db_path, sql])

        # Get the index of the new entry
        sql = "select max(rowid) from data;"
        new_entry = subprocess.check_output(["sqlite3", db_path, sql])
        new_entry = new_entry.decode("utf8").strip("\n")

        # Get all picture ids (monitor/space pairs)
        get_pics_cmd = ["sqlite3", db_path, "select rowid from pictures;"]
        pictures = subprocess.check_output(get_pics_cmd)
        pictures = pictures.decode("utf8").split("\n")

        # Clear all existing preferences
        sql += "delete from preferences; "

        # Write all pictures to the new image
        for pic in pictures:
            if pic:
                sql += "insert into preferences (key, data_id, picture_id) "
                sql += "values(1, %s, %s); " % (new_entry, pic)

        subprocess.call(["sqlite3", db_path, sql])

        # Kill the dock to fix issues with cached wallpapers.
        # macOS caches wallpapers and if a wallpaper is set that shares
        # the filename with a cached wallpaper, the cached wallpaper is
        # used instead.
        subprocess.call(["killall", "Dock"])

    # MacOS Sonomoa uses a plist file instead.  Interestingly the database
    # referenced above still exists, but doesn't seem to do anyything on Sonoma
    # so lets leave it for backward compatatility

    plist_path = (
        "Library/Application Support/com.apple.wallpaper/Store/Index.plist"
    )
    plist_path = os.path.join(HOME, plist_path)

    # Write a backup of plist file in temp in case something horrific happens
    with open(plist_path, "rb") as f:
        old_plist = plistlib.load(f)
        with tempfile.NamedTemporaryFile(
            prefix="pywal-plist-bk-", delete=False
        ) as g:
            logging.info(f"Backup plist file saved to {g.name}")
            plistlib.dump(old_plist, g)

    # Unfortunately these fields seem mandatory.  not extensively tested
    # - Configuration is a plist unto itself and a value is required
    with open(plist_path, "wb") as f:
        new_plist = {
            "Spaces": {},
            "SystemDefault": {
                "Desktop": {
                    "LastSet": datetime.datetime.now(),
                    "LastUse": datetime.datetime.now(),
                    "Content": {
                        "Choices": [
                            {
                                "Provider": "com.apple.wallpaper.choice.image",
                                "Files": [{"relative": f"file:///{img}"}],
                                "Configuration": b"",
                            }
                        ],
                        "Shuffle": "$null",
                    },
                },
                "Type": "individual",
                "Idle": {
                    "LastSet": datetime.datetime.now(),
                    "LastUse": datetime.datetime(
                        2023, 10, 21, 2, 51, 4, 435303
                    ),
                    "Content": {
                        "Choices": [
                            {
                                "Provider": "com.apple.wallpaper.choice.aerials",
                                "Files": [],
                                "Configuration": b"",
                            }
                        ],
                        "Shuffle": {
                            "Type": "afterDuration",
                            "Duration": [2341, 16172123445939666944],
                        },
                    },
                },
            },
            "Displays": {},
            "AllSpacesAndDisplays": {
                "Desktop": {
                    "LastSet": datetime.datetime.now(),
                    "LastUse": datetime.datetime.now(),
                    "Content": {
                        "Choices": [
                            {
                                "Provider": "com.apple.wallpaper.choice.image",
                                "Files": [{"relative": f"file:///{img}"}],
                                "Configuration": b'bplist00\xd2\x01\x02\x03\x0c_\x10\x0fbackgroundColorYplacement\xd2\x04\x05\x06\x0bZcomponentsZcolorSpace\xa4\x07\x08\t\n#?\xd0PPPPPP#?\xdaZZZZZZ#?\xe5UUUUUU#?\xf0\x00\x00\x00\x00\x00\x00O\x10Cbplist00_\x10\x17kCGColorSpaceGenericRGB\x08\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x10\x01\x08\r\x1f).9DIR[dm\xb3\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb5',
                            }
                        ],
                        "Shuffle": "$null",
                    },
                    "Last": datetime.datetime.now(),
                },
                "Type": "individual",
                "Idle": {
                    "LastSet": datetime.datetime.now(),
                    "LastUse": datetime.datetime.now(),
                    "Content": {
                        "Choices": [
                            {
                                "Provider": "com.apple.wallpaper.choice.aerials",
                                "Files": [],
                                "Configuration": b"",
                            }
                        ],
                        "Shuffle": {
                            "Type": "afterDuration",
                            "Duration": [2341, 16172123445939666944],
                        },
                    },
                },
            },
        }
        plistlib.dump(new_plist, f)
        f.close()
    subprocess.call(["killall", "WallpaperAgent"])


def set_win_wallpaper(img):
    """Set the wallpaper on Windows."""
    # There's a different command depending on the architecture
    # of Windows. We check the PROGRAMFILES envar since using
    # platform is unreliable.
    if "x86" in os.environ["PROGRAMFILES"]:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 3)
    else:
        # 'W' functions take unicode strings,
        # while 'A' functions take UTF-8 bytestrings.
        # (Python 3 strings are Unicode by default.)
        ctypes.windll.user32.SystemParametersInfoA(20, 0, str.encode(img), 3)


def change(img):
    """Set the wallpaper."""
    if not os.path.isfile(img):
        return

    desktop = get_desktop_env()

    if OS == "Darwin":
        set_mac_wallpaper(img)

    elif OS == "Windows":
        set_win_wallpaper(img)

    else:
        set_desktop_wallpaper(desktop, img)

    logging.info("Set the new wallpaper.")


def get(cache_dir=CACHE_DIR):
    """Get the current wallpaper."""
    current_wall = os.path.join(cache_dir, "wal")

    if os.path.isfile(current_wall):
        # make sure the file has some content in it,
        contents = util.read_file(current_wall)

        if len(contents) > 0:
            return contents[0]

    return "None"
