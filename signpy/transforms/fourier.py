from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from tqdm import tqdm

from signpy.config import F1_METHOD
if TYPE_CHECKING:
    from signpy.sgn import Signal1

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################

def f1(signal1: Signal1, method=F1_METHOD, shift=True) -> Signal1:
    """Calculates the one dimensional Fourier transform of a given
    signal.

    In order to perform the calculation, a specific algorithm can be
    given as a parameter.
    
    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to calculate the Fourier transform.
    method : {"dft", "fft"}, optional
        Method used to calculate the transform, by default F1_METHOD
    shift : bool
        Whether to shift the frequencies or not after applying the
        transform, by default True.

    Returns
    -------
    Signal1
        Signal representing the Fourier Transform.
    """
    output = F1_METHODS[method](signal1)
    if shift:
        output = freq_shift(output)
    return output

def calculate_dft1(signal1: Signal1) -> Signal1:
    """Calculates the Discrete Fourier Transform (DFT) of a signal :math:`\\mathcal{F}\\{x[n]\\} = X[k]`, such that

    .. math::
        X[k] = \\sum_{n=0}^{N-1}x[n]e^{-j2\\pi nk/N}

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to calculate the Fourier transform.

    Returns
    -------
    Signal1
        Signal representing the Fourier Transform.
    """
    output = signal1.clone()
    signal_len = len(output)
    new_values = np.zeros(signal_len, dtype=complex)
    for k in tqdm(range(signal_len), "Calculating DFT"):
        temp = 0 + 0j
        for n in range(signal_len):
            temp += output.values[n] * np.exp(-1j * (2 * n * k * np.pi / signal_len))
        new_values[k] = temp
    output.values = new_values
    return output

def calculate_fft1(signal1: Signal1) -> Signal1:
    """Calculates the FFT of a given signal.

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to calculate the Fourier transform.

    Returns
    -------
    Signal1
        Signal representing the Fourier Transform.
    """
    output = signal1.clone()
    output.values = np.fft.fft(output.values)
    return output


def freq_shift(signal1: Signal1) -> Signal1:
    """Shift the frequencies of the signal.

    Parameters
    ----------
    signal1 : Signal1
        Signal to shift.

    Returns
    -------
    Signal1
        Shifted signal
    """
    output = signal1.clone()
    signal_len = len(output)
    output.axis = output.axis - output.span() / 2
    output.values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
    return output

F1_METHODS = {
    "dft": calculate_dft1,
    "fft": calculate_fft1,
}

# class Fourier1(Transform1):
#     """One dimensional Fourier transform."""
#     def __init__(self, target: Signal1, method=F1_METHOD):
#         self.methods = {
#             "dft": self.calculate_dft,
#             "fft": self.calculate_fft,
#         }
#         super().__init__(target)
#         self.samp_freq = self.signal.sampling_freq()
#         self.axis, self.values = self.calculate(method).unpack()

#     def sampling_freq(self) -> float:
#         return self.samp_freq

#     def calculate(self, method=F1_METHOD) -> Signal1:
#         output = self.methods[method]()
#         # output.axis *= self.samp_freq / output.span()
#         return output

#     def freq_shift(self) -> Signal1:
#         output = self.clone()
#         signal_len = len(output)
#         output.axis = output.axis - output.span() / 2
#         output.values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
#         return output

#     def calculate_dft(self) -> Signal1:
#         """Calculates the Discrete Fourier Transform (DFT) of a signal :math:`\\mathcal{F}\\{x[n]\\} = X[k]`, such that

#         .. math::
#             X[k] = \\sum_{n=0}^{N-1}x[n]e^{-j2\\pi nk/N}

#         Returns
#         -------
#         Signal representing the Fourier Transform.
#         """
#         output = self.signal.clone()
#         signal_len = len(output)
#         new_values = np.zeros(signal_len, dtype=complex)
#         for k in tqdm(range(signal_len), "Calculating DFT"):
#             temp = 0 + 0j
#             for n in range(signal_len):
#                 temp += output.values[n] * np.exp(-1j * (2 * n * k * np.pi / signal_len))
#             new_values[k] = temp
#         output.values = new_values

#         return output

#     def calculate_fft(self) -> Signal1:
#         output = self.signal.clone()
#         output.values = np.fft.fft(output.values)
#         return output


# class InverseFourier1(Transform1):
#     """One dimensional inverse Fourier transform."""
#     def __init__(self, target: Signal1, method=F1_METHOD):
#         self.methods = {
#             "dft": self.calculate_dft,
#             "fft": self.calculate_fft,
#         }
#         super().__init__(target)
#         self.samp_freq = self.signal.sampling_freq()
#         self.axis, self.values = self.calculate(method).unpack()

#     def sampling_freq(self) -> float:
#         return self.samp_freq
    
#     def calculate(self, method=F1_METHOD) -> Signal1:
#         output = self.methods[method]()
#         # output.axis /= self.samp_freq / output.span()
#         return output

#     def freq_shift(self) -> Signal1:
#         output = self.signal.clone()
#         signal_len = len(output)
#         output.axis = output.axis + output.span() / 2
#         output.values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
#         return output

#     def calculate_dft(self) -> Signal1:
#         """Calculates the inverse Fourier Transform :math:`\\mathcal{F}^{-1}\\{X[k]\\} = x[n]` such that

#          .. math::
#             x[n] = \\sum_{k=0}^{N-1}X[k]e^{j2\\pi nk/N}

#         Returns
#         -------
#         Signal representing the Inverse Fourier Transform.
#         """
#         output = self.signal.clone()
#         signal_len = len(output)
#         new_values = np.zeros(signal_len, dtype=complex)
#         for n in tqdm(range(signal_len), "Calculating Inverse DFT"):
#             temp = 0 + 0j
#             for k in range(signal_len):
#                 temp += output.values[k] * np.exp(1j * (2 * n * k * np.pi / signal_len))
#             new_values[n] = temp / signal_len
#         output.values = new_values
#         return output * signal_len

#     def calculate_fft(self) -> Signal1:
#         output = self.signal.clone()
#         output.values = np.fft.ifft(output.values)
#         return output
