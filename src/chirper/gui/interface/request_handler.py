from __future__ import annotations
from typing import TYPE_CHECKING

from chirper.gui.interface import ChirpSource, ChirpType

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp, ChirpSource, ChirpType


class RequestHandler:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def take_request(self, request: Chirp):
        request_type = request.request_type
        source = request.source

        data = self.send_to_source(source)
        signal = self.send_to_process(data, request_type)
        return self.send_to_handler(signal, request_type)

    def send_to_source(self, source: ChirpSource):
        return self.api.input_source.fetch(source)

    def send_to_process(self, data, request_type: ChirpType):
        return self.api.data_process.process(data, request_type)

    def send_to_handler(self, signal, request_type: ChirpType):
        return self.api.data_handler.handle(signal, request_type)
