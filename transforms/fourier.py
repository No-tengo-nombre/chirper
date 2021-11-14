import sgn.signal
from transforms import Transform
from config import FOURIER_METHOD

import numpy as np
import tqdm


class Fourier(Transform):
    """Fourier transform"""
    def calculate(self):
        return self._calculate(FOURIER_METHOD)

    def _calculate(self, method):
        if method == "dft":
            return self._calculate_dft()

    def _calculate_dft(self):
        """Calculates the Discrete Fourier Transform (DFT) of a signal :math:`\\mathcal{F}\\{x[n]\\} = X[k]`, such that

        .. math::
            X[k] = \\sum_{n=0}^{N-1}x[n]e^{-j2\\pi nk/N}

        Returns
        -------
        Signal representing the Fourier Transform.
        """
        signal_len = len(self.signal)
        new_values = np.zeros(signal_len, dtype=complex)
        for k in tqdm.tqdm(range(signal_len), "Calculating DFT..."):
            temp = 0 + 0j
            for n in range(signal_len):
                temp += self.signal.values[n] * np.exp(-1j * (2 * n * k * np.pi / signal_len))
            new_values[k] = temp
            self.values = new_values
        return sgn.signal.Signal(self.time, self.values)


class InverseFourier(Transform):
    """Inverse Fourier transform"""
    def calculate(self):
        return self._calculate(FOURIER_METHOD)

    def _calculate(self, method):
        if method == "dft":
            return self._calculate_dft()

    def _calculate_dft(self):
        """Calculates the inverse Fourier Transform :math:`\\mathcal{F}^{-1}\\{X[k]\\} = x[n]` such that

         .. math::
            x[n] = \\sum_{k=0}^{N-1}X[k]e^{j2\\pi nk/N}

        Returns
        -------
        Signal representing the Inverse Fourier Transform.
        """
        signal_len = len(self.signal)
        new_values = np.zeros(signal_len, dtype=complex)
        for n in tqdm.tqdm(range(signal_len), "Calculating Inverse DFT..."):
            temp = 0 + 0j
            for k in range(signal_len):
                temp += self.signal.values[k] * np.exp(1j * (2 * n * k * np.pi / signal_len))
            new_values[n] = temp / signal_len
            self.values = new_values
        return sgn.signal.Signal(self.time, self.values) * signal_len
