from __future__ import annotations
from typing import TYPE_CHECKING
import csv
import numpy as np
from scipy.io import wavfile

from signpy.exceptions import InvalidFileExtension
if TYPE_CHECKING:
    from . import Signal1


def validate_extension(filename: str, expected: str) -> None:
    """Validates the extension of the given filename.

    Parameters
    ----------
    filename : str
        Name of the file to check.
    expected : str
        Expected file extension.

    Raises
    ------
    InvalidFileExtension
        If the file extension is not valid.
    """
    extension = filename.split(".")[-1]
    if extension != expected:
        raise InvalidFileExtension(extension=extension, exp_extension=expected)


class HandlerCSV:
    """Class for handling imports and exports with .csv files."""
    @staticmethod
    def validate_filename(filename: str) -> None:
        """Validates the name of the file.

        Parameters
        ----------
        filename : str
            Name of the file to check.
        """
        validate_extension(filename, "csv")

    @staticmethod
    def export_signal1(filename: str, signal1: Signal1) -> None:
        """Exports the given one dimensional signal to the .csv file."""
        HandlerCSV.validate_filename(filename)
        with open(filename, "w+") as file:
            writer = csv.writer(file)
            writer.writerows(*signal1.unpack())

    @staticmethod
    def import_signal1(filename : str) -> Signal1:
        """Imports a one dimensional signal from a .csv file."""
        HandlerCSV.validate_filename(filename)
        pass


class HandlerJSON:
    """Class for handling imports and exports with .json files."""
    @staticmethod
    def validate_filename(filename: str) -> None:
        """Validates the name of the file.

        Parameters
        ----------
        filename : str
            Name of the file to check.
        """
        validate_extension(filename, "json")

    @staticmethod
    def export_signal1(filename: str, signal1: Signal1) -> None:
        """Exports the given one dimensional signal to the .json file."""
        HandlerJSON.validate_filename(filename)
        with open(filename, "w+") as file:
            pass

    @staticmethod
    def import_signal1(filename : str) -> Signal1:
        """Imports a one dimensional signal from a .json file."""
        HandlerJSON.validate_filename(filename)
        pass


class HandlerWAV:
    """Class for handling imports and exports with .wav files."""
    @staticmethod
    def validate_filename(filename: str) -> None:
        """Validates the name of the file.

        Parameters
        ----------
        filename : str
            Name of the file to check.
        """
        validate_extension(filename, "wav")

    @staticmethod
    def export_signal1(filename: str, signal1: Signal1, samp_rate=None) -> None:
        """Exports the given one dimensional signal to the .wav file."""
        HandlerWAV.validate_filename(filename)
        if samp_rate is None:
            samp_rate = int(signal1.sampling_freq())
        wavfile.write(filename, samp_rate, signal1.values.astype(np.float32))

    @staticmethod
    def import_signal1(filename: str) -> Signal1:
        """Imports a one dimensional signal from a .wav file."""
        HandlerWAV.validate_filename(filename)
        pass
