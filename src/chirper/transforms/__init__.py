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

from chirper.transforms.cosine import c1, c2
from chirper.transforms.fourier import f1, f2
from chirper.transforms.hilbert import h1
from chirper.transforms.ifourier import if1, if2
from chirper.transforms.sine import s1, s2
from chirper.transforms.stft import stft1
