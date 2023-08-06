import itertools
from typing import Optional, Union, List, Iterator

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator

# re-import full modules for easier access
from . import const
from . import file
from . import style

# apply default rcParams right after loading
style.set_style()

output_mode = "auto"
"""
"file"        : only produce files
"interactive" : show all plots, including those with filename, produce no files
"both"        : produce files if requested, show all
"auto"        : save if file name given, show if not
"""

output_location = file.get_invoker_dir()
"""
base for relative file paths on output
"""

sizes = {
    "regular": (150 * const.GOLDEN_RATIO, 150),
    "wide": (300, 150)
}
"""
some template sizes for use with new_*, given in millimeters
"""


def default_dpi(save=False):
    if save and mpl.rcParams["savefig.dpi"] != "figure":
        return mpl.rcParams["savefig.dpi"]
    return mpl.rcParams["figure.dpi"]


def new_mm(*args, figsize, **kwargs):
    """Wrapper for plt.subplots, using figsize in millimeters

    :rtype: figure, axes
    """
    return plt.subplots(*args, figsize=(figsize[0] / 25.4, figsize[1] / 25.4), **kwargs)


def new_regular(*args, **kwargs):
    """Create a figure in a commonly used format

    :rtype: figure, axes
    """
    return new_mm(*args, figsize=sizes["regular"], **kwargs)


def new_wide(*args, **kwargs):
    """Create a wide figure, useful for timeseries

    :rtype: figure, axes
    """
    return new_mm(*args, figsize=sizes["wide"], **kwargs)


def set_ticks(axs: Axes, *, major: Optional[str] = None, minor: Optional[str] = None, maxn: Optional[int] = None,
              multiple: Optional[float] = None):
    """Configure axis ticks

    :param Axes axs: Axes object to manipulate
    :param str major: (optional) string containing xy
    :param str minor: (optional) string containing xy.
        Only modifies axis indicated by the parameter.
        If none of `major` and `minor` are given, assume major="",minor="xy"

    The first parameter present is executed, if none match, an AutoLocator is applied:

    :param int maxn: setup a MaxNLocator
    :param float multiple: setup a MultipleLocator
    """

    if major is None and minor is None:
        minor = "xy"
    if major is None:
        major = ""
    if minor is None:
        minor = ""

    def do_setting(ax, kind):
        setfn = getattr(ax, f"set_{kind}_locator")
        if maxn is not None:
            setfn(plt.MaxNLocator(maxn))
        elif multiple is not None:
            setfn(plt.MultipleLocator(multiple))
        else:
            setfn(plt.AutoLocator() if kind == "major" else AutoMinorLocator())

    "x" in major and do_setting(axs.xaxis, "major")
    "x" in minor and do_setting(axs.xaxis, "minor")
    "y" in major and do_setting(axs.yaxis, "major")
    "y" in minor and do_setting(axs.yaxis, "minor")


def set_grid(axs: Axes):
    """Apply default grid settings to Axes

    :param Axes axs: Axes object to manipulate
    """
    axs.grid(which="major", linestyle="-")
    axs.grid(which="minor", linestyle=":", linewidth=mpl.rcParams["grid.linewidth"] * 0.5,
             alpha=mpl.rcParams["grid.alpha"] * 0.8)


def get_object_facecolor(obj):
    if isinstance(obj, list):
        return get_object_facecolor(obj[-1])
    if isinstance(obj, mpl.lines.Line2D):
        return obj.get_color()
    if isinstance(obj, mpl.collections.Collection):
        return obj.get_facecolor()[0]
    return None


def finalize(fig: Figure, filename: Optional[str] = None):
    """Show and/or save the figure, and close(dispose) it afterwards.

    :param Figure fig: Figure object to manipulate
    :param str filename: (optional) file name to save to
    :return: absolute file name, or None if none was produced
    :rtype: str
    """
    if output_mode == "both":
        raise NotImplementedError(f"Unsupported due to errors with tight_layout")
    do_save = filename and (output_mode == "auto" or output_mode == "file")
    do_show = output_mode == "interactive" or (output_mode == "auto" and not filename)
    if do_show:
        fig.show()
    if do_save:
        filename = file.expand_relative(filename, output_location)
        fig.savefig(filename)
    if do_show or do_save:
        plt.close(fig)
    return filename


def get_cmap_cycle(cmap: Union[Colormap, str], k: Optional[int] = None) -> Union[Iterator, List]:
    """Return a cycler for colormaps.

    If *k=None*, return the iterator, otherwise return a list of *k* elements.

    :param (Colormap, str) cmap: colormap instance or cmap identifier
    :param int k: (optional) number of items to return
    :return:
    """
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    cycler = itertools.cycle(cmap.colors)
    if k is not None:
        return list(itertools.islice(cycler, k))
    return cycler
