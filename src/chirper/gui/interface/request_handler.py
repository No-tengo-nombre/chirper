from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GuiInterface
    from .chirp import Chirp, ChirpSource, ChirpType


class RequestHandler:
    def __init__(self, api: GuiInterface) -> None:
        self.api = api

    def take_request(self, request: Chirp, return_raw_data=False, **kwargs):
        # get_raw_data = get_kwarg(kwargs, "return_raw", None)
        request_type = request.request_type
        source = request.source

        data = self.send_to_source(request, **kwargs)
        if return_raw_data:
            return data
        # The source returns something if data is being fetched. If the
        # request is a control request, it is None
        if data is not None:
            signal = self.send_to_process(data, request_type, **kwargs)
            return self.send_to_handler(signal, request_type, **kwargs)

    def send_to_source(self, request: Chirp, **kwargs):
        return self.api.input_source.fetch(request, **kwargs)

    def send_to_process(self, data, request_type: ChirpType, **kwargs):
        return self.api.data_process.process(data, request_type, **kwargs)

    def send_to_handler(self, signal, request_type: ChirpType, **kwargs):
        return self.api.data_handler.handle(signal, request_type, **kwargs)
