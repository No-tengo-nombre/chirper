import numpy as np

from signpy.config import CONVOLUTION_METHOD, CROSS_CORRELATION_METHOD
from signpy.exceptions import DimensionError
# from signpy.transforms.fourier import Fourier1, InverseFourier1
# from signpy.sgn import Signal1


def convolution(s1_x, s1_y, method=CONVOLUTION_METHOD):
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
    from signpy.transforms.fourier import Fourier1, InverseFourier1
    x_fourier = Fourier1(s1_x)
    y_fourier = Fourier1(s1_y)
    return InverseFourier1(x_fourier * y_fourier)

def conv_direct(s1_x, s1_y):
    """Convolutes via brute-force."""
    x_copy = s1_x.clone()
    y_copy = s1_y.clone()
    if not np.array_equal(x_copy.axis, y_copy.axis):
        raise DimensionError("Dimensions of signals do not match.")
    # return copy.apply_function(_conv_helper, s1_y)
    vals = []
    for n, _ in enumerate(x_copy.values):
        sum = 0
        for m, _ in enumerate(y_copy.values):
            sum += x_copy.values[m] * y_copy.values[n - m]
        vals.append(sum)
    output = s1_x.clone()
    output.values = np.array(vals)
    return output

def cross_correlation(s1_x, s1_y, method=CROSS_CORRELATION_METHOD):
    """Calculates the cross correlation of two signals.

    Parameters
    ----------
    s1_x : Signal1
        First signal.
    s1_y : Signal1
        Second signal
    method : {"direct"}, optional
        Desired method to calculate the cross correlation, by default
        CROSS_CORRELATION_METHOD.

    Returns
    -------
    Signal1
        Cross correlated signal
    """
    cc_methods = {
        "fft" : cc_fft,
        "direct" : cc_direct,
    }
    return cc_methods[method](s1_x, s1_y)

def cc_direct(s1_x, s1_y):
    x_copy = s1_x.clone()
    y_copy = s1_y.clone()
    if not np.array_equal(x_copy.axis, y_copy.axis):
        raise DimensionError("Dimensions of signals do not match.")
    # return copy.apply_function(_conv_helper, s1_y)
    vals = []
    for n, _ in enumerate(x_copy.values):
        sum = 0
        for m, _ in enumerate(y_copy.values):
            sum += np.conjugate(x_copy.values[m]) * y_copy.values[(m + n) % len(x_copy)]
        vals.append(sum)
    output = s1_x.clone()
    output.values = np.array(vals)
    return output

def cc_fft(s1_x, s1_y):
    from signpy.transforms.fourier import Fourier1, InverseFourier1
    x_copy = s1_x.clone()
    y_copy = s1_y.clone()
    x_fourier = Fourier1(x_copy)
    y_fourier = Fourier1(y_copy)
    return InverseFourier1(x_fourier.conjugate() * y_fourier)