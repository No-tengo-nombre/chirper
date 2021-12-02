from signpy.sgn import Signal1
from signpy.transforms import Transform
from signpy.config import FOURIER_METHOD

import numpy as np
from tqdm import tqdm


class Fourier(Transform):
    """Fourier transform"""
    def __init__(self, target):
        super().__init__(target)
        self.methods = {
            "dft": self.calculate_dft,
            "fft": self.calculate_fft,
        }

    def calculate(self, method=FOURIER_METHOD):
        return self.methods[method]()

    def calculate_shift(self, method=FOURIER_METHOD):
        output = self.methods[method]()
        signal_len = len(output)

        shifted_values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
        freq_axis = output.time - output.time_span() / 2
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
        self.values = new_values

        shifted_values = np.array([*self.values[signal_len // 2:], *self.values[:signal_len // 2]])
        shifted_time = np.array([*self.time[signal_len // 2:], *self.time[:signal_len // 2]])

        return Signal1(self.time, self.values)#, Signal(shifted_time, shifted_values)

    # def calculate_fft(self):
    #     pass

    def calculate_fft(self):
        self.values = np.fft.fft(self.signal.values)
        return Signal1(self.time, self.values)


class InverseFourier(Transform):
    """Inverse Fourier transform"""
    def __init__(self, target):
        super().__init__(target)
        self.methods = {
            "dft": self.calculate_dft,
            "fft": self.calculate_fft,
        }
    
    def calculate(self, method=FOURIER_METHOD):
        return self.methods[method]()

    def calculate_shift(self, method=FOURIER_METHOD):
        signal_len = len(self.signal)
        self.signal.time = self.signal.time + self.signal.time_span() / 2
        self.signal.values = np.array([*self.signal.values[signal_len // 2:], *self.signal.values[:signal_len // 2]])
        # return Signal(*self.signal.unpack())
        return self.methods[method]()

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
        self.values = new_values
        return Signal1(self.time, self.values) * signal_len

    def calculate_fft(self):
        self.values = np.fft.ifft(self.signal.values)
        return Signal1(self.time, self.values)
