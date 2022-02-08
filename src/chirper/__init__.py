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

import unittest
import os
from importlib.metadata import version

from chirper.gui import main_gui
from chirper.test import manual_tests
from chirper.test import unit_tests


__all__ = ["sgn", "modulation", "transforms"]
__version__ = version("chirper-py")

BASE_DIRNAME = os.path.dirname(__file__)


def run_main_application(filename=None):
    main_gui.main()


def run_unit_tests():
    suite = unittest.TestLoader().loadTestsFromModule(unit_tests)
    unittest.TextTestRunner().run(suite)


def run_manual_tests(tests, show_results):
    manual_tests.run(tests, show_results)
