from signpy.sgn import Signal1
from signpy.sgn.defaults import COS, HEAVISIDE
from signpy.config import AM_MODULATION, HERTZ, SSB_UPPER
from signpy.transforms import fourier, ifourier


def am_modulation(signal1 : Signal1, carrier_freq, carrier_amp, *args, method=AM_MODULATION, hertz=HERTZ, **kwargs) -> Signal1:
    """Applies AM modulation to the given one dimensional signal.

    The currently available methods for modulation are:
     - DSBFC : Double-SideBand Full Carrier.
     - DSBSC : Double-SideBand Suppressed Carrier.
     - SSB : Single-SideBand.

    Parameters
    ----------
    signal1 : Signal1
        One dimensional signal to modulate.
    carrier_freq : float
        Frequency of the carrier wave.
    carrier_amp : float
        Amplitude of the carrier wave.
    method : {"dsbfc", "dsbsc"}, optional
        Method used for the modulation, by default AM_MODULATION.
    hertz : bool, optional
        Whether the frequency is given in Hertz, by default HERTZ.

    Returns
    -------
    Signal1
        Modulated one dimensional signal.
    """
    return AM_MODULATION_METHODS[method](signal1, carrier_freq, carrier_amp, hertz, *args, **kwargs)

def dsbfc_modulation(signal1 : Signal1, carrier_freq, carrier_amp, hertz=HERTZ) -> Signal1:
    copy = signal1.clone()
    axis = copy.axis
    carrier = COS(axis, carrier_freq, 1, hertz)
    return (carrier_amp + copy) * carrier

def dsbsc_modulation(signal1 : Signal1, carrier_freq, carrier_amp, hertz=HERTZ) -> Signal1:
    copy = signal1.clone()
    axis = copy.axis
    carrier = COS(axis, carrier_freq, carrier_amp, hertz)
    return carrier * copy

def ssb_modulation(signal1 : Signal1, carrier_freq, carrier_amp, hertz=HERTZ, upper=SSB_UPPER) -> Signal1:
    return signal1
    # time = signal.time
    # carrier = COS(time, carrier_freq, carrier_amp, hertz)
    # modulated = carrier * signal
    # # filter = HEAVISIDE(time, -carrier_freq, upper) + ((-1) ** int(not upper)) * HEAVISIDE(time, carrier_freq, False)
    # if upper:
    #     filter = HEAVISIDE(time, -carrier_freq, True) + HEAVISIDE(time, carrier_freq)
    # else:
    #     filter = HEAVISIDE(time, -carrier_freq) - HEAVISIDE(time, carrier_freq)
    # mod_fourier = Fourier(modulated).calculate() * filter
    # return InverseFourier(mod_fourier).calculate()

AM_MODULATION_METHODS = {
    "dsbfc": dsbfc_modulation,
    "dsbsc": dsbsc_modulation,
    "ssb": ssb_modulation,
}
