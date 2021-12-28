"""
===================
Signal manipulation
===================

This subpackage gives the basic tools needed to create, import and
export signals of different dimensions.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import bisect
import operator
import abc
from tqdm import tqdm
from numbers import Number, Real
from copy import deepcopy
from multipledispatch import dispatch

from signpy.exceptions import DimensionError
from signpy.config import (CONVOLUTION_METHOD, INTERP1_METHOD,
                           INTERP2_METHOD, CROSS_CORRELATION_METHOD,
                           KERNEL_OOB)
from signpy import math_lib
from .handlers import (handler_csv, handler_json, handler_wav,
                       handler_img)


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

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class Signal1(Signal):
    """Class representing a one dimensional signal."""
    handlers = {
        "csv": handler_csv,
        "json": handler_json,
        "wav": handler_wav,
    }

    def __init__(self, axis: np.ndarray, values: np.ndarray):
        """Creates a signal from an independent axis and a values list.

        Parameters
        ----------
        axis : array_like
            List of elements representing the independent variable
            (usually time).
        values : array_like
            List of elements representing the dependent variable for
            each axis element.

        Raises
        ------
        DimensionError
            Raises this when the dimensions of `axis` and `values`
            don't match each other.
        """
        if len(axis) != len(values):
            raise DimensionError(
                "The dimensions of the values do not match.", len(values), len(axis))
        self.axis = np.array(axis)
        self.values = np.array(values)

    def __getitem__(self, key):
        return self.values[key]

    @dispatch(slice)
    def __call__(self, key):
        # Slices the indices based on the given key, then intersects
        # them to get all the indices
        indices1 = np.where(
            key.start <= self.axis if key.start else self.axis)
        indices2 = np.where(
            self.axis <= key.stop if key.stop else self.axis)
        indices = np.intersect1d(indices1, indices2)
        return [self.values[i] for i in indices]

    def __call__(self, key, inter_method=INTERP1_METHOD):
        return self.interpolate(key, inter_method)[2]

    def __radd__(self, num):
        return self.__add__(num)

    @dispatch(Number)
    def __add__(self, value):
        return Signal1(self.axis, self.values + value)

    @dispatch(object)
    def __add__(self, signal):
        return Signal1(*self._do_bin_operation(signal, operator.add))

    def __rsub__(self, num):
        return num + self * -1

    @dispatch(Number)
    def __sub__(self, value):
        return Signal1(self.axis, self.values - value)

    @dispatch(object)
    def __sub__(self, signal):
        return Signal1(*self._do_bin_operation(signal, operator.sub))

    def __rmul__(self, num):
        return self.__mul__(num)

    @dispatch(Number)
    def __mul__(self, value):
        return Signal1(self.axis, self.values * value)

    @dispatch(object)
    def __mul__(self, signal):
        return Signal1(*self._do_bin_operation(signal, operator.mul))

    def __rtruediv__(self, num):
        return Signal1(self.axis, num / self.values)

    @dispatch(Number)
    def __truediv__(self, value):
        return Signal1(self.axis, self.values / value)

    @dispatch(object)
    def __truediv__(self, signal):
        return Signal1(*self._do_bin_operation(signal, operator.truediv))

    def __eq__(self, signal):
        return (
            np.array_equal(self.axis, signal.axis)
            and np.array_equal(self.values, signal.values)
        )

    def __str__(self):
        return f"{self.axis}\n{self.values}"

    def __abs__(self):
        return Signal1(self.axis, list(map(operator.abs, self.values)))

    def __len__(self):
        return len(self.axis)

    def _do_bin_operation(self, signal, operation, inter_method=INTERP1_METHOD, debug=False):
        # Joins the axes of both signals
        axis_list = np.union1d(self.axis, signal.axis)
        # axis_list.sort()

        new_values = np.array([])
        iterable = tqdm(
            axis_list, "Applying operation") if debug else axis_list
        for t in iterable:
            # Interpolates the values
            y1 = self(t, inter_method)
            y2 = signal(t, inter_method)
            # Operates using the interpolated values
            new_values = np.append(new_values, operation(y1, y2))
        return axis_list, new_values

    @classmethod
    def from_function(cls, axis: np.ndarray, func, *args, **kwargs):
        """Creates a signal from an axis list and a function.

        The function is applied to each element in the axis, so if the
        function f(x) = x**2 is given as a parameter to the axis
        [1, 2, 3, 4], the values should be [1, 4, 9, 16].

        Parameters
        ----------
        axis : array_like
            List of elements representing the independent variable
            (usually time).
        func : function
            Function to apply to each element.
        """
        return cls(axis, func(np.array(axis), *args, **kwargs))

    @classmethod
    def from_file(cls, filename: str, *args, **kwargs):
        """Creates a signal from a file.

        Parameters
        ----------
        filename : str
            Name of the file, including its path.

        Returns
        -------
        Signal1
            Signal after being read.

        Raises
        ------
        ValueError
            [description]
        """
        extension = filename.split(".")[-1]
        if extension == filename:
            raise ValueError()
        return cls(*Signal1.handlers[extension].import_signal1(
            filename, *args, **kwargs
        ))

    @classmethod
    def from_freq(cls, values: np.ndarray, sf=1, sp=0):
        """Creates a signal from a values list and a sampling frequency.

        Parameters
        ----------
        values : array_like
            List of elements representing the dependent variable for
            each axis element.
        sf : real number, optional
            Sampling frequency used to create the axis, by default 1.
        sp : real number, optional
            Starting point for the axis, by default 0.
        """
        samp_period = 1 / sf
        vals = np.array(values)
        axis = np.arange(len(values), samp_period) - sp
        return cls(axis, vals)

    @dispatch(Number, str)
    def add(self, value, method=INTERP1_METHOD, *args, **kwargs):
        """Adds this signal with another value."""
        return Signal1(self.axis, self.values + value)

    @dispatch(object, str)
    def add(self, signal, method=INTERP1_METHOD):
        """Adds this signal with another value."""
        return Signal1(*self._do_bin_operation(signal, operator.add, method))

    @dispatch(Number, str)
    def sub(self, value, method=INTERP1_METHOD):
        """Subtracts this signal with another value."""
        return Signal1(self.axis, self.values - value)

    @dispatch(object, str)
    def sub(self, signal, method=INTERP1_METHOD, *args, **kwargs):
        """Subtracts this signal with another value."""
        return Signal1(*self._do_bin_operation(signal, operator.sub, method, *args, **kwargs))

    @dispatch(Number, str)
    def mul(self, value, method=INTERP1_METHOD, *args, **kwargs):
        """Multiplies this signal with another value."""
        return Signal1(self.axis, self.values * value)

    @dispatch(object, str)
    def mul(self, signal, method=INTERP1_METHOD, *args, **kwargs):
        """Multiplies this signal with another value."""
        return Signal1(*self._do_bin_operation(signal, operator.mul, method, *args, **kwargs))

    @dispatch(Number, str)
    def div(self, value, method=INTERP1_METHOD, *args, **kwargs):
        """Divides this signal with another value."""
        return Signal1(self.axis, self.values / value)

    @dispatch(object, str)
    def div(self, signal, method=INTERP1_METHOD, *args, **kwargs):
        """Divides this signal with another value."""
        return Signal1(*self._do_bin_operation(signal, operator.truediv, method, *args, **kwargs))

    def sampling_freq(self) -> float:
        """Calculates the sampling frequency in hertz, assuming it is constant."""
        sf = 1 / (self.axis[1] - self.axis[0])
        return sf if sf > 0 else 0

    def interpolate_list(self, elements: list, method=INTERP1_METHOD):
        """Interpolates the current values to obtain new ones.

        Parameters
        ----------
        elements : list
            List of elements to interpolate.
        method : {"linear", "sinc"}, optional
            Method used for the interpolation, by default INTERP1_METHOD.

        Returns
        -------
        copy : Signal1
            Copy of the signal with the new values interpolated.
        """
        copy = self.clone()
        for t in elements:
            copy, _, _ = copy.interpolate(t, method)
        return copy

    def interpolate(self, element, method=INTERP1_METHOD):
        """Interpolates the current values to obtain a new value.

        Parameters
        ----------
        element : float
            Element to apply the interpolation to.
        method : {"linear", "sinc"}, optional
            Method used for the interpolation, by default INTERP1_METHOD.
        Returns
        -------
        copy : Signal1
            Copy of the signal with the new value interpolated.
        index : int
            Index of the interpolated value.
        new_value : float
            Value of the interpolated value.
        """
        methods = {
            "linear": self._linear_interp,
            "sinc": self._sinc_interp,
        }
        copy = self.clone()

        if element not in self.axis:
            return methods[method](element)
        else:
            index = bisect.bisect(copy.axis, element) - 1
            return copy, index, self[index]

    def _linear_interp(self, element):
        copy = self.clone()
        new_index = bisect.bisect(self.axis, element)
        copy.axis = np.insert(copy.axis, new_index, element)
        copy.values = np.insert(copy.values, new_index, 0)

        ta = copy.axis[new_index - 1]
        xa = copy.values[new_index - 1]
        try:
            tb = copy.axis[new_index + 1]
            xb = copy.values[new_index + 1]
        except IndexError:
            # This code is reached if the program tries to
            # interpolate points out of the range. In this case,
            # it simply interpolates using the last value. For
            # `xb` we take the element -2 because, if this code
            # is reached, a 0 was added in the last value
            tb = copy.axis[-1]
            xb = copy.values[-2]

        # Linearly interpolates
        new_value = xa + (xb - xa) * (element - ta) / (tb - ta)
        copy.values[new_index] = new_value
        return copy, new_index, new_value

    def _sinc_interp(self, element):
        copy = self.clone()
        new_index = bisect.bisect(self.axis, element)
        copy.axis = np.insert(copy.axis, new_index, element)
        copy.values = np.insert(copy.values, new_index, 0)

        fs = copy.sampling_freq()
        result = 0
        for t, x in zip(*self.unpack()):
            result += x * np.sinc(fs * (element - t))

        copy.values[new_index] = result
        return copy, new_index, result

    def unpack(self):
        """Unpacks the signal into two arrays. If used for its
        intended purpose, should be unpacked with *.
        """
        return self.axis, self.values

    def span(self) -> float:
        """Gets the span of the signal"""
        return self.axis[-1] - self.axis[0]

    def half(self, first=True):
        """Gets half of the signal"""
        half_span = int(len(self) / 2)
        if first:
            return Signal1(self.axis[:half_span], self.values[:half_span])
        else:
            return Signal1(self.axis[half_span:], self.values[half_span:])
        # return self[:int(self.span() / 2)] * 2 if first else self[int(self.span() / 2):] * 2

    def rect_smooth(self, factor: int) -> Signal1:
        """Directly applies a rectangular smoothing to the signal.

        With this method the edges of the signal look a bit rough.

        Parameters
        ----------
        factor : int (odd)
            Smoothing factor.

        Returns
        -------
        Signal1
            Smooth signal.
        """
        copy = self.clone()
        if factor % 2 != 1 or factor <= 1:
            raise ValueError("The smoothing factor must be an odd number.")
        shift = int((factor - 1) / 2)
        self_len = len(copy)
        new_values = copy.values[0:1]               # Copies the first element

        # Smooths the first elements with the only possible elements
        for n in range(1, shift):
            arr = copy.values[0:2 * n + 1]
            new_values = np.append(new_values, arr.sum() / (2 * n + 1))

        # Smooths the other elements using the given factor
        for n in range(shift, self_len - shift):
            arr = copy.values[n - shift:n + shift + 1]
            new_values = np.append(new_values, arr.sum() / factor)

        # Smooths the last elements adapting the smoothing factor
        for n in range(self_len - shift, self_len):
            new_shift = self_len - n - 1
            arr = copy.values[n - new_shift:self_len]
            new_values = np.append(new_values, arr.sum() / (2 * new_shift + 1))

        assert self_len == len(
            new_values), "There was an error during the smoothing."
        copy.values = new_values
        return copy

    def apply_function(self, func, *args, **kwargs) -> Signal1:
        """Applies a function to the values of the signal.

        Parameters
        ----------
        func : function
            Function to apply to the signal.

        Returns
        -------
        Signal1
            Modified signal.
        """
        copy = self.clone()
        copy.values = np.array([func(x, *args, **kwargs) for x in copy.values])
        return copy

    def apply_function_tuple(self, func, *args, **kwargs) -> Signal1:
        """Applies a function to both the axis and values of the signal.

        Parameters
        ----------
        func : function
            Function to apply to the signal.

        Returns
        -------
        Signal1
            Modified signal.
        """
        copy = self.clone()
        copy.values = np.array([func(t, x, *args, **kwargs)
                                for t, x in zip(copy.axis, copy.values)])
        return copy

    def convolute(self, signal1: Signal1, method=CONVOLUTION_METHOD) -> Signal1:
        """Convolute this signal with another.

        Parameters
        ----------
        signal1 : Signal1
            Signal to convolute with.
        method : {"fft", "direct"}, optional
            Method utilized to calculate the convolution, by
            default CONVOLUTION_METHOD.

        Returns
        -------
        Signal1
            Convoluted signal.
        """
        return math_lib.convolution(self, signal1, method)

    def cross_correlate(self, signal1: Signal1,
                        method=CROSS_CORRELATION_METHOD) -> Signal1:
        """Cross-correlates this signal with another.

        Parameters
        ----------
        signal1 : Signal1
            Signal to cross-correlate with.
        method : {"direct"}, optional
            Method utilized to calculate the cross-correlation, by
            default CROSS_CORRELATION_METHOD.

        Returns
        -------
        Signal1
            Cross-correlated signal.
        """
        return math_lib.cross_correlation(self, signal1, method)

    def auto_correlate(self, method=CROSS_CORRELATION_METHOD) -> Signal1:
        """Auto-correlates this signal.

        Parameters
        ----------
        method : {"direct"}, optional
            Method utilized to calculate the auto-correlation, by
            default CROSS_CORRELATION_METHOD.

        Returns
        -------
        Signal1
            Auto-correlated signal.
        """
        return math_lib.cross_correlation(self, self, method)

    def shift(self, value) -> Signal1:
        """Shifts the axis by `value`."""
        copy = self.clone()
        copy.axis += value
        return copy

    def export_to_file(self, filename: str, *args, **kwargs):
        """Exports the one dimensional signal to the given file.

        Parameters
        ----------
        filename : str
            String corrresponding to the file.

        Raises
        ------
        ValueError
            If the filename is empty (e.g trying to export to the file ".csv").
        """
        extension = filename.split(".")[-1]
        if extension == filename:
            raise ValueError()
        Signal1.handlers[extension].export_signal1(
            filename, self, *args, **kwargs)

    def apply_window(self, window: Signal1, center: Real,
                     interp_method=INTERP1_METHOD, *args,
                     **kwargs) -> Signal1:
        """Applies a window function to the signal.

        For this implementation it is assumed that the window function
        is zero outside of its given axis.

        Parameters
        ----------
        window : Signal1
            Window signal.
        center : Real
            Center point where the window is applied.
        interp_method : string, optional
            Method used for the interpolation, by default INTERP1_METHOD

        Returns
        -------
        Signal1
            Signal after applying the window.
        """
        w_span = window.span()
        copy = self.clone()

        # Divides the signals into the three relevant parts
        l_signal = copy.get(stop=center - w_span / 2)
        c_signal = copy.get(center - w_span / 2, center + w_span / 2)
        r_signal = copy.get(start=center + w_span / 2)

        # We assume the signals are zero outside of their specified range
        l_signal.values = np.zeros(len(l_signal))
        r_signal.values = np.zeros(len(r_signal))

        # We apply the window to the center part
        c_signal = c_signal.mul(window.clone().shift(
            center), interp_method, *args, **kwargs)

        return l_signal.concatenate(c_signal, r_signal)

    def get(self, start=None, stop=None) -> Signal1:
        """Gets a portion of the signal.

        Parameters
        ----------
        start : float, optional
            Starting point, by default the first point.
        stop : float, optional
            Stopping point, by default the last point.

        Returns
        -------
        Signal1
            The cut signal.
        """
        copy = self.clone()
        if start is None:
            start_index = 0
        else:
            start_index = bisect.bisect(copy.axis, start)

        if stop is None:
            stop_index = -1
        else:
            stop_index = bisect.bisect(copy.axis, stop)

        copy.axis, copy.values = (copy.axis[start_index:stop_index],
                                  copy.values[start_index:stop_index])
        return copy

    def concatenate(self, *signals) -> Signal1:
        """Concatenates this signal with others."""
        copy = self.clone()
        s_axis, s_values = ((sign.axis for sign in signals),
                            (sign.values for sign in signals))
        return Signal1(np.concatenate((copy.axis, *s_axis)),
                       np.concatenate((copy.values, *s_values)))

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal2 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class Signal2(Signal):
    """Class representing a two dimensional signal."""
    handlers = {
        "jpeg": handler_img,
        "jpg": handler_img,
        "png": handler_img,
    }

    def __init__(self, ax0: np.ndarray, ax1: np.ndarray,
                 values: np.ndarray):
        """Creates a two dimensional signal by giving two axes and a
        matrix.

        Each axis corresponds to one of the dimensions, where
        `ax0` indexes the rows of `values`, while `ax1` indexes its
        columns.

        Parameters
        ----------
        ax0 : array_like
            First axis, which indexes the rows of `values`.
        ax1 : array_like
            Second axis, which indexes the columns of `values`.
        values : two-dimensional array_like
            Matrix that indicates the values of the signal for every
            point.

        Raises
        ------
        DimensionError
            Raises this when the shape of `values` doesn't match the
            sizes of `ax0` and `ax1`.

        Example
        -------
        Creating the following object
        >>> ax0 = [1, 2, 3]
        >>> ax1 = [2, 4, 6]
        >>> vals = [
        >>>     [1, 2, 3],
        >>>     [2, 4, 6],
        >>>     [3, 6, 9]
        >>> ]
        >>> signal = Signal2(ax0, ax1, vals)
        can be understood as the following plot
          ax1
           |
         6 |  3  6  9
           |
         4 |  2  4  6
           |
         2 |  1  2  3
           |
         0 |--------- ax0
           0  1  2  3
        """
        if np.shape(values) != (len(ax0), len(ax1)):
            raise DimensionError("The dimensions of the values do not match.", np.shape(
                values), (len(ax0), len(ax1)))
        self.ax0 = np.array(ax0)
        self.ax1 = np.array(ax1)
        self.values = np.array(values)

    def __getitem__(self, key):
        return self.values[key]

    @dispatch(Real, Real)
    def __call__(self, key_x, key_y):
        return self.interpolate(key_x, key_y)[2]

    @dispatch(Real, Real, str)
    def __call__(self, key_x, key_y, interp_method=INTERP2_METHOD):
        return self.interpolate(key_x, key_y, method=interp_method)[2]

    def __radd__(self, num):
        return self.__add__(num)

    @dispatch(Number)
    def __add__(self, value):
        return Signal2(self.ax0, self.ax1, self.values + value)

    @dispatch(object)
    def __add__(self, signal):
        return Signal2(*self._do_bin_operation(signal, operator.add))

    def __rsub__(self, num):
        return num + self * -1

    @dispatch(Number)
    def __sub__(self, value):
        return Signal2(self.ax0, self.ax1, self.values - value)

    @dispatch(object)
    def __sub__(self, signal):
        return Signal2(*self._do_bin_operation(signal, operator.sub))

    def __rmul__(self, num):
        return self.__mul__(num)

    @dispatch(Number)
    def __mul__(self, value):
        return Signal2(self.ax0, self.ax1, self.values * value)

    @dispatch(object)
    def __mul__(self, signal):
        return Signal2(*self._do_bin_operation(signal, operator.mul))

    def __rtruediv__(self, num):
        return Signal2(self.ax0, self.ax1, num / self.values)

    @dispatch(Number)
    def __truediv__(self, value):
        return Signal2(self.ax0, self.ax1, self.values / value)

    @dispatch(object)
    def __truediv__(self, signal):
        return Signal2(*self._do_bin_operation(signal, operator.truediv))

    def __eq__(self, signal):
        return (
            np.array_equal(self.ax0, signal.ax0)
            and np.array_equal(self.ax1, signal.ax1)
            and np.array_equal(self.values, signal.values)
        )

    def __str__(self):
        return f"{self.ax0}\n{self.ax1}\n{self.values}"

    def __abs__(self):
        copy = self.clone()
        copy.values = abs(copy.values)
        return copy

    def _do_bin_operation(self, signal, operation):
        # Joins the axes of both signals
        new_ax0 = np.union1d(self.ax0, signal.ax0)
        new_ax1 = np.union1d(self.ax1, signal.ax1)
        new_ax0.sort()
        new_ax1.sort()

        new_values = new_ax1.copy()
        for x in new_ax0:
            row = np.array([])
            for y in new_ax1:
                # Interpolates the values
                val1 = self(x, y)
                val2 = signal(x, y)
                # Operates using the interpolated values
                row = np.append(row, operation(val1, val2))
            new_values = np.vstack((new_values, row))
        return new_ax0, new_ax1, new_values

    @classmethod
    def from_function(cls, ax0, ax1, func, *args, **kwargs):
        """Creates a signal from two axes and a function.

        The function is applied to each element in the axis, so
        if the function `f(x, y) = x**2 + y**2` is given as a parameter to
        the axes `[1, 2, 3]` and `[-1, -2, -3]`, the values would be the
        matrix `[[2, 5, 10], [5, 8, 13], [10, 13, 18]]`.

        Parameters
        ----------
        ax0 : np.ndarray
            First on which the function is mapped.
        ax1 : np.ndarray
            Second on which the function is mapped.
        func : function
            Function to map to the axes.
        """
        values = np.array([[func(x, y, *args, **kwargs)
                          for x in ax0] for y in ax1])
        return cls(ax0, ax1, values)

    @classmethod
    def from_file(cls, filename: str, *args, **kwargs):
        """Creates a signal from a file. If the file is an image with
        an RGB channel, using `channel` you can specify which channel
        to read from, or the method used to handle them.

        Parameters
        ----------
        filename : str
            File to read the data from.
        """
        extension = filename.split(".")[-1]
        if extension == filename:
            raise ValueError()
        return cls(*Signal2.handlers[extension].import_signal2(filename, *args, **kwargs))

    @classmethod
    def from_freq(cls, values: np.ndarray, sf_ax0=1, sf_ax1=1, sp_ax0=0, sp_ax1=0):
        """Creates a two dimensional signal by giving a values matrix
        and a frequency for each axis.

        Each axis corresponds to one of the dimensions, where
        `ax0` indexes the rows of `values`, while `ax1` indexes its
        columns.

        Parameters
        ----------
        values : two-dimensional array_like
            Matrix that indicates the values of the signal for every
            point.
        sf_ax0 : float, optional
            Sampling frequency of the first axis, by default 1.
        sf_ax1 : float, optional
            Sampling frequency of the second axis, by default 1.
        sp_ax0 : float, optional
            Starting point for the first axis, by default 0.
        sp_ax1 : float, optional
            Starting point for the second axis, by default 0.
        """
        ax0_samp_period = 1 / sf_ax0
        ax1_samp_period = 1 / sf_ax1
        vals = np.array(values)
        val_shape = np.shape(values)

        ax0 = np.arange(val_shape[0]) * ax0_samp_period - sp_ax0
        ax1 = np.arange(val_shape[1]) * ax1_samp_period - sp_ax1
        return cls(ax0, ax1, vals)

    @dispatch(Real, Real)
    def interpolate(self, val0, val1):
        """Interpolates the current values to obtain a new value."""
        return self._interpolate(val0, val1)

    @dispatch(Real, Real, str)
    def interpolate(self, val0, val1, method=INTERP2_METHOD):
        """Interpolates the current values to obtain a new value."""
        return self._interpolate(val0, val1, method)

    def _interpolate(self, val0, val1, method=INTERP2_METHOD):
        methods = {
            "bilinear": self._bilinear_interp,
        }
        copy = self.clone()

        if val0 not in self.ax0 and val1 not in self.ax1:
            return methods[method](val0, val1)
        else:
            ind0 = bisect.bisect(copy.ax0, val0) - 1
            ind1 = bisect.bisect(copy.ax1, val1) - 1
            return copy, (ind0, ind1), self[ind0, ind1]

    def _bilinear_interp(self, val0, val1):
        copy = self.clone()
        new_ind0 = bisect.bisect(self.ax0, val0)
        new_ind1 = bisect.bisect(self.ax1, val1)
        copy.ax0 = np.insert(copy.ax0, new_ind0, val0)
        copy.ax1 = np.insert(copy.ax1, new_ind1, val1)
        copy.values = np.insert(
            np.insert(copy.values, new_ind0, 0, 0), new_ind1, 0, 1)
        val_shape = copy.values.shape

        copy.values[new_ind0, new_ind1] = self._bilinear_interp_point(
            copy, new_ind0, new_ind1, val0, val1)

        for i in range(new_ind0):
            copy.values[i, new_ind1] = self._interp_side_neighbors(
                copy, i, new_ind1, copy.ax0[i], val1, axis=1)
        for i in range(new_ind1 + 1, val_shape[0]):
            copy.values[i, new_ind1] = self._interp_side_neighbors(
                copy, i, new_ind1, copy.ax0[i], val1, axis=1)

        for j in range(new_ind1):
            copy.values[new_ind0, j] = self._interp_side_neighbors(
                copy, new_ind0, j, val0, copy.ax1[j], axis=0)
        for j in range(new_ind1 + 1, val_shape[1]):
            copy.values[new_ind0, j] = self._interp_side_neighbors(
                copy, new_ind0, j, val0, copy.ax1[j], axis=0)

        return copy, (new_ind0, new_ind1), copy[new_ind0, new_ind1]

    def _bilinear_interp_point(self, copy, new_ind0, new_ind1, val0, val1):
        # We calculate all the required indices
        x0_error = False
        x1_error = False
        y0_error = False
        y1_error = False

        try:
            x0 = copy.ax0[new_ind0 - 1]
        except IndexError:
            x0_error = True
            x0 = copy.ax0[0]
        try:
            y0 = copy.ax1[new_ind1 - 1]
        except IndexError:
            y0_error = True
            y0 = copy.ax1[0]

        try:
            x1 = copy.ax0[new_ind0 + 1]
        except IndexError:
            x1_error = True
            x1 = copy.ax0[-1]
        try:
            y1 = copy.ax1[new_ind1 + 1]
        except IndexError:
            y1_error = True
            y1 = copy.ax1[-1]

        ind0 = 1 if x0_error else new_ind0 - 1
        ind1 = 1 if y0_error else new_ind1 - 1
        f00 = copy.values[ind0, ind1]

        ind0 = 1 if x0_error else new_ind0 - 1
        ind1 = -2 if y1_error else new_ind1 - 1
        f01 = copy.values[ind0, ind1]

        ind0 = -2 if x1_error else new_ind0 - 1
        ind1 = 1 if y0_error else new_ind1 - 1
        f10 = copy.values[ind0, ind1]

        ind0 = -2 if x1_error else new_ind0 - 1
        ind1 = -2 if y1_error else new_ind1 - 1
        f11 = copy.values[ind0, ind1]

        # With them, we interpolate in the x direction
        fx0 = f00 * (x1 - val0) / (x1 - x0) + f10 * (val0 - x0) / (x1 - x0)
        fx1 = f01 * (x1 - val0) / (x1 - x0) + f11 * (val0 - x0) / (x1 - x0)

        # Now we interpolate in the y direction
        return fx0 * (y1 - val1) / (y1 - y0) + fx1 * (val1 - y0) / (y1 - y0)

    def _interp_side_neighbors(self, copy, new_ind0, new_ind1, val0, val1, axis=0):
        if axis == 0:
            x0_error = False
            x1_error = False

            try:
                x0 = copy.ax0[new_ind0 - 1]
            except IndexError:
                x0_error = True
                x0 = copy.ax0[0]

            try:
                x1 = copy.ax0[new_ind0 + 1]
            except IndexError:
                x1_error = True
                x1 = copy.ax0[-1]

            ind0 = 1 if x0_error else new_ind0 - 1
            f0 = copy.values[ind0, new_ind1]

            ind0 = -2 if x1_error else new_ind0 + 1
            f1 = copy.values[ind0, new_ind1]
            
            # Linearly interpolates
            return f0 + (f1 - f0) * (val0 - x0) / (x1 - x0)
        elif axis == 1:
            y0_error = False
            y1_error = False

            try:
                y0 = copy.ax1[new_ind1 - 1]
            except IndexError:
                y0_error = True
                y0 = copy.ax1[0]

            try:
                y1 = copy.ax1[new_ind1 + 1]
            except IndexError:
                y1_error = True
                y1 = copy.ax0[-1]

            ind1 = 1 if y0_error else new_ind1 - 1
            f0 = copy.values[new_ind0, ind1]

            ind1 = -2 if y1_error else new_ind1 + 1
            f1 = copy.values[new_ind0, ind1]
            
            # Linearly interpolates
            return f0 + (f1 - f0) * (val1 - y0) / (y1 - y0)

    def unpack(self):
        """Unpacks the signal into three arrays. If used for its
        intended purpose, should be unpacked with *.
        """
        return self.ax0, self.ax1, self.values

    def apply_function(self, func, *args, **kwargs):
        """Applies a function to the values of the signal.

        Parameters
        ----------
        func : function
            Function to apply to the signal.
        """
        copy = self.clone()
        copy.values = np.array([func(x, *args, **kwargs) for x in copy.values])
        return copy

    def export_to_file(self, filename: str, *args, **kwargs):
        """Exports the one dimensional signal to the given file.

        Parameters
        ----------
        filename : str
            String corrresponding to the file.

        Raises
        ------
        ValueError
            If the filename is empty (e.g trying to export to the file ".csv").
        """
        extension = filename.split(".")[-1]
        if extension == filename:
            raise ValueError()
        Signal2.handlers[extension].export_signal2(
            filename, self, *args, **kwargs)

    def ax0_sampling_freq(self) -> float:
        """Calculates the sampling frequency of `ax0` in hertz, assuming
        it is constant.
        """
        sf = 1 / (self.ax0[1] - self.ax0[0])
        return sf if sf > 0 else 0

    def ax1_sampling_freq(self) -> float:
        """Calculates the sampling frequency of `ax1` in hertz, assuming
        it is constant.
        """
        sf = 1 / (self.ax1[1] - self.ax1[0])
        return sf if sf > 0 else 0

    def ax0_span(self) -> float:
        """Gets the span of the first axis."""
        return self.ax0[-1] - self.ax0[0]

    def ax1_span(self) -> float:
        """Gets the span of the second axis."""
        return self.ax1[-1] - self.ax1[0]

    def apply_kernel(self, kernel: np.ndarray, flip=False, oob=KERNEL_OOB) -> Signal2:
        """Applies a kernel over the signal. This process is also known
        as image convolution.

        Parameters
        ----------
        kernel : np.ndarray
            Matrix of the kernel to apply to the signal.
        flip : bool, optional
            Wheter to flip the kernel or not, by default False.
        oob : str, optional
            Specifier for how to handle values outside of the bounds of
            the signal, by default KERNEL_OOB.

        Returns
        -------
        Signal2
            Signal after applying the kernel.
        """
        return math_lib.apply_kernel(self, kernel, flip, oob)

    def transpose(self) -> Signal2:
        """Transposes the signal by interchanging `ax0` and `ax1`, and
        taking the transpose of `values`.

        Returns
        -------
        Signal2
            Transposed signal.
        """
        copy = self.clone()
        copy.ax0, copy.ax1 = copy.ax1, copy.ax0
        copy.values = copy.values.T
        assert np.shape(copy.values) == (
            len(copy.ax0), len(copy.ax1)), "Something went wrong."
        return copy

    def contourf(self):
        """Unpacks the signal in a way that the function `contourf`
        within the module `matplotlib.pyplot` can easily understand.
        If used for this purpose, should be called with * (e.g, if
        you want to plot the signal `sign`, then you would call
        `plt.contourf(*sign.contourf())`).

        For this, it returns both axes and the values (like the
        `unpack` method), except that the values are transposed.

        Returns
        -------
        np.ndarray, np.ndarray, np.ndarray
            Attributes `ax0`, `ax1` and `values` (this last one is
            transposed).
        """
        return self.ax0, self.ax1, self.values.T

    def half(self, axis=1, first=False):
        """Gets half of the signal.

        Which half to take can be specified using the `axis` and `first`
        parameters. `axis` tells the program in which direction to make
        the cut (axis 0 is row-wise, and axis 1 is column-wise), while
        `first` indicates whether to take the first half or second half.

        Parameters
        ----------
        axis : int, optional
            Direction in which to make the cut, by default 1. `0` is
            row-wise, `1` is column-wise.
        first : bool, optional
            Whether to take the first or second half, by default False.

        Returns
        -------
        Signal2
            Signal cut in half.
        """
        ax_handlers = {
            0: self._half_0,
            1: self._half_1,
        }
        return ax_handlers[axis](first)

    def _half_0(self, first=False):
        copy = self.clone()
        c_shape = copy.shape()
        half_val = int(c_shape[0] / 2)
        if first:
            copy.ax0 = copy.ax0[:half_val]
            copy.values = copy.values[:half_val, :]
        else:
            copy.ax0 = copy.ax0[half_val:]
            copy.values = copy.values[half_val:, :]
        return copy

    def _half_1(self, first=False):
        copy = self.clone()
        c_shape = copy.shape()
        half_val = int(c_shape[1] / 2)
        if first:
            copy.ax1 = copy.ax1[:half_val]
            copy.values = copy.values[:, :half_val]
        else:
            copy.ax1 = copy.ax1[half_val:]
            copy.values = copy.values[:, half_val:]
        return copy
