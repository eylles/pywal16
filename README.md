## This project is a 16 colors fork of [pywal](https://github.com/dylanaraps/pywal)
<h3 align="center"><img src="https://i.imgur.com/5WgMACe.gif" width="200px"></h3>
<p align="center">Generate and change color-schemes on the fly.</p>

<p align="center">
<a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
<a href="https://pypi.python.org/pypi/pywal16/"><img src="https://img.shields.io/pypi/v/pywal16.svg"></a>
<a href="https://pypi.python.org/pypi/pywal/"><img src="https://img.shields.io/pypi/v/pywal.svg"></a>
<a href="https://liberapay.com/eylles/donate"><img alt="Donate using Liberapay" src="https://img.shields.io/liberapay/receives/eylles.svg?logo=liberapay"></a>
<a href="https://liberapay.com/eylles/donate"><img alt="Donate using Liberapay" src="https://img.shields.io/liberapay/patrons/eylles.svg?logo=liberapay"></a>
</p>

<img src="https://i.imgur.com/V1FuvJP.png" alt="img" align="right" width="400px">

Pywal is a tool that generates a color palette from the dominant colors in an image. It then applies the colors system-wide and on-the-fly in all of your favourite programs.  

There are currently 8 supported color generation backends, each providing a different palette of colors from each image. You're bound to find an appealing color-scheme.

Pywal also supports predefined themes and has over 250 themes built-in. You can also create your own theme files to share with others.

The goal of Pywal was to be as out of the way as possible. It doesn't modify any of your existing configuration files. Instead it works around them and provides tools to integrate your system as you see fit.

Terminal emulators and TTYs have their color-schemes updated in real-time with no delay. With minimal configuration this functionality can be extended to almost anything running on your system.

### More: \[[Installation](https://github.com/eylles/pywal16/wiki/Installation)] \[[Getting Started](https://github.com/eylles/pywal16/wiki/Getting-Started)] \[[Customization](https://github.com/eylles/pywal16/wiki/Customization)] \[[Wiki](https://github.com/eylles/pywal16/wiki)] \[[Screenshots](https://www.reddit.com/r/unixporn/search?q=wal&restrict_sr=on&sort=relevance&t=all)] \[[Extras](https://github.com/eylles/pywal-extra)]

### NOTE: default name change

The default distribution of this project at the Python Package Index (PyPI) is moving from pywal16 to pywal, for the rest of 2026 and during 2027 both distribution namespaces will receive the same updates but the current plan
is starting 2028 to sundown the `pywal16` distribution in pypi, this is done in order to prioritize the vastly more popular `pywal` distribution and to prevent long term hogging of multiple names on pypi for the same package
for that reason the default name of the package in setup.py is changing from "pywal16" to "pywal" this should not affect those that package pywal16 for the various distributions beyond having a .whl or a tar.gz with a different
name when running `python -m build` which ought to be a tiny change to adapt to.

[![Packaging status](https://repology.org/badge/vertical-allrepos/pywal16.svg)](https://repology.org/project/pywal16/versions)
[![Packaging status](https://repology.org/badge/vertical-allrepos/pywal.svg)](https://repology.org/project/pywal/versions)

