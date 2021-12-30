from __future__ import annotations
from typing import TYPE_CHECKING
import sounddevice as sd

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import ChirpSource


def _get_kwarg(kwargs_dict, key, alt_val):
    try:
        return kwargs_dict[key]
    except KeyError:
        return alt_val

    
def parse_stream_data(indata, outdata, frames, time, status):
    return time.currentTime, indata


class InputSource:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def fetch(self, source: ChirpSource, **kwargs):
        return source.get_fetched(self, **kwargs)

    def fetch_microphone(self, **kwargs):
        samplerate = _get_kwarg(kwargs, "samplerate", 44100)
        channels = _get_kwarg(kwargs, "channels", 1)
        blocksize = _get_kwarg(kwargs, "blocksize", 4410)

