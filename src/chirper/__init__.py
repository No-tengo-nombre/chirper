"""
=======
Chirper
=======

Chirper is a package that aims to provide different tools and
functionalities for analyzing and processing signals.

Subpackages
-----------
sgn
    Basic creation and manipulation of signals.
modulation
    Different methods for modulating and demodulating signals,
    particularly useful when using signals to transmit and receive
    information.
transforms
    Implementation of different integral transforms utilized in signal
    processing applications.
api
    An API for the GUI to request data in a nicely formatted way.
gui
    Subpackage that contains the code for the GUI, which allows for live
    signal visualization and manipulation.
"""

import os
from importlib.metadata import version

from .gui import main_gui


__all__ = ["sgn", "modulation", "transforms"]
__version__ = version("chirper-py")

BASE_DIRNAME = os.path.dirname(__file__)


def run():
    main_gui.main()
