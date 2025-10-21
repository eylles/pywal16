"""wal - setup.py"""

import sys
import setuptools

try:
    import pywal
except ImportError:
    print("error: pywal requires Python 3.5 or greater.")
    sys.exit(1)

is_win = sys.platform.startswith("win")

LONG_DESC = open("README.md").read()
VERSION = pywal.__version__
DOWNLOAD = "https://github.com/eylles/pywal16/archive/%s.tar.gz" % VERSION

install_requires = []
if is_win:
    install_requires += ["colorama"]

setuptools.setup(
    name="pywal16",
    version=VERSION,
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="Generate and change color-schemes on the fly",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="wal colorscheme terminal-emulators changing-colorschemes",
    license="MIT",
    url="https://github.com/eylles/pywal16",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.11",
    ],
    data_files=[('man/man1', ['data/man/man1/wal.1'])],
    packages=["pywal"],
    entry_points={"console_scripts": ["wal=pywal.__main__:main"]},
    python_requires=">=3.11",
    install_requires=install_requires,
    extras_require={
        "colorthief": [
            "colorthief",
        ],  # known to work with 0.2.1
        "colorz": [
            "colorz",
        ],  # NOTE heavy, scipy dependency
        "fast-colorthief": [
            "fast-colorthief",
        ],
        "haishoku": [
            "haishoku",
        ],
        "modern_colorthief": [
            "modern_colorthief",
        ],
        "all": [
            "colorthief",
            "colorz",
            "fast-colorthief",
            "haishoku",
            "modern_colorthief",
        ],  # convience, all of the above
    },
    include_package_data=True,
    zip_safe=False,
)
