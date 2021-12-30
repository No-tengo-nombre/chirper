from __future__ import annotations
from typing import TYPE_CHECKING
import abc

if TYPE_CHECKING:
    from . import GuiInterface
    from .input_source import InputSource
    from .data_process import DataProcess
    from .data_handler import DataHandler


class ChirpType(abc.ABC):
    @abc.abstractmethod
    def get_processed(self, data_process: DataProcess, data):
        """Gets data processed by a data processor."""
        pass

    @abc.abstractmethod
    def get_handled(self, data_handler: DataHandler, signal):
        """Gets a signal handled by a data handler."""
        pass


class ChirpSource(abc.ABC):
    @abc.abstractmethod
    def get_fetched(self, input_source: InputSource):
        """Gets fetched by an input source."""
        pass


class Chirp:
    """Class for a request to the package."""

    def __init__(self, request_type: ChirpType, source: ChirpSource, root: GuiInterface) -> None:
        self.request_type = request_type
        self.source = source
        self.root = root
