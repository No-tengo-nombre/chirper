"""Module for handling imports and exports with .json files."""
from __future__ import annotations
from typing import TYPE_CHECKING

from chirper.utils.file_handling import validate_extension
if TYPE_CHECKING:
    from chirper.sgn import Signal1


def validate_filename(filename: str) -> None:
    """Validates the name of the file.

    Parameters
    ----------
    filename : str
        Name of the file to check.
    """
    validate_extension(filename, "json")


def export_signal1(filename: str, signal1: Signal1) -> None:
    """Exports the given one dimensional signal to the .json file."""
    validate_filename(filename)
    with open(filename, "w+") as file:
        pass


def import_signal1(filename: str) -> Signal1:
    """Imports a one dimensional signal from a .json file."""
    validate_filename(filename)
    pass
