import numpy as np

from signpy.sgn import Signal1
from signpy.sgn.defaults import HEAVISIDE
from signpy.transforms import Transform1
from signpy.transforms.fourier import Fourier1, InverseFourier1
from signpy.config import HILBERT_METHOD

class Hilbert(Transform1):
    def __init__(self, target: Signal1):
        super().__init__(target)
        self.methods = {
            "conv": self.calculate_conv,
            "fft": self.calculate_fft,
        }

    def _char_function(self, t):
            return 1 / (np.pi * t)

    def calculate(self, method=HILBERT_METHOD):
        return self.methods[method]()

    def calculate_conv(self):
        return self.signal.convolute(
            Signal1.from_function(
                self.signal.time,
                self._char_function
            )
        )

    def calculate_fft(self):
        output = self.signal.clone()
        self_fourier = Fourier1(self.signal)
        t_fourier = Fourier1(
            Signal1.from_function(self.signal.time, self._char_function)
        )

        return InverseFourier1(self_fourier * t_fourier)
