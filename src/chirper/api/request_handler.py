from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp


class RequestHandler:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def take_request(self, request: Chirp, **kwargs):
        data = self.send_to_source(request, **kwargs)

        # The source returns something if data is being fetched. If the
        # request is a control request, it is None
        if data is not None:
            logging.debug(f"Received request | {request}")
            signal = self.send_to_process(data, request, **kwargs)
            return self.send_to_handler(signal, request, **kwargs)

    def send_to_source(self, request: Chirp, **kwargs):
        return self.api.input_source.fetch(request, **kwargs)

    def send_to_process(self, data, request: Chirp, **kwargs):
        return self.api.data_process.process(data, request, **kwargs)

    def send_to_handler(self, signal, request: Chirp, **kwargs):
        return self.api.data_handler.handle(signal, request, **kwargs)
