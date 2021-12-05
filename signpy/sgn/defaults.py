import numpy as np

from signpy.config import HERTZ, NOISE_TYPE
from . import Signal1


########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
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
