from signpy.transforms import Transform
from signpy.sgn.signal import HEAVISIDE, Signal
from signpy.transforms.fourier import Fourier, InverseFourier
from signpy.config import HILBERT_METHOD

import numpy as np

from signpy.transforms.fourier import Fourier

class Hilbert(Transform):
    def __init__(self, target):
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
            Signal.from_function(
                self.signal.time,
                self._char_function
            )
        )

    def calculate_fft(self):
        self_fourier = Fourier(self.signal).calculate()
        t_fourier = Fourier(
            Signal.from_function(self.signal.time, self._char_function)
        ).calculate()

        return InverseFourier(self_fourier * t_fourier).calculate()
