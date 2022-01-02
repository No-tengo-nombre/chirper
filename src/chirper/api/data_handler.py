from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from ..sgn import Signal1, Signal2
from ..transforms import fourier
if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp


class DataHandler:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api
        self.values = None

    def handle(self, signal: Signal1, request: Chirp, **kwargs):
        return request.request_type.get_handled(self, signal, **kwargs)

    def handle_spectrogram(self, signal: Signal1, half=True, positive_half=True, max_time=5, **kwargs):
        if half:
            fourier_signal = fourier.f1(signal).half(positive_half)
        else:
            fourier_signal = fourier.f1(signal)

        # This runs on the first fetch request
        if self.values is None:
            return self._handle_spectrogram_empty(fourier_signal, max_time, **kwargs)

        # If the data was fetched before, `self.values` will not
        # be `None`
        else:
            return self._handle_spectrogram_notempty(fourier_signal, max_time, **kwargs)

    def _handle_spectrogram_empty(self, fourier_signal, max_time, **kwargs):
        self.dt = self.api.blocksize / self.api.samplerate

        # Accessing [:, None] turns the array into a column vector.
        # Then we take the transpose so that it has the proper dimensions
        self.values = Signal2(
            [0],
            fourier_signal.axis,
            fourier_signal.values[:, None].T,
        )
        assert self.values.is_valid(), "Something went wrong"
        return self.values.abs()

    def _handle_spectrogram_notempty(self, fourier_signal, max_time, **kwargs):
        self.values.ax0 = np.append(
            self.values.ax0,
            self.values.ax0[-1] + self.dt,
        )
        self.values.values = np.vstack(
            (self.values.values, fourier_signal.values)
        )

        if self.values.ax0_span() > max_time:
            end_time = self.values.ax0[-1]
            self.values = self.values.get_ax0(end_time - max_time)

        assert self.values.is_valid(), "Something went wrong"
        return self.values.abs()
