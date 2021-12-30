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
    def get_processed(self, data_process: DataProcess, data, **kwargs):
        """Gets data processed by a data processor."""
        pass

    @abc.abstractmethod
    def get_handled(self, data_handler: DataHandler, signal, **kwargs):
        """Gets a signal handled by a data handler."""
        pass

    @abc.abstractmethod
    def fetch(self, input_source: InputSource, chirp_source: ChirpSource):
        pass


# class ChirpDataRequest(ChirpType):
#     @abc.abstractmethod
#     def fetch(self, input_source: InputSource, chirp_source: ChirpSource):
#         pass


# class ChirpFlowControl(ChirpType):
#     pass


class ChirpSource(abc.ABC):
    @abc.abstractmethod
    def get_fetched(self, input_source: InputSource, **kwargs):
        """Gets fetched by an input source."""
        pass


class Chirp:
    """Class for a request to the package."""

    def __init__(self, request_type: ChirpType, source: ChirpSource, root: GuiInterface) -> None:
        self.request_type = request_type
        self.source = source
        self.root = root
