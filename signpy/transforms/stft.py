from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from signpy import window
from . import fourier
from signpy.sgn import Signal1, Signal2


def stft1(signal1: Signal1, time_interval=None,
          window_method="rectangular", samp_time=0.01,
          interp_method="linear", shift=True, scale=True,
          *args, **kwargs) -> Signal2:
    windows = {
        "window": window.w_rectangular,
        "gaussian": window.w_gaussian,
    }
    copy = signal1.clone()
    w_signal = windows[window_method](samp_time, *args, **kwargs)

    if time_interval is None:
        time_interval = (signal1.axis[0], signal1.axis[-1])

    windowed = copy.apply_window(w_signal, 0.5 * samp_time, interp_method)
    w_fourier = fourier.f1(windowed)

    time_axis = np.arange(*time_interval, samp_time)
    freq_axis = w_fourier.axis
    values = np.empty((len(time_axis), len(freq_axis)))

    for i, t in enumerate(np.arange(*time_interval, samp_time) + 0.5 * samp_time):
        windowed = copy.apply_window(w_signal, t, interp_method)
        w_fourier = fourier.f1(windowed, shift, scale)
        values[:, i] = w_fourier.values

    return Signal2(time_axis, freq_axis, values)
