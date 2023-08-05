import os
from matpopmod.model import MPM
from matpopmod.compadre import MPMCollection
from matpopmod.compadre import InvalidMPM
from matpopmod.utils import set_rng_seed
import matpopmod.examples as examples
import matpopmod.collapsing as collapsing
import matpopmod.mathtools as mathtools
import matpopmod.compadre as compadre
import matpopmod.plot as plot

try:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "VERSION"), encoding = "utf-8") as fh:
        __version__ = fh.read()
except Exception:
    __version__ = None
