"""Two dimensional signal"""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import bisect
import operator
from numbers import Number, Real
from multipledispatch import dispatch

from chirper.exceptions import DimensionError
from chirper.config import INTERP2_METHOD, KERNEL_OOB
from chirper.utils import math_lib
from chirper.sgn.handlers import handler_img
from chirper.sgn.signal import Signal


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

    # TODO: Fix the REALLY slow speed when operating signals
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
        If used for this purpose, should be called with *. 

        For example, if you want to plot the signal `sign`, then you
        would call
        >>> plt.contourf(*sign.contourf())

        For this, it returns both axes and the values (like the
        `unpack` method), except that the values are transposed.

        Returns
        -------
        np.ndarray, np.ndarray, np.ndarray
            Attributes `ax0`, `ax1` and `values` (this last one is
            transposed).
        """
        return self.ax0, self.ax1, self.values.T

    def imshow(self):
        """Unpacks the signal in a way that the function `imshow` within
        the module `matplotlib.pyplot` can easily understand, in such a
        way that the axes are automatically reshaped to fit the real
        axes of the signal. If used for this purpose, should be
        called with **.

        For example, if you want to plot the signal `sign`, then
        you would call
        >>> plt.imshow(**sign.imshow())

        Returns
        -------
        dict
            Dictionary with the appropiate keywords for `plt.imshow`.
        """
        copy = self.clone()
        xmin, xmax = copy.ax0[0], copy.ax0[-1]
        ymin, ymax = copy.ax1[0], copy.ax1[-1]
        return {"X": copy.values.T, "extent": [xmin, xmax, ymin, ymax]}

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

    def is_valid(self):
        return self.values.shape == (len(self.ax0), len(self.ax1))

    def get_ax0(self, start=None, stop=None) -> Signal2:
        copy = self.clone()
        if start is None:
            start_index = 0
        else:
            start_index = bisect.bisect(copy.ax0, start)

        if stop is None:
            stop_index = -1
        else:
            stop_index = bisect.bisect(copy.ax0, stop)

        copy.ax0 = copy.ax0[start_index:stop_index]
        copy.values = copy.values[start_index:stop_index, :]
        return copy

    def get_ax1(self, start=None, stop=None) -> Signal2:
        copy = self.clone()
        if start is None:
            start_index = 0
        else:
            start_index = bisect.bisect(copy.ax1, start)

        if stop is None:
            stop_index = -1
        else:
            stop_index = bisect.bisect(copy.ax1, stop)

        copy.ax1 = copy.ax1[start_index:stop_index]
        copy.values = copy.values[:, start_index:stop_index]
        return copy
