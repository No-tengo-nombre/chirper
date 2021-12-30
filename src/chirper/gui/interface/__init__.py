from .request_handler import RequestHandler
from .input_source import InputSource
from .data_handler import DataHandler
from .data_process import DataProcess
from .chirp import Chirp, ChirpType, ChirpSource

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||| Base classes |||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class GuiInterface:
    def __init__(self) -> None:
        self.data_handler = DataHandler(self)
        self.input_source = InputSource(self)
        self.request_handler = RequestHandler(self)
        self.data_process = DataProcess(self)

    def get_request(self, request_data):
        request = self.parse_request_data(request_data)
        return self.request_handler.take_request(request)

    def parse_request_data(self, request_data) -> Chirp:
        return None

########################################################################################################################
# ||||||||||||||||||||||||||||||||||||||||||||||| Chirp Types |||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class ChirpTypeSpectrogram(ChirpType):
    def get_processed(self, data_process: DataProcess, data):
        return data_process.process_spectrogram(data)

    def get_handled(self, data_handler: DataHandler, signal):
        return data_handler.handle_spectrogram(signal)

########################################################################################################################
# ||||||||||||||||||||||||||||||||||||||||||||||| Chirp Sources |||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class ChirpSourceMicrophone(ChirpSource):
    def get_fetched(self, input_source: InputSource):
        return input_source.fetch_microphone()
