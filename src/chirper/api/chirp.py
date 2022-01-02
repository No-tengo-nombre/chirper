from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .input_source import InputSource
    from .data_process import DataProcess
    from .data_handler import DataHandler


class ChirpType:
    def get_processed(self, data_process: DataProcess, data, **kwargs):
        """Gets data processed by a data processor."""
        return None

    def get_handled(self, data_handler: DataHandler, signal, **kwargs):
        """Gets a signal handled by a data handler."""
        return None

    def fetch(self, input_source: InputSource, chirp_source: ChirpSource, **kwargs):
        return None


class ChirpSource:
    def get_fetched(self, input_source: InputSource, **kwargs):
        """Gets fetched by an input source."""
        return None


class Chirp:
    """Class for a request to the package."""

    def __init__(self, request_type: ChirpType, source: ChirpSource) -> None:
        self.request_type = request_type
        self.source = source

    def __str__(self) -> str:
        return f"request_type: {self.request_type} - source: {self.source}"
