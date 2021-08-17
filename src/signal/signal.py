from src.exceptions import DimensionError
from src import INTERPOLATION_METHOD

import numpy as np
import bisect
import operator


class Signal:
    """Class representing a signal object."""

    def __init__(self, time, values):
        """Creates a signal from a time and a values list.

        Parameters
        ----------
        time : array_like
            List of elements representing the independent variable
            (usually time).
        values : array_like
            List of elements representing the dependent variable for
            each time.
        """
        if len(time) != len(values):
            raise DimensionError("The dimensions of the values do not match.")
        self.time = np.array(time)
        self.values = np.array(values)

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Slices the indices based on the given key, then intersects them to get all the indices
            indices1 = np.where(key.start <= self.time if key.start else self.time)
            indices2 = np.where(self.time <= key.stop if key.stop else self.time)
            indices = np.intersect1d(indices1, indices2)
            return Signal(
                [self.time[i] for i in indices],
                [self.values[i] for i in indices]
            )
        index = np.where(self.time == key)[0]
        return self.values[index]

    def __add__(self, signal):
        return Signal(*self._do_bin_operation(signal, operator.add))

    def __sub__(self, signal):
        return Signal(*self._do_bin_operation(signal, operator.sub))

    def __mul__(self, signal):
        return Signal(*self._do_bin_operation(signal, operator.mul))

    def __truediv__(self, signal):
        return Signal(*self._do_bin_operation(signal, operator.truediv))

    def __eq__(self, signal):
        return np.array_equal(self.time, signal.time) and np.array_equal(self.values, signal.values)

    def __str__(self):
        return f"{self.time}\n{self.values}"

    def __abs__(self):
        return Signal(self.time, list(map(operator.abs, self.values)))

    def __len__(self):
        return len(self.time)

    def _do_bin_operation(self, signal, operation):
        # Joins the times of both signals
        time_list = np.union1d(self.time, signal.time)
        time_list.sort()

        new_values = np.array([])
        for t in time_list:
            # Interpolates the values
            y1 = self.interp(t)[1]
            y2 = signal.interp(t)[1]
            # Operates using the interpolated values
            new_values = np.append(new_values, operation(y1, y2))
        return time_list, new_values

    @classmethod
    def from_function(cls, time, func):
        """Creates a signal from a time list and a function.

        The function is applied to each element in the time series, so
        if the function f(x) = x**2 is given as a parameter to the time
        series [1, 2, 3, 4], the values should be [1, 4, 9, 16].

        Parameters
        ----------
        time : array_like
            List of elements representing the independent variable
            (usually time).
        func : function
            Function to apply to each element.
        """
        return cls(time, func(np.array(time)))

    def interpolate(self, time, method):
        """Interpolates the current values to obtain a new value.

        Parameters
        ----------
        time : float
            Time to apply the interpolation to.
        method : {"linear"}
            Method used for the interpolation.
        Returns
        -------
        New index and value.
        """
        if time not in self.time:
            # Inserts the new time into the time series
            new_index = bisect.bisect(self.time, time)
            self.time = np.insert(self.time, new_index, time)

            if method == "linear":
                ta = self.time[new_index - 1]
                xa = self.values[new_index - 1]
                try:
                    tb = self.time[new_index + 1]
                    xb = self.values[new_index + 1]
                except IndexError:
                    # This code is reached if the program tries to interpolate points out of the range.
                    # In this case, it simply interpolates using the last value.
                    tb = self.time[-1]
                    xb = self.values[-1]

                # Linearly interpolates
                new_value = xa + (xb - xa) * (time - ta) / (tb - ta)
                self.values = np.insert(self.values, new_index, new_value)
                return new_index, new_value
        else:
            index = bisect.bisect(self.time, time) - 1
            return index, self.values[index]

    def interpl(self, time):
        """Applies a linear interpolation to obtain a new value.

        Parameters
        ----------
        time : float
            Time to apply the interpolation to.

        Returns
        -------
        New index and value.
        """
        return self.interpolate(time, "linear")

    def interp(self, time):
        """Interpolates the current values to obtain a new value using the default method given by
        `INTERPOLATION_METHOD` (by default "linear") defined in "src.__init__.py".
        
        Parameters
        ----------
        time : float
            Time to apply the interpolation to.

        Returns
        -------
        New index and value
        """
        method = INTERPOLATION_METHOD
        return self.interpolate(time, method)

    def unpack(self):
        """Unpacks the signal into two arrays. If used for its intended purpose, should be unpacked with *."""
        return self.time, self.values
