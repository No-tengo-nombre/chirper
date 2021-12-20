import numpy as np

from signpy.sgn import Signal1
from signpy.config import PM_MODULATION, HERTZ


def pm_modulation(signal1 : Signal1, carrier_freq, carrier_amp, method=PM_MODULATION, hertz=HERTZ) -> Signal1:
    """Applies PM modulation to the given one dimensional signal.

    The currently available methods for modulation are:
     - Traditional

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to modulate.
    carrier_freq : float
        Frequency of the carrier wave.
    carrier_amp : float
        Amplitude of the carrier wave.
    method : {"trad"}, optional
        Method used for the modulation, by default PM_MODULATION.
    hertz : bool, optional
        Whether the frequency is given in Hertz, by default HERTZ.

    Returns
    -------
    Signal1
        Modulated one dimensional signal.
    """
    return PM_MODULATION_METHODS[method](signal1, carrier_freq, carrier_amp, hertz)

def trad_modulation(signal1 : Signal1, carrier_freq, carrier_amp, hertz):
    copy = signal1.clone()
    axis = copy.axis
    freq = 2 * np.pi * carrier_freq if hertz else carrier_freq
    values = carrier_amp * np.sin(freq * axis + copy.values)
    return Signal1(axis, values)
        
PM_MODULATION_METHODS = {
    "traditional": trad_modulation,
}
