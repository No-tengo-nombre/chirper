from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from tqdm import tqdm

from . import fourier
from chirper import window
from chirper.sgn import Signal1, Signal2


def stft1(signal1: Signal1, time_interval=None,
          window_method="rectangular", samp_time=0.01,
          interp_method="linear", shift=True, scale=True,
          *args, **kwargs) -> Signal2:
    windows = {
        "rectangular": window.w_rectangular,
        "gaussian": window.w_gaussian,
    }
    copy = signal1.clone()
    w_signal = windows[window_method](samp_time, *args, **kwargs)

    if time_interval is None:
        time_interval = (signal1.axis[0], signal1.axis[-1])

    copy = copy.get(*time_interval)

    windowed = copy.apply_window(w_signal, 0.5 * samp_time, interp_method)
    w_fourier = fourier.f1(windowed)

    time_axis = np.arange(*time_interval, samp_time)
    freq_axis = w_fourier.axis
    values = np.zeros((1, len(freq_axis)))

    for t in tqdm(time_axis + 0.5 * samp_time, "Calculating STFT"):
        windowed = copy.apply_window(w_signal, t, interp_method)
        w_fourier = fourier.f1(windowed, shift=shift, scale=scale)
        values_pad, w_pad = _pad(values, w_fourier.values)

        # If we had to pad the previous values, we update the frequency axis
        if len(w_fourier.axis) > len(freq_axis):
            freq_axis = w_fourier.axis
        values = np.vstack((values_pad, w_pad))
    return Signal2(time_axis, freq_axis, values[1:, :])


def _pad(arr1, arr2):
    # Helper function to handle padding of matrices when stacking
    len1, len2 = arr1.shape, arr2.shape
    if len(len1) == 1:
        max_len = max(len1[0], len2[0])
        arr1_copy = np.pad(arr1, (0, max_len - len1[0]))
        arr2_copy = np.pad(arr2, (0, max_len - len2[0]))
        return arr1_copy, arr2_copy
    else:
        max_len = max(len1[1], len2[0])
        arr1_copy = np.pad(arr1, [(0, 0), (0, max_len - len1[1])])
        arr2_copy = np.pad(arr2, (0, max_len - len2[0]))
        return arr1_copy, arr2_copy
