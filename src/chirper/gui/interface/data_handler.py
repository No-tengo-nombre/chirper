from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import ChirpType


class DataHandler:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def handle(self, signal, request_type: ChirpType):
        return request_type.get_handled(self, signal)

    def handle_spectrogram(self, signal):
        return None
