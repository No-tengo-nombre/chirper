from signpy.exceptions import DimensionError
from signpy.config import INTERPOLATION_METHOD, NOISE_TYPE, HERTZ

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
        if isinstance(signal, float) or isinstance(signal, int):                # Ugly code
            return Signal(self.time, self.values + signal)
        return Signal(*self._do_bin_operation(signal, operator.add))

    def __sub__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):                # Ugly code
            return Signal(self.time, self.values - signal)
        return Signal(*self._do_bin_operation(signal, operator.sub))

    def __mul__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):                # Ugly code
            return Signal(self.time, self.values * signal)
        return Signal(*self._do_bin_operation(signal, operator.mul))

    def __truediv__(self, signal):
        if isinstance(signal, float) or isinstance(signal, int):                # Ugly code
            return Signal(self.time, self.values / signal)
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
    def from_function(cls, time, func, *args, **kwargs):
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
        return cls(time, func(np.array(time), *args, **kwargs))

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

    def time_span(self):
        """Gets the time span of the signal"""
        return self.time[-1] - self.time[0]

    def half(self, first=True):
        """Gets half of the signal"""
        return self[:self.time_span() / 2] * 2 if first else self[self.time_span() / 2:] * 2

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
        self.values = np.array([func(t, x, *args, **kwargs) for t, x in zip(self.time, self.values)])
        return self

    def convolute(self, signal):
        """Convolute this signal with another."""
        copy_signal = Signal(self.time, self.values)
        return copy_signal.apply_function(self._conv_helper, signal)

    def _conv_helper(self, a, signal):
        sum = 0
        for k in signal.time:
            sum += a * signal[k]
        return sum

    def shift(self, value):
        """Shifts the time axis by `value`."""
        self.time += value

    def real_part(self):
        values = np.real(self.values)
        return Signal(self.time, values)

    def imag_part(self):
        values = np.imag(self.values)
        return Signal(self.time, values)

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||| DEFAULT SIGNALS ||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class SQUARE(Signal):
    """Square signal"""
    def __init__(self, time, freq, amp, rads=False, phase=0):
        """Generates a square signal centered at 0.

        Parameters
        ----------
        time : array like
            Array for the time.
        freq : float
            Frequency for the square wave.
        amp : float
            Amplitude of the wave.
        rads : bool
            Whether the frequency is given in radians or hertz, by default False.
        phase : float, optional
            Phase of the wave, by default 0.
        """
        super().__init__(time, self._generate(time, freq, amp, rads, phase))

    @staticmethod
    def _generate(time, freq, amp, rads, phase):
        real_freq = freq if rads else 2 * np.pi * freq
        real_phase = phase if rads else 2 * np.pi * phase
        return amp * np.array(list(map(lambda x: int(x >= 0), np.sin(real_freq * time + real_phase))))


class SIN(Signal):
    """Sinusoidal signal"""
    def __init__(self, time, freq, amp, hertz=HERTZ, phase=0):
        """Generates a sinusoidal signal centered at 0.

        Parameters
        ----------
        time : array like
            Array for the time.
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
        super().__init__(time, self._generate(time, freq, amp, hertz, phase))

    @staticmethod
    def _generate(time, freq, amp, hertz, phase):
        real_freq = 2 * np.pi * freq if hertz else freq
        real_phase = 2 * np.pi * phase if hertz else phase
        return amp * np.sin(real_freq * time + real_phase)


class COS(Signal):
    """Cosine signal"""
    def __init__(self, time, freq, amp, hertz=HERTZ, phase=0):
        """Generates a cosine signal centered at 0.

        Parameters
        ----------
        time : array like
            Array for the time.
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
        super().__init__(time, self._generate(time, freq, amp, hertz, phase))

    @staticmethod
    def _generate(time, freq, amp, hertz, phase):
        real_freq = 2 * np.pi * freq if hertz else freq
        real_phase = 2 * np.pi * phase if hertz else phase
        return amp * np.cos(real_freq * time + real_phase)


class NOISE(Signal):
    """Noise signal"""
    def __init__(self, time, std, add=True, noise_type=NOISE_TYPE):
        """Generates a noise signal.

        Parameters
        ----------
        time : array like
            Array for the time.
        std : float
            Standard deviation of the noise.
        add : bool, optional
            Whether the noise should be additive (with mean 0) or multiplicative (with mean 1), by default True.
        noise_type : {"gaussian"}, optional
            The type of noise to use, by default `NOISE_TYPE` defined in the config file (gaussian).
        """
        if noise_type == "gaussian":
            super().__init__(time, self._generate_gaussian(time, std, add))

    @staticmethod
    def _generate_gaussian(time, std, add):
        mean = 0 if add else 1
        return np.random.normal(mean, std, len(time))


class HEAVISIDE(Signal):
    """Heaviside step function centered at a certain time."""
    def __init__(self, time, point=0, inverted=False):
        """Creates a Heaviside step function.

        Parameters
        ----------
        time : array like
            Array for the time.
        point : float, optional
            Point to center the signal around (e.g if `point == 0` then the function would change values at 0), by
            default 0.
        inverted : bool, optional
            Whether to invert the signal or not. If true, the signal would be 1 and switch to 0 after the point. By
            default False.
        """
        if inverted:
            values = list(map(lambda x: int(x <= point), time))
        else:
            values = list(map(lambda x: int(x >= point), time))
        super().__init__(time, values)


class IMPULSE(Signal):
    """Discrete impulse/delta function centered at 0."""
    def __init__(self, time, value=1.0):
        """Creates a discrete impulse centered at 0, with value `value`.

        Parameters
        ----------
        time : array like
            Array for the time.
        value : float, optional
            Value for the impulse to take at 0, by default 1.0
        """
        super().__init__(time, value * self._init_helper(time))
        
    def _init_helper(self, time):
        values = []
        for i, t in enumerate(time):
            if t < 0.0:
                values.append(0.0)
            else:
                values.append(1.0 if t == 0 or time[i - 1] < 0 else 0.0)
        return values


class CONSTANT(Signal):
    """Constant signal."""
    def __init__(self, time, value=1.0):
        """Creates a constant signal.

        Parameters
        ----------
        time : array like
            Array for the time.
        value : float or complex, optional
            Value to use for the constant, by default 1.0.
        """
        super().__init__(time, [value for t in time])
