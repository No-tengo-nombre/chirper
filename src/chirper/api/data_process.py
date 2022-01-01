from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from ..sgn import Signal1
if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp


class DataProcess:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def process(self, data, request: Chirp, **kwargs):
        return request.request_type.get_processed(self, data, **kwargs)

    def process_spectrogram(self, data, **kwargs):
        samp_freq = self.api.samplerate
        values = data.mean(axis=1)
        return Signal1.from_freq(values, samp_freq)
