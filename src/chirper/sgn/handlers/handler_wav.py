"""Module for handling imports and exports with .wav files."""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from scipy.io import wavfile

from .utils import validate_extension
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


def import_signal1(filename: str, amplification=1/200, channels="mean", *args, **kwargs) -> Signal1:
    """Imports a one dimensional signal from a .wav file."""
    channel_handler = {
        "mean": _mean,
        "get": _get,
    }
    validate_filename(filename)
    sf, values = wavfile.read(filename)
    axis = np.arange(values.shape[0]) / sf
    values = channel_handler[channels](values, *args, **kwargs)
    return axis, amplification * values


def _mean(values: np.ndarray):
    if len(values.shape) != 1:
        return values.mean(axis=1)
    else:
        return values


def _get(values: np.ndarray, channel=0):
    return values[:, :, channel]
