"""Module for handling imports and exports with images."""
from __future__ import annotations
from typing import TYPE_CHECKING
import cv2
import numpy as np

from .utils import validate_extension
if TYPE_CHECKING:
    from .. import Signal2


def validate_filename(filename: str) -> None:
    """Validates the name of the file.

    Parameters
    ----------
    filename : str
        Name of the file to check.
    """
    valid_extensions = (
        "jpg",
        "jpeg",
        "png",
    )
    validate_extension(filename, valid_extensions)


def export_signal2(filename: str, signal2: Signal2) -> None:
    """Exports the given two dimensional signal."""
    validate_filename(filename)
    pass


def import_signal2(filename: str, channel="mean", norm=False, sf_ax0=1,
                   sf_ax1=1, sp_ax0=0, sp_ax1=0) -> Signal2:
    """Imports a two dimensional signal from a file.

    Parameters
    ----------
    filename : str
        File to read from.
    channel : {"mean", "r", "g", "b", 0, 1, 2}, optional
        How to handle images with multiple channels, by default "mean",
        which means it takes the mean of every channel.
    sf_ax0, sf_ax1 : float, optional
        Sampling frequency for each axis, by default 1.
    sp_ax0, sp_ax1 : float, optional
        Starting point for each axis, by default 0.

    Returns
    -------
    Signal2
        Read image.
    """
    validate_filename(filename)
    channels = {
        "mean": _import_s2_mean,
        "r": lambda vals, norm: _import_s2_channel(vals, 2, norm),
        "g": lambda vals, norm: _import_s2_channel(vals, 1, norm),
        "b": lambda vals, norm: _import_s2_channel(vals, 0, norm),
        0: lambda vals, norm: _import_s2_channel(vals, 0, norm),
        1: lambda vals, norm: _import_s2_channel(vals, 1, norm),
        2: lambda vals, norm: _import_s2_channel(vals, 2, norm),
    }
    signal = cv2.imread(filename)
    values = channels[channel](signal, norm)

    ax0_samp_period = 1 / sf_ax0
    ax1_samp_period = 1 / sf_ax1
    val_shape = np.shape(values)
    ax0 = np.arange(val_shape[0]) * ax0_samp_period - sp_ax0
    ax1 = np.arange(val_shape[1]) * ax1_samp_period - sp_ax1
    return ax0, ax1, values


def _import_s2_channel(values: np.ndarray, channel: int, norm=False):
    return values[:, :, channel] / 255 if norm else values[:, :, channel]


def _import_s2_mean(values: np.ndarray, norm=False):
    return np.mean(values, axis=2) / 255 if norm else np.mean(values, axis=2)
