from copy import deepcopy

from .request_handler import RequestHandler
from .input_source import InputSource
from .data_handler import DataHandler
from .data_process import DataProcess
from .chirp import Chirp, ChirpType, ChirpSource

########################################################################################################################
# ||||||||||||||||||||||||||||||||||||||||||||||| Chirp Types |||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class ChirpTypeSpectrogram(ChirpType):
    def get_processed(self, data_process: DataProcess, data, **kwargs):
        return data_process.process_spectrogram(data, **kwargs)

    def get_handled(self, data_handler: DataHandler, signal, **kwargs):
        return data_handler.handle_spectrogram(signal, **kwargs)

    def fetch(self, input_source: InputSource, source: ChirpSource, **kwargs):
        return source.get_fetched(input_source, **kwargs)


class ChirpTypeStart(ChirpType):
    def get_processed(self, data_process: DataProcess, data, **kwargs):
        return None

    def get_handled(self, data_handler: DataHandler, signal, **kwargs):
        return None

    def fetch(self, input_source: InputSource, source: ChirpSource, **kwargs):
        return source.start_stream(input_source, **kwargs)


class ChirpTypeStop(ChirpType):
    def get_processed(self, data_process: DataProcess, data, **kwargs):
        return None

    def get_handled(self, data_handler: DataHandler, signal, **kwargs):
        return None

    def fetch(self, input_source: InputSource, source: ChirpSource, **kwargs):
        return source.stop_stream(input_source, **kwargs)

########################################################################################################################
# ||||||||||||||||||||||||||||||||||||||||||||||| Chirp Sources |||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class ChirpSourceMicrophone(ChirpSource):
    def get_fetched(self, input_source: InputSource, **kwargs):
        return input_source.fetch_microphone(**kwargs)

    def start_stream(self, input_source: InputSource, **kwargs):
        return input_source.start_microphone(**kwargs)

    def stop_stream(self, input_source: InputSource, **kwargs):
        return input_source.stop_microphone(**kwargs)

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||| Base classes |||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class GuiInterface:
    """Interface for the GUI to send instructions and receive data."""
    REQUEST_TYPES = {
        "spectrogram": ChirpTypeSpectrogram,
        "start": ChirpTypeStart,
        "stop": ChirpTypeStop,
    }
    REQUEST_SOURCES = {
        "microphone": ChirpSourceMicrophone,
    }

    def __init__(self) -> None:
        self.data_handler = DataHandler(self)
        self.input_source = InputSource(self)
        self.request_handler = RequestHandler(self)
        self.data_process = DataProcess(self)

    def make_request(self, request_data):
        request, kwargs = self.parse_request_data(request_data)
        result = self.request_handler.take_request(request, **kwargs)
        return result

    def parse_request_data(self, request_data: dict) -> Chirp:
        copy_data = deepcopy(request_data)
        data_type = copy_data.pop("request_type")
        data_source = copy_data.pop("source")

        # Make the request
        request_type = GuiInterface.REQUEST_TYPES[data_type]()
        source = GuiInterface.REQUEST_SOURCES[data_source]()
        return Chirp(request_type, source), copy_data
