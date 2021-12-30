from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import ChirpType


class DataProcess:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def process(self, data, request_type: ChirpType):
        return request_type.get_processed(self, data)

    def process_spectrogram(self, data):
        # Do things with Chirper
        return None
