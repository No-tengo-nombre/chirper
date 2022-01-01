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

from .gui import mic_test

__all__ = ["sgn", "modulation", "transforms"]


def run():
    mic_test.main()
