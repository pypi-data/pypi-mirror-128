"""
Shorthand for importing pyplot on headless systems, to avoid auto-selecting a backend that might want
to access an X server or similar.
"""

import matplotlib

matplotlib.use("Agg")
from matplotlib.pyplot import *
