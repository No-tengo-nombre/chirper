"""
======
Chirper
======

Chirper is a package that aims to provide different tools and functionalities for analyzing and processing
signals.

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
"""

import os
from importlib.metadata import version

from .gui import main_pyqt5


__all__ = ["sgn", "modulation", "transforms"]
__version__ = version("chirper-py")

BASE_DIRNAME = os.path.dirname(__file__)


def run():
    main_pyqt5.main()
