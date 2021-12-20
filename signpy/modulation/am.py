from signpy.sgn import Signal1
from signpy.sgn.defaults import COS, SIN
from signpy.config import AM_MODULATION, HERTZ, SSB_UPPER
from signpy.transforms import hilbert


def am_modulation(signal1: Signal1, *args, method=AM_MODULATION, hertz=HERTZ, **kwargs) -> Signal1:
    """Applies AM modulation to the given one dimensional signal.

    The currently available methods for modulation are:
     - DSBFC : Double-SideBand Full Carrier.
     - DSBSC : Double-SideBand Suppressed Carrier.
     - SSB : Single-SideBand.
     - USB : Upper-SideBand, an alias for calling SSB with `upper=True`.
     - LSB : Lower-SideBand, an alias for calling SSB with `upper=False`.

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to modulate.
    carrier_freq : float
        Frequency of the carrier wave.
    carrier_amp : float
        Amplitude of the carrier wave. Only for DSBFC and DSBSC.
    method : {"dsbfc", "dsbsc", "ssb", "usb", "lsb"}, optional
        Method used for the modulation, by default AM_MODULATION.
    hertz : bool, optional
        Whether the frequency is given in Hertz, by default HERTZ.

    Returns
    -------
    Signal1
        Modulated one dimensional signal.
    """
    return AM_MODULATION_METHODS[method](signal1, *args, hertz, **kwargs)


def _dsbfc_modulation(signal1: Signal1, carrier_freq, carrier_amp, hertz=HERTZ) -> Signal1:
    copy = signal1.clone()
    axis = copy.axis
    carrier = COS(axis, carrier_freq, 1, hertz)
    return (carrier_amp + copy) * carrier


def _dsbsc_modulation(signal1: Signal1, carrier_freq, carrier_amp, hertz=HERTZ) -> Signal1:
    copy = signal1.clone()
    axis = copy.axis
    carrier = COS(axis, carrier_freq, carrier_amp, hertz)
    return carrier * copy


def _ssb_modulation(signal1: Signal1, carrier_freq, hertz=HERTZ, upper=SSB_UPPER) -> Signal1:
    x = signal1.clone()
    axis = x.axis
    x_h = hilbert.h1(x)
    return x * COS(axis, carrier_freq, 1, hertz) + ((-1) ** int(upper)) * x_h * SIN(axis, carrier_freq, 1, hertz)


def _usb_modulation(signal1: Signal1, carrier_freq, hertz=HERTZ) -> Signal1:
    return _ssb_modulation(signal1, carrier_freq, hertz, True)


def _lsb_modulation(signal1: Signal1, carrier_freq, hertz=HERTZ) -> Signal1:
    return _ssb_modulation(signal1, carrier_freq, hertz, False)


AM_MODULATION_METHODS = {
    "dsbfc": _dsbfc_modulation,
    "dsbsc": _dsbsc_modulation,
    "ssb": _ssb_modulation,
    "usb": _usb_modulation,
    "lsb": _lsb_modulation,
}
