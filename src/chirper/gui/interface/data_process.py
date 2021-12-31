from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from chirper.sgn import Signal1
from chirper.transforms import fourier
if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp


class DataProcess:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def process(self, data, request: Chirp):
        return request.get_processed(self, data)

    def process_spectrogram(self, data):
        samp_freq = self.api.samplerate
        values = data.mean(axis=1)
        return fourier.f1(Signal1.from_freq(values, samp_freq))
