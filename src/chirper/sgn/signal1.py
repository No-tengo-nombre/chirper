"""One dimensional signal"""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import bisect
import operator
from tqdm import tqdm
from numbers import Number, Real
from multipledispatch import dispatch

from chirper.exceptions import DimensionError
from chirper.config import CONVOLUTION_METHOD, INTERP1_METHOD, CROSS_CORRELATION_METHOD
from chirper.utils import math_lib
from chirper.sgn.handlers import handler_csv, handler_json, handler_wav
from chirper.sgn.signal import Signal


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
        axis = samp_period * np.arange(len(vals)) - sp
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

    def is_valid(self):
        return self.axis.shape == self.values.shape
