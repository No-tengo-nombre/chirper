from __future__ import annotations
from typing import TYPE_CHECKING
import sounddevice as sd
import logging

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp


class InputSource:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api
        self.source = None

    def fetch(self, request: Chirp, **kwargs):
        return request.request_type.fetch(self, request.source, **kwargs)

    def fetch_microphone(self, blocksize=4410, **kwargs):
        output = self.source.read(blocksize)
        self.api.blocksize = blocksize
        if output[1]:
            logging.info("Overflow detected")
        return output[0]

    def start_microphone(self, samplerate=44100, channels=1, **kwargs):
        self.source = sd.InputStream(samplerate, channels)
        self.api.samplerate = samplerate
        self.api.channels = channels
        self.source.start()

    def stop_microphone(self, **kwargs):
        self.source.stop()
