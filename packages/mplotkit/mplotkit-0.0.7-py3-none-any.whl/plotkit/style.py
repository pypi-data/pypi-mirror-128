from typing import Optional

import matplotlib as mpl
import matplotlib.pyplot as plt

# https://matplotlib.org/tutorials/introductory/customizing.html#customizing-with-matplotlibrc-files
# Units in matplotlib:
#   figure size       : inches relative to figure.dpi
#   font size         : 1pt=1/72"
#   linewidth         : 1pt=1/72"
#   savefig           : oversampled by savefig.dpi/figure.dpi
#
# In vanilla matplotlib (default 100dpi), a 4" figure is 400 pixels, and 72pt Text is 100px tall. The intention is
# to get good representation on a screen, but while most displays are close to 100dpi, is is usually never exact.
# Add desktop DPI scaling to the mix and it gets rather tedious for complex manual layouts. Fixing everything to
# 72dpi and letting savefig deal with scaling is much more intuitive.

styles = {
    "default": {
        "pk_use": "default",
        "figure.dpi": 72,
        "savefig.dpi": 144,
        "figure.autolayout": True,
        # "figure.constrained_layout.use": True,
        "lines.linewidth": 1.5,
        "lines.linestyle": "-",
        "grid.color": "silver",
        "grid.linewidth": 0.75,
        # svg.fonttype : "path"         # How to handle SVG fonts:
        #    "none": Assume fonts are installed on the machine where the SVG will be viewed.
        #    "path": Embed characters as paths -- supported by most SVG renderers
        #    "svgfont": Embed characters as SVG fonts -- supported only by Chrome,
        #               Opera and Safari
        "svg.fonttype": "none"
    },
    "print": {
        "pk_pre": "default",
        "savefig.dpi": 600,
    },
    "poster": {
        "pk_pre": "print",
        "font.size": 18
    }
}


def apply_styledef(pk_use=None, pk_pre=None, **rc):
    if pk_use:
        plt.style.use(pk_use)
    if pk_pre:
        if isinstance(pk_pre, list):
            for p in pk_pre:
                apply_styledef(**styles[p])
        else:
            apply_styledef(**styles[pk_pre])
    mpl.rcParams.update(rc)


def set_style(target: Optional[str] = None):
    """Apply a style target

    :param str target: (optional) style target name, such as "print", "poster", ...
    """
    if not target:
        target = "default"
    apply_styledef(**styles[target])
