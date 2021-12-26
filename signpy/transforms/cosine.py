from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from tqdm import tqdm

from signpy.config import C1_METHOD, C2_METHOD
if TYPE_CHECKING:
    from signpy.sgn import Signal1, Signal2

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def c1(signal1: Signal1, method=C1_METHOD) -> Signal1:
    """Calculates the one dimensional Cosine transform of a given
    signal.

    In order to perform the calculation, a specific algorithm can be
    given as a parameter.

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to calculate the Cosine transform.
    method : {"i", "ii", "iii", "iv", 1, 2, 3, 4}, optional
        Cosine transform to calculate, by default F1_METHOD

    Returns
    -------
    Signal1
        Signal representing the Cosine transform.
    """
    output = C1_METHODS[method](signal1)
    output.axis *= output.sampling_freq() / output.span()
    return output


def _calculate_i_1(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal_len = len(output)
    new_values = np.zeros(signal_len)
    for k in tqdm(range(signal_len), "Calculating DCT-I"):
        temp = 0
        for n, x in enumerate(output.values[1:-1]):
            temp += x * np.cos(np.pi * n * k / (signal_len - 1))
        new_values[k] = (temp + 0.5 * (output.values[0] +
                         (-1 ** k) * output.values[-1]))
    output.values = new_values * np.sqrt(2 / (signal_len - 1))
    return output


def _calculate_ii_1(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal_len = len(output)
    new_values = np.zeros(signal_len)
    for k in tqdm(range(signal_len), "Calculating DCT-II"):
        temp = 0
        for n, x in enumerate(output.values):
            temp += x * np.cos((np.pi * k / signal_len) * (n + 0.5))
        new_values[k] = temp
    output.values = new_values * np.sqrt(2 / signal_len)
    return output


def _calculate_iii_1(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal_len = len(output)
    new_values = np.zeros(signal_len)
    for k in tqdm(range(signal_len), "Calculating DCT-III"):
        temp = 0
        for n, x in enumerate(output.values[1:]):
            temp += x * np.cos((np.pi * n / signal_len) * (k + 0.5))
        new_values[k] = temp + 0.5 * output.values[0]
    output.values = new_values * np.sqrt(2 / signal_len)
    return output


def _calculate_iv_1(signal1: Signal1) -> Signal1:
    output = signal1.clone()
    signal_len = len(output)
    new_values = np.zeros(signal_len)
    for k in tqdm(range(signal_len), "Calculating DCT-IV"):
        temp = 0
        for n, x in enumerate(output.values):
            temp += x * np.cos((np.pi / signal_len) * (n + 0.5) * (k + 0.5))
        new_values[k] = temp
    output.values = new_values * np.sqrt(2 / signal_len)
    return output


C1_METHODS = {
    1: _calculate_i_1,
    2: _calculate_ii_1,
    3: _calculate_iii_1,
    4: _calculate_iv_1,
    "i": _calculate_i_1,
    "ii": _calculate_ii_1,
    "iii": _calculate_iii_1,
    "iv": _calculate_iv_1,
}

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal2 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def c2(signal2: Signal2, method=C2_METHOD) -> Signal2:
    """Calculates the two dimensional Cosine transform of a given
    signal.

    In order to perform the calculation, a specific algorithm can be
    given as a parameter.

    Parameters
    ----------
    signal2 : Signal2
        Two dimensional signal to calculate the Cosine transform.
    method : {"ii", "iv", 2, 4}, optional
        Cosine transform to calculate, by default F1_METHOD

    Returns
    -------
    Signal2
        Signal representing the Cosine transform.
    """
    output = C2_METHODS[method](signal2)
    output.ax1 *= output.ax1_sampling_freq() / output.ax1_span()
    output.ax2 *= output.ax2_sampling_freq() / output.ax2_span()
    return output


def _calculate_ii_2(signal2: Signal2) -> Signal2:
    output = signal2.clone()
    signal_shape = output.shape()
    N, M = signal_shape
    new_values = np.zeros(signal_shape)
    for k in tqdm(range(N), "Calculating 2D DCT-II"):
        for l in range(M):
            temp = 0
            for n in range(N):
                for m in range(M):
                    temp += output[n, m] * np.cos(np.pi * (m + 0.5)
                                                  * l / M) * np.cos(np.pi * (n + 0.5) * k / N)
            new_values[k, l] = temp
    output.values = new_values
    return output


def _calculate_iv_2(signal2: Signal2) -> Signal2:
    output = signal2.clone()
    signal_shape = output.shape()
    N, M = signal_shape
    new_values = np.zeros(signal_shape)
    for k in tqdm(range(N), "Calculating 2D DCT-IV"):
        for l in range(M):
            temp = 0
            for n in range(N):
                for m in range(M):
                    temp += output[n, m] * np.cos(np.pi * (2 * m + 1) * (2 * k + 1) / (
                        4 * N)) * np.cos(np.pi * (2 * n + 1) * (2 * l + 1) / (4 * M))
            new_values[k, l] = temp
    output.values = new_values
    return output


C2_METHODS = {
    2: _calculate_ii_2,
    4: _calculate_iv_2,
    "ii": _calculate_ii_2,
    "iv": _calculate_iv_2,
}
