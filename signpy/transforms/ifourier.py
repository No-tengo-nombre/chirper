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

def if1(signal1: Signal1, method=F1_METHOD, shift=True) -> Signal1:
    """Calculates the one dimensional Inverse Fourier transform of a
    given signal.

    In order to perform the calculation, a specific algorithm can be
    given as a parameter.
    
    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to calculate the Inverse Fourier
        transform.
    method : {"dft", "fft"}, optional
        Method used to calculate the transform, by default F1_METHOD
    shift : bool
        Whether to shift the frequencies or not before applying the
        inverse, by default True.

    Returns
    -------
    Signal1
        Signal representing the Inverse Fourier Transform.
    """
    if shift:
        output = freq_shift(signal1)
    output = F1_METHODS[method](output)
    return output

def calculate_dft1(signal1: Signal1) -> Signal1:
    """Calculates the Inverse Fourier Transform :math:`\\mathcal{F}^{-1}\\{X[k]\\} = x[n]` such that

        .. math::
        x[n] = \\sum_{k=0}^{N-1}X[k]e^{j2\\pi nk/N}

    Returns
    -------
    Signal representing the Inverse Fourier Transform.
    """
    output = signal1.clone()
    signal_len = len(output)
    new_values = np.zeros(signal_len, dtype=complex)
    for n in tqdm(range(signal_len), "Calculating Inverse DFT"):
        temp = 0 + 0j
        for k in range(signal_len):
            temp += output.values[k] * np.exp(1j * (2 * n * k * np.pi / signal_len))
        new_values[n] = temp / signal_len
    output.values = new_values
    return output * signal_len

def calculate_fft1(signal1: Signal1) -> Signal1:
    """Calculates the inverse FFT of a given signal.

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to calculate the Inverse Fourier
        transform.

    Returns
    -------
    Signal1
        Signal representing the Inverse Fourier Transform.
    """
    output = signal1.clone()
    output.values = np.fft.ifft(output.values)
    return output

def freq_shift(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal_len = len(output)
    output.axis = output.axis + output.span() / 2
    output.values = np.array([*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
    return output

F1_METHODS = {
    "dft": calculate_dft1,
    "fft": calculate_fft1,
}