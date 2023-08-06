import os
import subprocess
import sys
from shutil import which
from typing import Optional

from .file import split_fname, expand_relative

inkscape_binary: Optional[str] = None
"""
location of the inkscape binary
"""

inkscape_version = (0, 92)
"""
version of inkscape in `inkscape_binary`. the commandline api changed for (1,0)
"""


def convert_svg(svg: str, raster: str = ".png", dpi=300):
    """Convert an SVG file into another format supported by inkscape

    :param str svg: source vector file
    :param str raster: (optional) absolute file name OR file name relative to svg OR extension only
    :param int dpi: (optional) resolution of rasterized image
    :return: exit code of the Inkscape process
    """
    if not inkscape_binary or not os.path.isfile(inkscape_binary):
        raise ValueError("Inkscape binary does not exist or is not set: " + inkscape_binary)
    if not svg or not os.path.isfile(svg):
        raise ValueError("Input file not exist or is not set: " + inkscape_binary)
    spath, sname, sext = split_fname(svg)
    raster_pre, raster_ext = os.path.splitext(os.path.basename(raster))
    if not raster_ext:
        raster_pre, raster_ext = raster_ext, raster_pre
    if not raster_pre:
        raster = os.path.join(spath, sname + raster_ext)
    raster = expand_relative(raster, os.path.dirname(svg))
    cmdline = [inkscape_binary, "--without-gui"]
    if inkscape_version < (1, 0):
        _, raster_fmt = os.path.splitext(raster)
        raster_fmt = raster_fmt[1:]
        if not raster_fmt in ("png", "ps", "eps", "pdf", "wmf", "emf"):
            raise ValueError(("Raster format not supported by inkscape: " + raster_fmt))
        cmdline += ["--file=%s" % svg, "--export-dpi=%d" % dpi, "--export-%s=%s" % (raster_fmt, raster)]
    else:
        # TODO https://wiki.inkscape.org/wiki/index.php/Using_the_Command_Line
        raise NotImplementedError("This version of Inkscape is not yet supported.")
    return subprocess.call(cmdline)


def _locate_inkscape():
    loc = which("inkscape")
    if loc and os.path.isfile(loc):
        return loc
    if sys.platform == "win32":
        for programs in ["PROGRAMW6432", "PROGRAMFILES", "PROGRAMFILES(X86)"]:
            if programs in os.environ:
                loc = os.path.join(os.environ[programs], r"Inkscape\inkscape.exe")
                if loc and os.path.isfile(loc):
                    return loc
    return None


# noinspection PyRedeclaration
inkscape_binary = _locate_inkscape()
