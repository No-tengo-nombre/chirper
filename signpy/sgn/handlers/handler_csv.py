"""Module for handling imports and exports with .csv files."""
from __future__ import annotations
from typing import TYPE_CHECKING
import csv

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
    validate_extension(filename, "csv")

def export_signal1(filename: str, signal1: Signal1) -> None:
    """Exports the given one dimensional signal to the .csv file."""
    validate_filename(filename)
    with open(filename, "w+") as file:
        writer = csv.writer(file)
        writer.writerows(*signal1.unpack())

def import_signal1(filename: str) -> Signal1:
    """Imports a one dimensional signal from a .csv file."""
    validate_filename(filename)
    pass