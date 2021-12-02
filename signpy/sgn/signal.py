from signpy.exceptions import DimensionError
from signpy.config import INTERPOLATION_METHOD, NOISE_TYPE, HERTZ
from signpy import math
from signpy import sgn
from signpy.sgn import handler

import numpy as np
import bisect
import operator


class Signal1(sgn.Signal):
    """Class representing a signal object."""
    handlers = {
        "csv": handler.HandlerCSV,
        "json": handler.HandlerJSON,
    }

    def __init__(self, axis, values):
        """Creates a signal from an independent axis and a values list.

        Parameters
        ----------
        axis : array_like
            List of elements representing the independent variable
            (usually time).
        values : array_like
            List of elements representing the dependent variable for
            each axis element.
        """
        if len(axis) != len(values):
            raise DimensionError("The dimensions of the values do not match.")
        self.axis = np.array(axis)
        self.values = np.array(values)
        # self.exporters = {
        #     "csv": exporter.ExporterCSV
        # }

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Slices the indices based on the given key, then intersects them to get all the indices
            indices1 = np.where(key.start <= self.axis if key.start else self.axis)
            indices2 = np.where(self.axis <= key.stop if key.stop else self.axis)
            indices = np.intersect1d(indices1, indices2)
            return Signal1(
                [self.axis[i] for i in indices],
                [self.values[i] for i in indices]
            )
        index = np.where(self.axis == key)[0]
        return self.values[index]

    def __add__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):
            return Signal1(self.axis, self.values + signal)
        return Signal1(*self._do_bin_operation(signal, operator.add))

    def __sub__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):
            return Signal1(self.axis, self.values - signal)
        return Signal1(*self._do_bin_operation(signal, operator.sub))

    def __mul__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):
            return Signal1(self.axis, self.values * signal)
        return Signal1(*self._do_bin_operation(signal, operator.mul))

    def __truediv__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):
            return Signal1(self.axis, self.values / signal)
        return Signal1(*self._do_bin_operation(signal, operator.truediv))

    def __eq__(self, signal):
        return np.array_equal(self.axis, signal.axis) and np.array_equal(self.values, signal.values)

    def __str__(self):
        return f"{self.axis}\n{self.values}"

    def __abs__(self):
        return Signal1(self.axis, list(map(operator.abs, self.values)))

    def __len__(self):
        return len(self.axis)

    def _do_bin_operation(self, signal, operation):
        # Joins the axiss of both signals
        axis_list = np.union1d(self.axis, signal.axis)
        axis_list.sort()

        new_values = np.array([])
        for t in axis_list:
            # Interpolates the values
            y1 = self.interp(t)[1]
            y2 = signal.interp(t)[1]
            # Operates using the interpolated values
            new_values = np.append(new_values, operation(y1, y2))
        return axis_list, new_values

    @classmethod
    def from_function(cls, axis: np.ndarray, func: function, *args, **kwargs):
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
    def from_file(cls, filename: str):
        try:
            name, extension = filename.split(".")
            Signal1.handlers[extension].export_signal1(filename, cls)
        except ValueError:
            print("Name must not contain dots.")
        except Exception:
            print("An unexpected error has ocurred.")

    def interpolate(self, element, method: str):
        """Interpolates the current values to obtain a new value.

        Parameters
        ----------
        element : float
            Element to apply the interpolation to.
        method : {"linear"}
            Method used for the interpolation.
        Returns
        -------
        copy : Signal1
            Copy of the signal with the new value interpolated.
        index : int
            Index of the interpolated value.
        new_value : float
            Value of the interpolated value.
        """
        copy = self.clone()
        if element not in self.axis:
            # Inserts the new element into the axis
            new_index = bisect.bisect(self.axis, element)
            copy.axis = np.insert(copy.axis, new_index, element)

            if method == "linear":
                ta = copy.axis[new_index - 1]
                xa = copy.values[new_index - 1]
                try:
                    tb = copy.axis[new_index + 1]
                    xb = copy.values[new_index + 1]
                except IndexError:
                    # This code is reached if the program tries to interpolate points out of the range.
                    # In this case, it simply interpolates using the last value.
                    tb = copy.axis[-1]
                    xb = copy.values[-1]

                # Linearly interpolates
                new_value = xa + (xb - xa) * (element - ta) / (tb - ta)
                copy.values = np.insert(copy.values, new_index, new_value)
                return copy, new_index, new_value
        else:
            index = bisect.bisect(copy.axis, element) - 1
            return copy, index, self.values[index]

    def interpl(self, element):
        """Applies a linear interpolation to obtain a new value.

        Parameters
        ----------
        element : float
            Element to apply the interpolation to.

        Returns
        -------
        New index and value.
        """
        return self.interpolate(element, "linear")

    def interp(self, element):
        """Interpolates the current values to obtain a new value using the default method given by
        `INTERPOLATION_METHOD` (by default "linear") defined in "src.__init__.py".
        
        Parameters
        ----------
        element : float
            Element to apply the interpolation to.

        Returns
        -------
        New index and value
        """
        method = INTERPOLATION_METHOD
        return self.interpolate(element, method)

    def unpack(self):
        """Unpacks the signal into two arrays. If used for its intended purpose, should be unpacked with *."""
        return self.axis, self.values

    def span(self):
        """Gets the span of the signal"""
        return self.axis[-1] - self.axis[0]

    def half(self, first=True):
        """Gets half of the signal"""
        return self[:self.span() / 2] * 2 if first else self[self.span() / 2:] * 2

    def rect_smooth(self, factor):
        """Directly applies a rectangular smoothing to the signal.

        With this method the edges of the signal look a bit rough.

        Parameters
        ----------
        factor : int (odd)
            Smoothing factor.

        Returns
        -------
        Smooth signal (it also mutates the original signal).
        """
        if factor % 2 != 1 or factor <= 1:
            raise ValueError("The smoothing factor must be an odd number.")
        shift = int((factor - 1) / 2)
        self_len = len(self)
        new_values = self.values[0:1]               # Copies the first element

        # Smooths the first elements with the only possible elements
        for n in range(1, shift):
            arr = self.values[0:2 * n + 1]
            new_values = np.append(new_values, arr.sum() / (2 * n + 1))

        # Smooths the other elements using the given factor
        for n in range(shift, self_len - shift):
            arr = self.values[n - shift:n + shift + 1]
            new_values = np.append(new_values, arr.sum() / factor)

        # Smooths the last elements adapting the smoothing factor
        for n in range(self_len - shift, self_len):
            new_shift = self_len - n - 1
            arr = self.values[n - new_shift:self_len]
            new_values = np.append(new_values, arr.sum() / (2 * new_shift + 1))

        assert self_len == len(new_values), "There was an error during the smoothing."
        self.values = new_values
        return self

    def apply_function(self, func, *args, **kwargs):
        """Applies a function to the values of the signal.

        Parameters
        ----------
        func : function
            Function to apply to the signal.

        Returns
        -------
        Modified signal.
        """
        self.values = np.array([func(x, *args, **kwargs) for x in self.values])
        return self

    def apply_function_tuple(self, func, *args, **kwargs):
        self.values = np.array([func(t, x, *args, **kwargs) for t, x in zip(self.axis, self.values)])
        return self

    def convolute(self, sign):
        return math.convolute(self, sign)

    # def convolute(self, signal):
    #     """Convolute this signal with another."""
    #     copy_signal = Signal(self.axis, self.values)
    #     return copy_signal.apply_function(self._conv_helper, signal)

    # def _conv_helper(self, a, signal):
    #     sum = 0
    #     for k in signal.axis:
    #         sum += a * signal[k]
    #     return sum

    def shift(self, value):
        """Shifts the axis by `value`."""
        copy = self.clone()
        copy.axis += value
        return copy

    def real_part(self):
        values = np.real(self.values)
        return Signal1(self.axis, values)

    def imag_part(self):
        values = np.imag(self.values)
        return Signal1(self.axis, values)

    # def clone(self):
    #     return Signal1(self.axis, self.values)

    def conjugate(self):
        copy = self.copy()
        copy.values = copy.values.conjugate()
        return copy

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||| DEFAULT SIGNALS ||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class SQUARE(Signal1):
    """Square signal"""
    def __init__(self, axis, freq, amp, rads=False, phase=0):
        """Generates a square signal centered at 0.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        freq : float
            Frequency for the square wave.
        amp : float
            Amplitude of the wave.
        rads : bool
            Whether the frequency is given in radians or hertz, by default False.
        phase : float, optional
            Phase of the wave, by default 0.
        """
        super().__init__(axis, SQUARE._generate(axis, freq, amp, rads, phase))

    @staticmethod
    def _generate(axis, freq, amp, rads, phase):
        real_freq = freq if rads else 2 * np.pi * freq
        real_phase = phase if rads else 2 * np.pi * phase
        return amp * np.array(list(map(lambda x: int(x >= 0), np.sin(real_freq * axis + real_phase))))


class SIN(Signal1):
    """Sinusoidal signal"""
    def __init__(self, axis, freq, amp, hertz=HERTZ, phase=0):
        """Generates a sinusoidal signal centered at 0.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        freq : float
            Frequency for the wave.
        amp : float
            Amplitude of the wave.
        hertz : bool, optional
            If True then the frequency is assumed to be in hertz, if not
            then it is in radians, by default config.HERTZ.
        phase : float, optional
            Phase of the wave, by default 0.
        """
        super().__init__(axis, SIN._generate(axis, freq, amp, hertz, phase))

    @staticmethod
    def _generate(axis, freq, amp, hertz, phase):
        real_freq = 2 * np.pi * freq if hertz else freq
        real_phase = 2 * np.pi * phase if hertz else phase
        return amp * np.sin(real_freq * axis + real_phase)


class COS(Signal1):
    """Cosine signal"""
    def __init__(self, axis, freq, amp, hertz=HERTZ, phase=0):
        """Generates a cosine signal centered at 0.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        freq : float
            Frequency for the wave.
        amp : float
            Amplitude of the wave.
        hertz : bool, optional
            If True then the frequency is assumed to be in hertz, if not
            then it is in radians, by default config.HERTZ.
        phase : float, optional
            Phase of the wave, by default 0.
        """
        super().__init__(axis, COS._generate(axis, freq, amp, hertz, phase))

    @staticmethod
    def _generate(axis, freq, amp, hertz, phase):
        real_freq = 2 * np.pi * freq if hertz else freq
        real_phase = 2 * np.pi * phase if hertz else phase
        return amp * np.cos(real_freq * axis + real_phase)


class NOISE(Signal1):
    """Noise signal"""

    def __init__(self, axis, std, add=True, noise_type=NOISE_TYPE):
        """Generates a noise signal.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        std : float
            Standard deviation of the noise.
        add : bool, optional
            Whether the noise should be additive (with mean 0) or multiplicative (with mean 1), by default True.
        noise_type : {"gaussian"}, optional
            The type of noise to use, by default `NOISE_TYPE` defined in the config file (gaussian).
        """
        self.methods = {
            "gaussian" : NOISE._generate_gaussian,
        }
        # if noise_type == "gaussian":
        #     super().__init__(axis, NOISE._generate_gaussian(axis, std, add))
        super().__init__(axis, self.methods[noise_type](axis, std, add))

    @staticmethod
    def _generate_gaussian(axis, std, add):
        mean = 0 if add else 1
        return np.random.normal(mean, std, len(axis))


class HEAVISIDE(Signal1):
    """Heaviside step function centered at a certain point."""
    def __init__(self, axis, point=0, inverted=False):
        """Creates a Heaviside step function.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        point : float, optional
            Point to center the signal around (e.g if `point == 0` then the function would change values at 0), by
            default 0.
        inverted : bool, optional
            Whether to invert the signal or not. If true, the signal would be 1 and switch to 0 after the point. By
            default False.
        """
        if inverted:
            values = list(map(lambda x: int(x <= point), axis))
        else:
            values = list(map(lambda x: int(x >= point), axis))
        super().__init__(axis, values)


class IMPULSE(Signal1):
    """Discrete impulse/delta function centered at 0."""
    def __init__(self, axis, value=1.0):
        """Creates a discrete impulse centered at 0, with value `value`.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        value : float, optional
            Value for the impulse to take at 0, by default 1.0
        """
        super().__init__(axis, value * self._init_helper(axis))
        
    def _init_helper(self, axis):
        values = []
        for i, t in enumerate(axis):
            if t < 0.0:
                values.append(0.0)
            else:
                values.append(1.0 if t == 0 or axis[i - 1] < 0 else 0.0)
        return values


class CONSTANT(Signal1):
    """Constant signal."""
    def __init__(self, axis, value=1.0):
        """Creates a constant signal.

        Parameters
        ----------
        axis : array like
            Array for the axis.
        value : float or complex, optional
            Value to use for the constant, by default 1.0.
        """
        super().__init__(axis, [value for t in axis])
