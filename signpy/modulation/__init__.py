from signpy.exceptions import InvalidModulation

class Modulator:
    """Modulator object."""
    def __init__(self, carrier_freq, carrier_amp):
        """Create an empty modulator. Generally, you probably don't want
        to call this function.

        Parameters
        ----------
        carrier_freq : float
            Frequency of the carrier signal.
        carrier_amp : float
            Amplitude of the carrier signal.
        """
        self.carrier_freq = carrier_freq
        self.carrier_amp = carrier_amp

    def apply(self, signal, method=None):
        """Applies the modulator to a given signal.

        Parameters
        ----------
        signal : sgn.signal.Signal
            Signal to modulate.
        method : str, optional
            Desired method for the modulation process, by default None.

        Raises
        ------
        InvalidModulation
            If the modulation could not be applied, or if trying to apply
            an empty modulator.
        """
        raise InvalidModulation("Can not apply empty modulator.")
