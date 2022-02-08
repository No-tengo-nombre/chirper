from scipy import signal

from chirper.sgn import Signal1
from chirper.config import H1_METHOD


def h1(signal1: Signal1, method=H1_METHOD) -> Signal1:
    return H1_METHODS[method](signal1)


def calculate_scipy(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    output.values = signal.hilbert(output.values)
    return output.imag_part()


H1_METHODS = {
    "scipy": calculate_scipy,
}
