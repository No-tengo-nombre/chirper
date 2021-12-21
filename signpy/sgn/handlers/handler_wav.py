"""Module for handling imports and exports with .wav files."""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from scipy.io import wavfile

from . import validate_extension
if TYPE_CHECKING:
    from .. import Signal1


def validate_filename(filename: str) -> None:
    """Validates the name of the file.

    Parameters
    ----------
    filename : str
        Name of the file to check.
    """
    validate_extension(filename, "wav")


def export_signal1(filename: str, signal1: Signal1, samp_rate=None) -> None:
    """Exports the given one dimensional signal to the .wav file."""
    validate_filename(filename)
    if samp_rate is None:
        samp_rate = int(signal1.sampling_freq())
    wavfile.write(filename, samp_rate, signal1.values.astype(np.float32))


def import_signal1(filename: str) -> Signal1:
    """Imports a one dimensional signal from a .wav file."""
    validate_filename(filename)
    pass
