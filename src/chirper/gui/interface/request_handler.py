from __future__ import annotations
from typing import TYPE_CHECKING

from chirper.gui.interface import ChirpSource, ChirpType

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp, ChirpSource, ChirpType


class RequestHandler:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def take_request(self, request: Chirp, **kwargs):
        request_type = request.request_type
        source = request.source

        data = self.send_to_source(source, **kwargs)
        signal = self.send_to_process(data, request_type, **kwargs)
        return self.send_to_handler(signal, request_type, **kwargs)

    def send_to_source(self, source: ChirpSource, **kwargs):
        return self.api.input_source.fetch(source, **kwargs)

    def send_to_process(self, data, request_type: ChirpType, **kwargs):
        return self.api.data_process.process(data, request_type, **kwargs)

    def send_to_handler(self, signal, request_type: ChirpType, **kwargs):
        return self.api.data_handler.handle(signal, request_type, **kwargs)
