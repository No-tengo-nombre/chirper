from signpy.sgn import Signal1
from signpy.transforms import Transform1
from signpy.config import FOURIER_METHOD

import numpy as np
from tqdm import tqdm


class Fourier(Transform1):
    """Fourier transform"""
    def __init__(self, target : Signal1, method=FOURIER_METHOD):
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

        shifted_values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
        freq_axis = output.axis - output.span() / 2
        return Signal1(freq_axis, shifted_values)

    def calculate_dft(self):
        """Calculates the Discrete Fourier Transform (DFT) of a signal :math:`\\mathcal{F}\\{x[n]\\} = X[k]`, such that

        .. math::
            X[k] = \\sum_{n=0}^{N-1}x[n]e^{-j2\\pi nk/N}

        Returns
        -------
        Signal representing the Fourier Transform.
        """
        signal_len = len(self.signal)
        new_values = np.zeros(signal_len, dtype=complex)
        for k in tqdm(range(signal_len), "Calculating DFT"):
            temp = 0 + 0j
            for n in range(signal_len):
                temp += self.signal.values[n] * np.exp(-1j * (2 * n * k * np.pi / signal_len))
            new_values[k] = temp

        return Signal1(self.signal.axis, new_values)

    def calculate_fft(self):
        values = np.fft.fft(self.signal.values)
        return Signal1(self.signal.axis, values)


class InverseFourier(Transform1):
    """Inverse Fourier transform"""
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
        signal_len = len(self.signal)
        new_time = self.signal.time + self.signal.time_span() / 2
        new_values = np.array([*self.signal.values[signal_len // 2:], *self.signal.values[:signal_len // 2]])
        return Signal1(new_time, new_values)
        # return self.methods[method]()

    def calculate_dft(self):
        """Calculates the inverse Fourier Transform :math:`\\mathcal{F}^{-1}\\{X[k]\\} = x[n]` such that

         .. math::
            x[n] = \\sum_{k=0}^{N-1}X[k]e^{j2\\pi nk/N}

        Returns
        -------
        Signal representing the Inverse Fourier Transform.
        """
        signal_len = len(self.signal)
        new_values = np.zeros(signal_len, dtype=complex)
        for n in tqdm(range(signal_len), "Calculating Inverse DFT"):
            temp = 0 + 0j
            for k in range(signal_len):
                temp += self.signal.values[k] * np.exp(1j * (2 * n * k * np.pi / signal_len))
            new_values[n] = temp / signal_len
        # self.values = new_values
        return Signal1(self.signal.axis, new_values) * signal_len

    def calculate_fft(self):
        values = np.fft.ifft(self.signal.values)
        return Signal1(self.signal.axis, values)
