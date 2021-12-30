from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import ChirpSource


class InputSource:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def fetch(self, source: ChirpSource):
        return source.get_fetched(self)

    def fetch_microphone(self):
        return None
