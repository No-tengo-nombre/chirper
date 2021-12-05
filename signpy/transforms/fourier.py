from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from signpy.sgn import Signal1
import numpy as np
from tqdm import tqdm

from signpy.config import FOURIER_METHOD
from . import Transform1


class Fourier1(Transform1):
    """One dimensional Fourier transform."""
    def __init__(self, target: Signal1, method=FOURIER_METHOD):
        self.methods = {
            "dft": self.calculate_dft,
            "fft": self.calculate_fft,
        }
        super().__init__(target)
        self.axis, self.values = self.calculate(method).unpack()

    def calculate(self, method=FOURIER_METHOD):
        return self.methods[method]()

    def freq_shift(self):
        output = self.clone()
        signal_len = len(output)
        output.axis = output.axis - output.span() / 2
        output.values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
        return output

    def calculate_dft(self):
        """Calculates the Discrete Fourier Transform (DFT) of a signal :math:`\\mathcal{F}\\{x[n]\\} = X[k]`, such that

        .. math::
            X[k] = \\sum_{n=0}^{N-1}x[n]e^{-j2\\pi nk/N}

        Returns
        -------
        Signal representing the Fourier Transform.
        """
        output = self.signal.clone()
        signal_len = len(output)
        new_values = np.zeros(signal_len, dtype=complex)
        for k in tqdm(range(signal_len), "Calculating DFT"):
            temp = 0 + 0j
            for n in range(signal_len):
                temp += output.values[n] * np.exp(-1j * (2 * n * k * np.pi / signal_len))
            new_values[k] = temp
        output.values = new_values

        return output

    def calculate_fft(self):
        output = self.signal.clone()
        output.values = np.fft.fft(output.values)
        return output


class InverseFourier1(Transform1):
    """One dimensional inverse Fourier transform."""
    def __init__(self, target: Signal1, method=FOURIER_METHOD):
        self.methods = {
            "dft": self.calculate_dft,
            "fft": self.calculate_fft,
        }
        super().__init__(target)
        self.axis, self.values = self.calculate(method).unpack()
    
    def calculate(self, method=FOURIER_METHOD):
        return self.methods[method]()

    def freq_shift(self):
        output = self.signal.clone()
        signal_len = len(output)
        output.axis = output.axis + output.span() / 2
        output.values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
        return output

    def calculate_dft(self):
        """Calculates the inverse Fourier Transform :math:`\\mathcal{F}^{-1}\\{X[k]\\} = x[n]` such that

         .. math::
            x[n] = \\sum_{k=0}^{N-1}X[k]e^{j2\\pi nk/N}

        Returns
        -------
        Signal representing the Inverse Fourier Transform.
        """
        output = self.signal.clone()
        signal_len = len(output)
        new_values = np.zeros(signal_len, dtype=complex)
        for n in tqdm(range(signal_len), "Calculating Inverse DFT"):
            temp = 0 + 0j
            for k in range(signal_len):
                temp += output.values[k] * np.exp(1j * (2 * n * k * np.pi / signal_len))
            new_values[n] = temp / signal_len
        output.values = new_values
        return output * signal_len

    def calculate_fft(self):
        output = self.signal.clone()
        output.values = np.fft.ifft(output.values)
        return output
