import numpy as np

from chirper.sgn import Signal1
from chirper.config import HERTZ, FM_MODULATION


def fm_modulation(signal1: Signal1, *args, method=FM_MODULATION, hertz=HERTZ, **kwargs) -> Signal1:
    return FM_MODULATION_METHODS[method](signal1, *args, hertz, **kwargs)


def _trad_modulation(signal1: Signal1, carrier_freq, carrier_amp, const, hertz=HERTZ) -> Signal1:
    copy = signal1.clone()
    axis = copy.axis
    freq = 2 * np.pi * carrier_freq if hertz else carrier_freq
    values = carrier_amp * np.cos((freq + const * copy.values) * axis)
    return Signal1(axis, values)


FM_MODULATION_METHODS = {
    "trad": _trad_modulation,
}
