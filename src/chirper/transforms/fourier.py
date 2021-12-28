from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from tqdm import tqdm

from chirper.config import F1_METHOD, F2_METHOD
if TYPE_CHECKING:
    from chirper.sgn import Signal1, Signal2

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def f1(signal1: Signal1, method=F1_METHOD, shift=True, scale=True) -> Signal1:
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
    shift : bool, optional
        Whether to shift the frequencies or not after applying the
        transform, by default True.
    scale : bool, optional
        Whether to scale the frequencies or not after applying the
        transform, by default True.

    Returns
    -------
    Signal1
        Signal representing the Fourier Transform.
    """
    output = F1_METHODS[method](signal1)
    if scale:
        output.axis *= output.sampling_freq() / output.span()
    if shift:
        output = freq_shift1(output)
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


def freq_shift1(signal1: Signal1) -> Signal1:
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


def f2(signal2: Signal2, method=F2_METHOD, shift=True, scale=True) -> Signal2:
    output = F2_METHODS[method](signal2)
    if scale:
        output.ax0 *= output.ax0_sampling_freq() / output.ax0_span()
        output.ax1 *= output.ax1_sampling_freq() / output.ax1_span()
        # output.ax0 = output.ax0 * output.ax0_sampling_freq() / output.ax0_span()
        # output.ax1 = output.ax1 * output.ax1_sampling_freq() / output.ax1_span()
    if shift:
        output = freq_shift2(output)
    return output


def _calculate_dft2(signal2: Signal2) -> Signal2:
    output = signal2.clone()
    ax0_len, ax1_len = output.shape()
    new_values = np.zeros((ax0_len, ax1_len), dtype=complex)
    for u in tqdm(range(ax0_len), "Calculating DFT"):
        for v in range(ax1_len):
            temp = 0 + 0j
            for n in range(ax0_len):
                for m in range(ax1_len):
                    temp += output.values[n, m] * \
                        np.exp(-1j * 2 * np.pi *
                               (u * n / ax0_len + v * m / ax1_len))
            new_values[u, v] = temp
    output.values = new_values
    return output


def _calculate_fft2(signal2: Signal2) -> Signal2:
    output = signal2.clone()
    output.values = np.fft.fft2(output.values)
    return output


def freq_shift2(signal2: Signal2) -> Signal2:
    """Shift the frequencies of the signal.

    Parameters
    ----------
    signal2 : Signal2
        Signal to shift.

    Returns
    -------
    Signal2
        Shifted signal
    """
    output = signal2.clone()
    ax0_len, ax1_len = output.shape()
    output.ax0 = output.ax0 - output.ax0_span() / 2
    output.ax1 = output.ax1 - output.ax1_span() / 2
    output.values = np.fft.fftshift(output.values)
    return output


F2_METHODS = {
    "dft": _calculate_dft2,
    "fft": _calculate_fft2,
}
