# from signpy.sgn import Signal1

import numpy as np

from signpy.config import CONVOLUTION_METHOD
from signpy.transforms.fourier import Fourier, InverseFourier


def convolute(s1_x, s1_y, method=CONVOLUTION_METHOD):
    """Calculates the convolution of two one-dimensional signals.

    There are different methods to calculate the convolution of two
    signals. The ones currently implemented are:
     - "fft": Uses the property that convolution in the time domain
        translates into multiplication in the frequency domain.
        That way, one can use the FFT to calculate the Fourier
        transforms of both signals (which is done really quickly),
        multiplies the spectra and then applies the inverse.

     - "direct" : Uses the formula of convolution to calculate it via
        brute-force. Very inneficient, as it is O(N*M).

    Parameters
    ----------
    s1_x : Signal1
        First one-dimensional signal to convolute.
    s1_y : Signal1
        Second one-dimensional signal to convolute.
    method : {"fft", "direct"}, optional
        Method used for the convolution, by default CONVOLUTION_METHOD.

    Returns
    -------
    Signal1
        Convoluted signal.
    """
    conv_methods = {
        "fft" : conv_fft,
        "direct" : conv_direct,
    }
    return conv_methods[method](s1_x, s1_y)

def conv_fft(s1_x, s1_y):
    """Convolutes using the FFT."""
    x_fourier = Fourier(s1_x)
    y_fourier = Fourier(s1_y)
    return InverseFourier(x_fourier * y_fourier)

def conv_direct(s1_x, s1_y):
    """Convolutes via brute-force."""
    copy = s1_x.clone()
    return copy.apply_function(_conv_helper, s1_y)

def _conv_helper(self, a, signal1):
    sum = 0
    for k in signal1.time:
        sum += a * signal1[k]
    return sum

def cross_correlation(s1_x, s1_y):
    copy = s1_x.clone()
