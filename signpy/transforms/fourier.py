from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from numpy.core.numeric import outer
from tqdm import tqdm

from signpy.config import F1_METHOD, F2_METHOD
from signpy.sgn import Signal, Signal2
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
    output.axis *= output.sampling_freq() / output.span()
    if shift:
        output = freq_shift(output)
    return output


def _calculate_dft1(signal1: Signal1) -> Signal1:
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
            temp += output.values[n] * \
                np.exp(-1j * (2 * n * k * np.pi / signal_len))
        new_values[k] = temp
    output.values = new_values
    return output


def _calculate_fft1(signal1: Signal1) -> Signal1:
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
    output.values = np.array(
        [*output.values[signal_len // 2:], *output.values[:signal_len // 2]])
    return output


F1_METHODS = {
    "dft": _calculate_dft1,
    "fft": _calculate_fft1,
}

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal2 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def f2(signal2: Signal2, method=F2_METHOD, shift=True) -> Signal2:
    output = F2_METHODS[method](signal2)
    return output


def _calculate_dft2(signal2: Signal2) -> Signal2:
    output = signal2.clone()
    ax1_len, ax2_len = output.shape()
    new_values = np.zeros((ax1_len, ax2_len), dtype=complex)
    for u in tqdm(range(ax1_len), "Calculating DFT"):
        for v in range(ax2_len):
            temp = 0 + 0j
            for n in range(ax1_len):
                for m in range(ax2_len):
                    temp += output.values[n, m] * \
                        np.exp(-1j * 2 * np.pi *
                               (u * n / ax1_len + v * m / ax2_len))
            new_values[u, v] = temp
    output.values = new_values
    return output


def _calculate_fft2(signal2: Signal2) -> Signal2:
    output = signal2.clone()
    output.values = np.fft.fft2(output.values)
    return output


F2_METHODS = {
    "dft": _calculate_dft2,
    "fft": _calculate_fft2,
}
