"""
===================
Integral transforms
===================

This subpackage gives access to different integral transforms used for
signal processing purposes. The ones currently available are:
- Fourier
- Inverse Fourier
- Hilbert
- Cosine
- Sine
- Short-time Fourier
"""

from .cosine import c1, c2
from .fourier import f1, f2
from .hilbert import h1
from .ifourier import if1, if2
from .sine import s1, s2
from .stft import stft1
