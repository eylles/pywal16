# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.8.10] - 2025-09-29
Fixes:
- Use exact name for waybar and polybar.
- More reliable imagemagick output parsing.
- Make the behaviour of the --saturation flag more intuitive.

New:
- `foot` consider alpha for the default template.
- `ultrakill` palette generation.

## [3.8.9] - 2025-05-31
Fixes:
- Fix the fix that was not fixed with `--out-dir`.

## [3.8.8] - 2025-05-31
Fixes:
- Error during color export.

## [3.8.7] - 2025-05-31
Fixes:
- Ensure alpha value is the correct type and is within valid range.
- Increase saturation of very dark theme background colors.

New:
- Prefer the alpha value from flag over the theme alpha.
- Allow the `--saturate` flag to affect colors 0 and 8.
- Added the `--out-dir` flag to allow changing export dir, it overrides the value of '$PYWAL_CACHE_DIR'.

## [3.8.6] - 2025-04-14
Fixes:
- `pywal` no longer crashes on windows when `colorama` is not present.

## [3.8.5] - 2025-03-31
New:
- Added tokyonight colorschemes.
- Set `alpha_num` value from command line even when loading theme files.
- Added mechanism to live reload nvim colors through `nvim-colo-reload`.

## [3.8.4] - 2025-03-25
New:
- Added rosepine colorschemes.
- Support reloading of mako.

## [3.8.3] - 2025-03-16
New:
- `retroarch` rgui colors template.
- `termux` support.

Fixes:
- `KDE` 6.3.3 error where pywal would crash upon failing to set the wallpaper.

## [3.8.2] - 2025-03-03
Fixes:
- Hyprland and Hyprpaper support actually this time.

    New:
- Fuzzel template.
- Tofi template.
- Mako template.
- Zathura template.
- webp image format support.

## [3.8.1] - 2025-02-23
Fixes:
- Hyprland and Hyprpaper support working properly.

New:
- Hyprland colors template.
- dwl colors template.
- Added support for `wbg`.
- Added catpuccin colorschemes.

## [3.8.0] - 2025-02-15

New features:
- Added Dynamic shade conversion, using the `--cols16` flag will convert 9 shades themes to 16 shades.
- Added Nested template directories, subdirectories with templates can be created inside the templates dir.
- Added support for pywalfox.
- Added support for waybar.
- Added support for hyprpaper.
- Added Dracula colorschemes.
- Added ghostty template.
- Added base16-kanagawa colorscheme.
- Added color template for dwm urgent window patch.

Bug fixes and Improvements:
- Better colors for Fish.
- Restrict colorama import only to ms windows.
- Change dwm selection background to match dmenu.

Removals:
- gtk reloading, python 2 is obsolete and that method worked only for gtk2.

## [3.7.2] - 2024-11-29

- make color.get and color.cache_fname API more backwards compatible.

## [3.7.1] - 2024-11-27

- Use test_file3.json in test_export.py.

## [3.7.0] - 2024-11-27

- Added `foot` terminal emulator template.
- Added `zed` template.
- Remove redundant template `colors.hs`.
- Add `--contrast` option.
- Enable MS Windows color output.
- Use kwargs for the cols16 and contrast internal API.
- Improved info log to include template directory paths.
- Add optional dependencies to setup.py.
- Made `checksum` available to the colorscheme dict.
- Added `adjust_alpha` function to be used in templates.
- Added support for MacOS Sonoma.
- Added manpage `wa.1`.
- Changed formatting to use `BLACK` formatter.

## [3.6.0] - 2024-07-04

- Fixed empty message on KDE plasma when sending sequences.
- Add the `okthief` backend.
- Fix issue with `fcntl` in unsupported platforms.
- Explicitly add the method by which 16 colors scheme is created to the file name.
- Fix the darkness of color 0
- Fix the darkness and saturation of colors 7 and 8

## [3.5.3] - 2024-06-02

- fixed issue with `wal` backend on arch where it would fail to generate a colorscheme.

## [3.5.3] - 2024-05-07

- Fixed issue with `wal` backend sometimes reading garbage data form imagemagick.
- Added notice for Imagemagick 7 policy change, fix on wiki.
- Added custom `foreground` argument just like custom `background` argument.
- Change open files to write in non-blocking mode.

## [3.5.2] - 2024-05-06

- modified generic_adjust and added a pre-adjust to the colorthief backend to match legacy background colors

## [3.5.1] - 2024-04-20

- Added wallpaper checksum generation and comparison for cached color schemes.
- Added toml template for new `alacritty` versions.

## [3.5.0] - 2024-02-xx

- Added rgb color template.
- Added support for `swww`.
- Added wallpaper override when using a theme.
- Change `alacritty` template to match v11.0+ config.
- Change wallpaper path on microsoft windows uses bytestring.
- Change when pywal is used as module allow using user templates.
- Added swaybg wallpaper support.
- Change `--cols16` flag now supports arguments `darken` and `lighten` to generate the color palette.

## [3.4.0] - 2022-10-31

- Fixed template exporting issue, rewriting may be necessary for a proper fix.
- Added new properties red_dec, green_dec and blue_dec.
- Added new properties red_hex, green_hex and blue_hex.
- Added new property for templates `rgbspace`.
- Added `leftwm` support template colors-leftwm-theme.ron.
- Added support for gnome dark wallpapers.
- Fixed crash when '~/.cache/wal' is empty.
- Fixed `xmonad` support template Colors.hs added.
- Added support for ARGB hex strings, `hexargb` and `alpha_hex`
- Fixed color setting on OpenBSD.
- Fixed `kitty` reloading.
- Added `alacritty` templates colors--alacritty.yml and colors--nodim-alacritty.yml.
- Added `--cols16` flag to generate 16 color schemes.
- Added `fast_colorthief` backend.
- Fixed `rofi` template for rofi >v1.7.0
- Fixed wallpaper path on microsoft windows.
- Added `themer` template colors-themer.js.
- Fixed gruvbox colorscheme.
- Added KDE `plasma` support, wallpaper setting and template colors-nqq.css.
- Added decimal output support, `decimal`, `decimal_strip` for templates.
- Fixed template export, replace "." with "_".
- Fixed `hsetroot` support to set wallpaper, was duplicated.
- Added `xwallpaper` support to set wallpaper.
- Fixed `xrdb` reload, wait until reloading is finished.
- Added red green and blue properties to color class.
- Fixed template exporting issue.
- Added `tilix` template colors-tilix.json.
- Added support `st` on sequences.py
- Added ability to modify colors using `lighten`, `darken` and `saturate` in templates.
- Added indicator to last used theme on `--theme` flag (only for provided themes).
- Fixed eror if theme has never been set.
- Added `stylus` template colors.styl.
- Added `-w` flag to use last wallpaper for color generation.
- Added base16-snazzy colorscheme.
- Fixed `pidof` in MacOS.
- Added support `xfce` 4.12 and later.
- Fixed `kitty` support.
- Added `--recursive` option to search images in all subdird of the given dir.
- Fixed template `colors.sh` wallpaper quoting.
- Fixed `iterm2` cursor color.
- Fixed MacOS mojave Dock Crash.
- Added ability to load random user theme.
- Added ability to load random theme.
- Added ability to saving user themes.
- Added `bspwm` color setting support.
- Improved file size caching to avoid image name collisions.
- Fixed skip .swp files.
- Improved print error message when template cannot be read
- Improved use XDG dirs.
- Fixed error if `pidof` is not installed.
- Fixed `awesomewm` wallpaper setting.
- Added vscode template `colors-vscode.json`

## [3.3.0] - 2019-01-21

- Fixed `urxvt` borders not respecting background opacity
- Added ENVAR PYWAL_CACHE_DIR to change cache dir.
- Added `colors.hs` template for xmonad.
- Added `colors-wal-dmenu.h` template for dmenu.
- Added rgba support, funciton `rgba()`.
- Fixed `rofi` templates.
- Removed `oomox` support, use `wpgtk` instead.
- Added `colors-speedcrunch.json` template.
- Added `colors-waybar.css` template.
- Added `--vte` to fix artifacts on vte terminals.
- Fixed template `templates/colors-vivid.yml`.

## [3.2.1] - 2018-10-24

- Improved light colors (brighter colors)
- Fixed `urxvt` background

## [3.2.0] - 2018-10-23

- Simplified `colorz` backend
- Fixed `-c` now exits
- broken theme file removed `colorschemes/dark/dkeg-conv.sh.json`
- wal shows usage when no args are passed.
- Added `--preview flag` for current color palette.
- Added `kitty` support (reload and template).
- Fixed quiet mode with cached schemes.
- Fixed reloading by pid.
- Fixed Alpha setting.
- Added support for awesomewm to set wallpaper `set_desktop_wallpaper(desktop, img)`.
- Fixed reload `get_pid(name)` function.
- Added hash name for cache filename.
- Increased background contrast (darken set to 0.80, was 0.75)
- Fixed `putty` template.

## [3.1.0] - 2018-06-21

- Added `--saturate` to change color saturation.
    - Takes a float as its value: `0.0` to `1.0`.
- Added `vim` output file.
- Fixed `LS_COLORS` issue.
- Fixed issues in iTerm2 on macOS.
- Fixed hang caused by `imagemagick`.
- Fixed issue with `-i` and transparency.


## [3.0.1] - 2018-05-27

- Added Tempus themes.
- Added `LS_COLORS` to `colors.sh` to fix color issues.
- Compressed all theme files.
- Don’t print directory of image used.
- Fixed alpha value not persisting with `wal -R`.
- Fixed vim-airline theme when used with light color-schemes.


## [3.0.0] - 2018-05-06

Pywal now has **250** included themes! If there are any other themes
you'd like to see added. Open an issue.

- Added all of @dkeg's themes.
- Added all themes from [terminal.sexy](https://terminal.sexy)
- Themes are now split between `light` and `dark`.
    - Local themes now need to be put into `~/.config/wal/colorschemes/{light,dark}`.
- Added `unity` wallpaper support.

## [2.1.0] - 2018-04-29

- Added all `base16` themes to `pywal`. @metalelf0
- Added `--iterative` to iterate over a directory in order (*instead of random*).
- Fix minor theme issue in `rofi`. @esp10mm
- Fix some conflicting arguments.
- Fixed bug causing nested directory structure.
- Fixed bug where the configuration directory wouldn't be created early enough.
- Fixed missing color in `st` cache file. @jameh
- Limit color palette width in output.
- Removed `-nocpp` from `xrdb` call.


## [2.0.5] - 2018-04-05

- Fixed crash when using `--theme` on Python `3.5`.

## [2.0.4] - 2018-04-03

- Fixed cursor color
- Made output prettier

## [2.0.3] - 2018-04-02

-  args: Fixed bug where `--backend` wouldn't work.

## [2.0.2] - 2018-04-02

- Fixed bug where `wal -R` wouldn't work.
- Various cleanup and refactoring.
- Proper arg handling for `-R`, `-i` and `--theme`.

## [2.0.1] - 2018-04-01

- Fixed a bug where `pywal` wasn't updating files.
- Fixed a bug where `pywal` would crash if you tried to redirect it's output.

## [2.0.0] - 2018-04-01

This is a big release and I've probably broken something. Expect a minor release or two to fix any bugs that arise. ~~Users of `wpgtk` I recommend not updating `pywal` until @deviantfero adds support for the new release.~~ `wpgtk` is now supported.

It's going to take me some time to update the documentation (*I've got a total rewrite planned*). Bear with me.

## General


- xrdb: Added missing `background` and `foreground` values.
- image: Fixed crash when using light themes and gifs.
- args: Added `-t` to disable `pywal` in ttys.
- args: `-R` now works with theme files.
- sequences: Save sequence file with `-s`. @Amar1729
- misc: Added proper logging to `pywal`.
- misc: Added palette to console output.
- misc: Added colors/bold to console output.


## Backends

`pywal` now has support for different color generation backends. In addition to `pywal`'s default color generation, support was added for:

- `schemer2`: https://github.com/thefryscorer/schemer2
- `colorthief`: https://github.com/fengsp/color-thief-py
- `colorz`: https://github.com/metakirby5/colorz
- `haishoku`: https://github.com/LanceGin/haishoku

Usage:

- `wal --backend` lists all available backends.
- `wal --backend colorz -i img.jpg` sets the backend.
- `wal --backend random` uses a backend at random.

If you know of any other color generation programs let me know and I'll see if I can add backends for them.


## Themes

You can now store colorschemes in files and manage them using `pywal`. There are a bunch of colorschemes included with `pywal` and I will happily accept PRs to add more.

- `wal --theme` lists all available built-in themes.
- `wal --theme theme-name` applies a theme.
- `wal --theme random` applies a theme at random.
- Themes can be added locally at `~/.config/wal/colorschemes`.
- `wal --theme` can be used with colorschemes exported in `json` format from https://terminal.sexy/.
` wal --theme /path/to/file` loads a scheme from a file.

## [1.3.3] - 2018-03-03

- rofi: Added colon to template.
- tty.sh: Cleanup.
- sequences: Fixed terminal highlight colors.
- templates: Added octal color format. @MitchWeaver
- macOS: Fixed error with `.DS_Store` files. @blahsd
- macOS: Disabled travis (*It's really broken*)


## [1.3.2] - 2018-02-04

- Fixed comment colors not being a shade of grey.
- Added version to cache files.
- Removed broken notifications.

## [1.3.0] - 2018-02-03

- Added light colorscheme support.
    - Use `-l` to generate a light scheme.
    - You can use `wal -R -l` (swap to light) and `wal -R` (swap to dark) to swap between light and dark.

![scrot](https://i.imgur.com/VFzC7Vc.jpg)

## [1.2.3] - 2018-02-01

- Fixed typo in help. @gillescastel
- Scheme files are now versioned.
- Changed rofi theme to use the new `rasi` format.
    - New instructions: https://github.com/dylanaraps/pywal/wiki/Customization#rofi
- Added light/dark themes for rofi.
- Oomox is now **off** by default.
    - `-g` now enables oomox.

## [1.2.2] - 2018-01-09

- Added `-g` to skip generating a theme with `oomox`.

## [1.2.1] - 2018-01-08

Remember to use wal -c after every release.

- reload: Call oomox last so it doesn't block.

## [1.2.0] - 2018-01-08

Remember to use wal -c after every release.

- Added support for `oomox`.
    - See: https://github.com/dylanaraps/pywal/wiki/Customization#gtk2gtk3
- Removed support for `flatabulous-wal`.

## [1.1.2] - 2018-01-07

Remember to use `wal -c` after every release.

- fixed bug related to palette sorting.
- use color blending to create a better white.

## [1.1.1] - 2018-01-06

reload: Fixed permissions error.

## [1.1.0] - 2018-01-03

**general**

- Added support for changing colors in linux `ttys`.
- Fixed bug with transparency in urxvt.
- Added `imagemagick display` as a wallpaper setter fallback.

**api**

- Added missing export options.

**misc**

- Code cleanup.
- Minor optimizations.

## [1.0.4] - 2017-12-31

- reload: Fixed issue with rofi.
- reload: Speed up `xrdb` by using `-nocpp`

## [1.0.3] - 2017-12-31

- shuffle: Better error handling
- export: Added missing rofi option.

## [1.0.2] - 2017-12-29

- Add back `-r` for compatibility with `wpgtk`.
    - It's still deprecated.
    - An error message is still displayed.

## [1.0.1] - 2017-12-29

- colors: Improve background contrast.
- colors: Improve forground brightness and contrast.
- general: Fix `pywal` causing pc beeps.

## [1.0.0] - 2017-12-27

\[[Installation](https://github.com/dylanaraps/pywal/wiki/Installation)\] \[[Getting Started](https://github.com/dylanaraps/pywal/wiki/Getting-Started)\] \[[Customization](https://github.com/dylanaraps/pywal/wiki/Customization)\] \[[Wiki](https://github.com/dylanaraps/pywal/wiki)\]


This release of `pywal` contains some large changes and may very well break things for some users. Expect bugs and expect additional releases to fix them. The version has been bumped to `1.0.0` as I'm now happy with where `pywal` is feature-wise.

The goal for the future is improving the schemes that `pywal` generates. Feel free to send me your wallpapers that generate subpar schemes and I'll use them in my testing data.


### Removal of `-r`

The flag `-r` was removed as it was basically a glorified `cat` of the `sequences` file with **300ms** of python overhead. The new recommended way to load the schemes is to replace `wal -r` with `cat ~/.cache/wal/sequences`.


### Removal of `-t`

Yup! The `-t` flag to fix garbage in VTE terminals (termite, xfce4-terminal, gnome-terminal) is no longer needed. I've come up with a workaround that really **shouldn't work** but does. ¯\\\_(ツ)_/¯

The problem: The sequence  `\033[708;#000000\007` is unsupported by VTE and VTE's sequence parsing doesn't hide unknown sequences, instead it just displays them as plain text. We can't add an if statement or a check for VTE terminals as we're writing to each terminal via it's file descriptor. The only thing that is interpreted is escape sequences.

The workaround: The problem sequence is wrapped in a series of other escape sequences so that the unsupported sequence isn't echo'd to the terminal.

How it works:

```
# \0337                # Save cursor position.
# \033[1000H           # Move the cursor off screen.
# \033[8m              # Conceal text.
# \033]708;#000000\007 # Garbage sequence.
# \0338                # Restore cursor position.

\0337\033[1000H\033[8m\033]708;#000000\007\0338
```

This took a lot of trial and error to make sure it works across all terminals and doesn't cause issues for underlying terminal programs.


### Added User Template Support

You can now define your own custom `pywal` template files or you can overwrite the default template files. Any files stored in `~/.config/wal/templates` will be processed and exported to `~/.cache/wal/` under the same name.

The user template files follow the exact same syntax as the built-in templates. See the built-in templates for syntax examples: https://github.com/dylanaraps/pywal/tree/master/pywal/templates

For example: To define a custom `rofi` template file to set the background transparent.

Save this file to `~/.config/wal/templates/colors-rofi.Xresources` and re-run wal. Rofi will now use the colors defined below instead.

```
#define BG #CC{background.strip}
#define HI #CC{color1.strip}
#define FG {color15}
#define TX {color15}

! State:           bg, fg, bg2,  hlbg, hlfg
rofi.color-normal: BG, FG, BG,   HI,   TX
rofi.color-active: BG, FG, BG,   HI,   TX
rofi.color-urgent: BG, HI, BG,   HI,   FG
rofi.color-window: BG, BG, BG
```

### Templates

- Added template file for `rofi`.
- Added template file for `st`.
- Added template file for `tabbed`.
- Added template file for `dwm`.


### Args

- Added `-s` to disable changing terminal colors on the fly.

## [0.7.5] - 2017-12-19

- Really fixed wallpaper bug.

## [0.7.4] - 2017-12-19

- Fixed wallpaper not changing in WMs.

## [0.7.3] - 2017-12-17

- Fixed lint error.

## [0.7.2] - 2017-12-17

- Fixed license file not appearing in release tarballs.
- Fixed bug when using `pywal.reload.colors()`.
- Fixed shuffle not working with some file types.
- Fixed yaml error.
- Fixed sway error.
- Added sway wallpaper support.
- Made wallpaper setting faster for WMs.

## [0.7.0] - 2017-10-19

- Fixed failing tests on macOS. @linuxunil
- Added workaround for cursor color issues.
- Use run instead of popen so that things are closed correctly. @linuxunil
- Added resource file for Sway. @ranisalt
- Set `fzf` colors.

## [0.6.9] - 2017-08-27

- sequences: Fix flash on color reload.

## [0.6.8] - 2017-08-27

- Fixed `File not found` error on Windows.

## [0.6.7] - 2017-08-25

- os: Added support for Windows.
    - Cache dir on Windows is: `%UserProfile%\.cache\wal`
    - Wallpaper setting works on un-activated Windows copies (*neat*).
    - Note: Changing terminal colors doesn't work on Windows.
- xres: Fixed URxvt border not having transparency applied. @JoshuaRLi
- xres: Added `emacs` background/foreground. @adamsdarlingtower



## [0.6.6] - 2017-08-16

- reload: Fixed bug on macOS systems with XQuartz.

## [0.6.4] - 2017-08-15

- image: Fixed issue with relative file paths.

## [0.6.3] - 2017-08-13

- wallpaper: Remove useless print.

## [0.6.2] - 2017-08-13

- wallpaper: Fix `urllib` error when using GNOME or MATE.

## [0.6.1] - 2017-08-13

- wallpaper: Correctly encode file path to URI.

## [0.6.0] - 2017-08-12

- python: Added support for Python 3.5.
- api: `Path` types are no longer accepted by the api. Use `Strings` instead,

## [0.5.13] - 2017-08-12

- args: Added `-R` to restore the previous colorscheme.
- reload: Theme is now option for GTK reload. @deviantfero
- colors: Colors are now correctly set for UXTerm.
- tests: Added more tests. @aeikenberry

## [0.5.12] - 2017-08-03

- Fix wallpaper on macOS. @aeikenberry
- Added `-e` to skip reloading the environment. @aeikenberry

## [0.5.11] - 2017-08-02

- colors: Un-hardcode `color8`.
    - `color8` is now generated from `color0`.

## [0.5.10] - 2017-08-02

- `pywal` now colors iTerm2's window and tabs. @aeikenberry
- Fixed output message inconsistencies.

## [0.5.9] - 2017-07-31

- Fixed `hyper-wal` not working with `pywal`.

## [0.5.8] - 2017-07-31

- Added support for macOS (iTerm2 only)
    - Thanks to @aeikenberry for testing.
- Fixed issue with `tk`.
- Fixed bug with brighter background colors.

## [0.5.7] - 2017-07-30

- general: Use `sys.exit` everywhere instead of `exit`.
- export: Export colors in `yaml` format.
- wallpaper: Fix a crash on first run of `wal`.

## [0.5.6] - 2017-07-28

- css: Fixed wallpaper variable not working in `css`.

Updated `css` example:

```css
@import url('file:///home/dylan/.cache/wal/colors.css');

body {
  background-image: var(--wallpaper);
}
```

## [0.5.5] - 2017-07-28

- pypi: Don't load a 3MB image on pypi or github.
- pypi: Fixed README on pypi.
- install: Fixed pypandoc issue stopping install.
- install: Fixed gtk-reload not being installed with pip.



## [0.5.1] - 2017-07-28

- export: Added GTK2 support.
    - See: https://github.com/dylanaraps/pywal/wiki/Customization#gtk2
- image: Fixed bug causing shuffle to use duplicate images.
- args: Added `-b` to set a custom background color.
    - example: `wal -i img.jpg -b "#333333"`
- colors: `wal` now darkens the background color if the contrast between the wallpaper is too low.
    - See: #60 for an example.

## [0.5.0] - 2017-07-24

There aren't any breaking changes in this release but due to
the size I've bumped the major version number.

- api: `pywal` can now be imported and used as a module.
    - See [using pywal as a module](https://github.com/dylanaraps/pywal/wiki/Using-%60pywal%60-as-a-module).
- args: Added `-a` to control transparency. (URxvt only)
- comments: Removed redundent comments.
- linting: Removed lint comments.
- reload: Reload `polybar` colors automatically.
- speed: Sped up colorscheme generation by `5-6`x  by resizing image before processing.
- tests: Added more tests.
- util: Files are now saved safely.
    - Parent dirs are created on file save if they don't exist.



## [0.4.0] - 2017-07-10

- Wallpaper name/location is now cached in the export files.
- You can now specify a wallpaper to set in your custom co,oscheme files.
- `xclock` colors are now set.


Example coloscheme file with wallpaper:

```json
{
    "wallpaper": "/path/to/img.jpg",

    "special": {
        "background": "#4A3636",
        "foreground": "#F8F8F8",
        "cursor": "#F8F8F8"
    },
    "colors": {
        "color0": "#4A3636",
        "color1": "#EDD0B0",
        "color2": "#EDB7C8",
        "color3": "#E0D4DC",
        "color4": "#F4D3D0",
        "color5": "#F5E8D6",
        "color6": "#F5EDEA",
        "color7": "#F8F8F8",
        "color8": "#999999",
        "color9": "#EDD0B0",
        "color10": "#EDB7C8",
        "color11": "#E0D4DC",
        "color12": "#F4D3D0",
        "color13": "#F5E8D6",
        "color14": "#F5EDEA",
        "color15": "#F8F8F8"
    }
}
```

## [0.3.10] - 2017-07-08

- Better outdated Python version error.
- Fixed infinite loop when `wal` is given a very simple image.
- `wal` will now abort if it can't find `16` colors after 20 loops.
- Fixed a bug where a cached scheme would be used for the wrong image.

## [0.3.8] - 2017-07-07

- Added message to let the user know that `pywal` requires Python `3.6` or greater.

## [0.3.7] - 2017-07-06

- Remove executable permissions from Python files.
- Fix `set_grey()` type mismatch.
- Update docs.
- Fix a bug causing the wallpaper to not be set correctly.

## [0.3.6] - 2017-07-01

- template: Export generic xrdb special colors.

## [0.3.5] - 2017-06-30

- Add back `MANIFEST.in` as it's actually needed.

## [0.3.4] - 2017-06-30

- colors: Fix bug with `i3` titlebars being given the wrong colors.
- template: Added a template for Konsole theme generation.
- general: Remove `MANIFEST.in`. Turns out it's uneeded.

## [0.3.3] - 2017-06-30

- Remove non-ascii char from package description. #23

## [0.3.2] - 2017-06-30

- Really fix templates not being installed.

## [0.3.1] - 2017-06-30

- Fix templates not being installed with `pip`.

## [0.3.0] - 2017-06-30

- Add `-f` flag to read colorscheme from a file. @opatut
    - Added support for importing colors in a `.json` format.
- Exported files are now created using template files.
    - Added `json` export format. (`colors.json`)
- Fixed bug with wallpaper not being set in some Window Managers.

You can now import your own colorschemes using a json file in the following format:

```json
{
    "special": {
        "background": "#3A5130",
        "foreground": "#FAF9F5",
        "cursor": "#FAF9F5"
    },
    "colors": {
        "color0": "#3A5130",
        "color1": "#E3A19D",
        "color2": "#E1CEAE",
        "color3": "#D6DDCC",
        "color4": "#F1D2CB",
        "color5": "#F5E9D6",
        "color6": "#F9F0E5",
        "color7": "#FAF9F5",
        "color8": "#999999",
        "color9": "#E3A19D",
        "color10": "#E1CEAE",
        "color11": "#D6DDCC",
        "color12": "#F1D2CB",
        "color13": "#F5E9D6",
        "color14": "#F9F0E5",
        "color15": "#FAF9F5"
    }
}
```

## [0.2.6] - 2017-06-28

- Fix bug when shuffling images.
- Use `os.scandir` for a speed boost.


## [0.2.5] - 2017-06-27

- Added unit tests.

## [0.2.4] - 2017-06-27

- Remove `find_packages()`.

Note to self: Don't flag releases before coffee.

## [0.2.3] - 2017-06-27

- Fix missing import error.

## [0.2.2] - 2017-06-27

- Fix `console_script` `entry_point`.  #10 - @danielx

## [0.2.1] - 2017-06-26

- Fix bug with `vte` terminals.

## [0.2.0] - 2017-06-26

- Moved `wal` into a module and split the script into multiple files.
- Removed all usage of global variables.
- General cleanup.

## [0.1.6] - 2017-06-25

- Fix incorrect Python shebang #5.
- [wallpaper] Surpress `xfconf` output.

## [0.1.5] - 2017-06-23

- Cleanup
- Name change

## [0.1.4] - 2017-06-22

- Display a notification during generation.
- Remove macOS code.
    - The main `wal` functions don't work on macOS so why support it in minor areas?

## [0.1.3] - 2017-06-22

- I love pypi!

## [0.1.2] - 2017-06-22

- Remove all markdown conversion from `setup.py`.

## [0.1.1] - 2017-06-22

- Fix pypi long description.

## 0.1.0 - 2017-06-22



[Unreleased]: https://github.com/eylles/pywal16/compare/3.8.10...HEAD
[3.8.10]: https://github.com/eylles/pywal16/compare/3.8.9...3.8.10
[3.8.9]: https://github.com/eylles/pywal16/compare/3.8.8...3.8.9
[3.8.8]: https://github.com/eylles/pywal16/compare/3.8.7...3.8.8
[3.8.7]: https://github.com/eylles/pywal16/compare/3.8.6...3.8.7
[3.8.6]: https://github.com/eylles/pywal16/compare/3.8.5...3.8.6
[3.8.5]: https://github.com/eylles/pywal16/compare/3.8.4...3.8.5
[3.8.4]: https://github.com/eylles/pywal16/compare/3.8.3...3.8.4
[3.8.3]: https://github.com/eylles/pywal16/compare/3.8.2...3.8.3
[3.8.2]: https://github.com/eylles/pywal16/compare/3.8.1...3.8.2
[3.8.1]: https://github.com/eylles/pywal16/compare/3.8.0...3.8.1
[3.8.0]: https://github.com/eylles/pywal16/compare/3.7.2...3.8.0
[3.7.2]: https://github.com/eylles/pywal16/compare/3.7.1...3.7.2
[3.7.1]: https://github.com/eylles/pywal16/compare/3.7.0...3.7.1
[3.7.0]: https://github.com/eylles/pywal16/compare/3.6.0...3.7.0
[3.6.0]: https://github.com/eylles/pywal16/compare/3.5.4...3.6.0
[3.5.4]: https://github.com/eylles/pywal16/compare/3.5.3...3.5.4
[3.5.3]: https://github.com/eylles/pywal16/compare/3.5.2...3.5.3
[3.5.2]: https://github.com/eylles/pywal16/compare/3.5.1...3.5.2
[3.5.1]: https://github.com/eylles/pywal16/compare/3.5.0...3.5.1
[3.5.0]: https://github.com/eylles/pywal16/compare/3.4.0...3.5.0
[3.4.0]: https://github.com/eylles/pywal16/compare/3.3.0...3.4.0
[3.3.0]: https://github.com/dylanaraps/pywal/compare/3.2.1...3.3.0
[3.2.1]: https://github.com/dylanaraps/pywal/compare/3.2.0...3.2.1
[3.2.0]: https://github.com/dylanaraps/pywal/compare/3.1.0...3.2.0
[3.1.0]: https://github.com/dylanaraps/pywal/compare/3.0.1...3.1.0
[3.0.1]: https://github.com/dylanaraps/pywal/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/dylanaraps/pywal/compare/2.1.0...3.0.0
[2.1.0]: https://github.com/dylanaraps/pywal/compare/2.0.5...2.1.0
[2.0.5]: https://github.com/dylanaraps/pywal/compare/2.0.4...2.0.5
[2.0.4]: https://github.com/dylanaraps/pywal/compare/2.0.3...2.0.4
[2.0.3]: https://github.com/dylanaraps/pywal/compare/2.0.2...2.0.3
[2.0.2]: https://github.com/dylanaraps/pywal/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/dylanaraps/pywal/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/dylanaraps/pywal/compare/1.3.3...2.0.0
[1.3.3]: https://github.com/dylanaraps/pywal/compare/1.3.2...1.3.3
[1.3.2]: https://github.com/dylanaraps/pywal/compare/1.3.0...1.3.2
[1.3.0]: https://github.com/dylanaraps/pywal/compare/1.2.3...1.3.0
[1.2.3]: https://github.com/dylanaraps/pywal/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/dylanaraps/pywal/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/dylanaraps/pywal/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/dylanaraps/pywal/compare/1.1.2...1.2.0
[1.1.2]: https://github.com/dylanaraps/pywal/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/dylanaraps/pywal/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/dylanaraps/pywal/compare/1.0.4...1.1.0
[1.0.4]: https://github.com/dylanaraps/pywal/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/dylanaraps/pywal/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/dylanaraps/pywal/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/dylanaraps/pywal/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/dylanaraps/pywal/compare/0.7.5...1.0.0
[0.7.5]: https://github.com/dylanaraps/pywal/compare/0.7.4...0.7.5
[0.7.4]: https://github.com/dylanaraps/pywal/compare/0.7.3...0.7.4
[0.7.3]: https://github.com/dylanaraps/pywal/compare/0.7.2...0.7.3
[0.7.2]: https://github.com/dylanaraps/pywal/compare/0.7.0...0.7.2
[0.7.0]: https://github.com/dylanaraps/pywal/compare/0.6.9...0.7.0
[0.6.9]: https://github.com/dylanaraps/pywal/compare/0.6.8...0.6.9
[0.6.8]: https://github.com/dylanaraps/pywal/compare/0.6.7...0.6.8
[0.6.7]: https://github.com/dylanaraps/pywal/compare/0.6.6...0.6.7
[0.6.6]: https://github.com/dylanaraps/pywal/compare/0.6.4...0.6.6
[0.6.4]: https://github.com/dylanaraps/pywal/compare/0.6.3...0.6.4
[0.6.3]: https://github.com/dylanaraps/pywal/compare/0.6.2...0.6.3
[0.6.2]: https://github.com/dylanaraps/pywal/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/dylanaraps/pywal/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/dylanaraps/pywal/compare/0.5.13...0.6.0
[0.5.13]: https://github.com/dylanaraps/pywal/compare/0.5.12...0.5.13
[0.5.12]: https://github.com/dylanaraps/pywal/compare/0.5.11...0.5.12
[0.5.11]: https://github.com/dylanaraps/pywal/compare/0.5.10...0.5.11
[0.5.10]: https://github.com/dylanaraps/pywal/compare/0.5.9...0.5.10
[0.5.9]: https://github.com/dylanaraps/pywal/compare/0.5.8...0.5.9
[0.5.8]: https://github.com/dylanaraps/pywal/compare/0.5.7...0.5.8
[0.5.7]: https://github.com/dylanaraps/pywal/compare/0.5.6...0.5.7
[0.5.6]: https://github.com/dylanaraps/pywal/compare/0.5.5...0.5.6
[0.5.5]: https://github.com/dylanaraps/pywal/compare/0.5.1...0.5.5
[0.5.1]: https://github.com/dylanaraps/pywal/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/dylanaraps/pywal/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/dylanaraps/pywal/compare/0.3.10...0.4.0
[0.3.10]: https://github.com/dylanaraps/pywal/compare/0.3.8...0.3.10
[0.3.8]: https://github.com/dylanaraps/pywal/compare/0.3.7...0.3.8
[0.3.7]: https://github.com/dylanaraps/pywal/compare/0.3.6...0.3.7
[0.3.6]: https://github.com/dylanaraps/pywal/compare/0.3.5...0.3.6
[0.3.5]: https://github.com/dylanaraps/pywal/compare/0.3.4...0.3.5
[0.3.4]: https://github.com/dylanaraps/pywal/compare/0.3.3...0.3.4
[0.3.3]: https://github.com/dylanaraps/pywal/compare/0.3.2...0.3.3
[0.3.2]: https://github.com/dylanaraps/pywal/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/dylanaraps/pywal/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/dylanaraps/pywal/compare/0.2.6...0.3.0
[0.2.6]: https://github.com/dylanaraps/pywal/compare/0.2.5...0.2.6
[0.2.5]: https://github.com/dylanaraps/pywal/compare/0.2.4...0.2.5
[0.2.4]: https://github.com/dylanaraps/pywal/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/dylanaraps/pywal/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/dylanaraps/pywal/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/dylanaraps/pywal/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/dylanaraps/pywal/compare/0.1.6...0.2.0
[0.1.6]: https://github.com/dylanaraps/pywal/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/dylanaraps/pywal/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/dylanaraps/pywal/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/dylanaraps/pywal/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/dylanaraps/pywal/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/dylanaraps/pywal/compare/0.1.0...0.1.1
