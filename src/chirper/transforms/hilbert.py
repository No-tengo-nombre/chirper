import numpy as np
from scipy import signal

from chirper.sgn import Signal1
from chirper.config import H1_METHOD
from chirper.transforms import f1, if1


def _char_function(t) -> float:
    return 1 / (np.pi * t)


def h1(signal1: Signal1, method=H1_METHOD) -> Signal1:
    return H1_METHODS[method](signal1)


def calculate_conv(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal2 = Signal1.from_function(output.axis, _char_function)
    return output.convolute(signal2)


def calculate_fft(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal2 = Signal1.from_function(output.axis, _char_function)
    self_fourier = f1(output)
    t_fourier = f1(signal2)
    return if1(self_fourier * t_fourier)


def calculate_prod(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    self_fourier = f1(output)
    # self_fourier = Fourier1(output).freq_shift()
    axis_len = len(output.axis)
    if axis_len % 2 == 0:
        h_values = 2 * np.ones(axis_len // 2 - 1)
    else:
        h_values = 2 * np.ones(axis_len // 2)
    h_values[0] = 1
    h_values[-1] = 1
    h_values = np.append(h_values, np.zeros(axis_len // 2 + 1))
    assert len(h_values) == axis_len
    # output.values = h_values
    # return InverseFourier1(output * self_fourier)
    output.values = output.values * self_fourier.values
    return if1(output)


def calculate_scipy(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    output.values = signal.hilbert(output.values)
    return output.imag_part()


H1_METHODS = {
    "conv": calculate_conv,
    "fft": calculate_fft,
    "prod": calculate_prod,
    "scipy": calculate_scipy,
}
