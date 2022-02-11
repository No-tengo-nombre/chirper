"""Base abstract signal"""
from __future__ import annotations
import numpy as np
import abc
from copy import deepcopy


class Signal(abc.ABC):
    """Abstract class representing a signal object of arbitrary dimensions."""

    @abc.abstractmethod
    def __getitem__(self, key):
        pass

    @abc.abstractmethod
    def __add__(self, signal):
        pass

    @abc.abstractmethod
    def __sub__(self, signal):
        pass

    @abc.abstractmethod
    def __mul__(self, signal):
        pass

    @abc.abstractmethod
    def __truediv__(self, signal):
        pass

    @abc.abstractmethod
    def __eq__(self, signal):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __abs__(self):
        pass

    @abc.abstractclassmethod
    def from_function(cls, axis, func, *args, **kwargs):
        """Creates a signal from an axis and a function.

        The function is applied to each element in the axis, so
        if the function f(x) = x**2 is given as a parameter to the axis
        [1, 2, 3, 4], the values would be [1, 4, 9, 16].

        Parameters
        ----------
        axis : np.ndarray
            Axis on which the function is mapped.
        func : function
            Function to map to the axis.
        """
        pass

    @abc.abstractclassmethod
    def from_file(cls, filename: str):
        """Creates a signal from a file.

        Parameters
        ----------
        filename : str
            File to read the data from.
        """
        pass

    @abc.abstractmethod
    def interpolate(self, value, method):
        """Interpolates the current values to obtain a new value."""
        pass

    @abc.abstractmethod
    def unpack(self):
        """Unpacks the signal into arrays. If used for its intended
        purpose, should be unpacked with *.
        """
        pass

    @abc.abstractmethod
    def apply_function(self, func, *args, **kwargs):
        """Applies a function to the values of the signal.

        Parameters
        ----------
        func : function
            Function to apply to the signal.
        """
        pass

    @abc.abstractmethod
    def export_to_file(self, filename: str):
        """Exports the signal values to a file.

        Parameters
        ----------
        filename : str
            File to export the data to.
        """
        pass

    @abc.abstractmethod
    def is_valid(self):
        """Checks whether the dimensions of the signal are valid."""
        pass

    def clone(self):
        """Makes a copy of this signal."""
        return deepcopy(self)

    def psd(self) -> Signal:
        """Generates the PSD (Power Spectral Density) of the signal.

        Returns
        -------
        Signal
            Signal representing the PSD.
        """
        copy = self.clone()
        copy.values = (copy.values.conjugate() * copy.values).real
        return copy

    def abs(self) -> Signal:
        """Takes the absolute value of the values."""
        return self.__abs__()

    def real_part(self) -> Signal:
        """Takes the real part of the values."""
        copy = self.clone()
        copy.values = np.real(copy.values)
        return copy

    def imag_part(self) -> Signal:
        """Takes the imaginary part of the values."""
        copy = self.clone()
        copy.values = np.imag(copy.values)
        return copy

    def conjugate(self) -> Signal:
        """Takes the conjugate of the values."""
        copy = self.clone()
        copy.values = copy.values.conjugate()
        return copy

    def shape(self) -> tuple:
        """Gets the shape of this signal."""
        return np.shape(self.values)
