from signpy.sgn import Signal1
from signpy.sgn.defaults import COS, HEAVISIDE
from signpy.config import AM_MODULATION, HERTZ, SSB_UPPER
from signpy.transforms import fourier, ifourier


def am_modulation(signal1 : Signal1, carrier_freq, carrier_amp, method=AM_MODULATION, hertz=HERTZ) -> Signal1:
    """Applies AM modulation to the given one dimensional signal.

    The currently available methods for modulation are:
     - DSBFC : Double-SideBand Full Carrier.
     - DSBSC : Double-SideBand Suppressed Carrier.

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
    return AM_MODULATION_METHODS[method](signal1, carrier_freq, carrier_amp, hertz)

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
    pass
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

# class Modulator_AM(Modulator):
#     def __init__(self, carrier_freq, carrier_amp):
#         super().__init__(carrier_freq, carrier_amp)
#         self.methods = {
#             "dsbfc": self.dsbfc_modulation,
#             "dsbsc": self.dsbsc_modulation,
#             "ssb": self.ssb_modulation,
#         }

#     def apply(self, signal : Signal1, method=AM_MODULATION, hertz=HERTZ):
#         return self.methods[method](signal, self.carrier_freq, self.carrier_amp, hertz)

#     def dsbfc_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz=HERTZ):
#         time = signal.time
#         carrier = COS(time, carrier_freq, 1, hertz)
#         # return (carrier_amp + signal) * carrier
#         return COS(time, carrier_freq, carrier_amp, hertz) + signal * carrier

#     def dsbsc_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz=HERTZ):
#         time = signal.time
#         carrier = COS(time, carrier_freq, carrier_amp, hertz)
#         return carrier * signal

#     def ssb_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz=HERTZ, upper=SSB_UPPER):
#         pass
#         # time = signal.time
#         # carrier = COS(time, carrier_freq, carrier_amp, hertz)
#         # modulated = carrier * signal
#         # # filter = HEAVISIDE(time, -carrier_freq, upper) + ((-1) ** int(not upper)) * HEAVISIDE(time, carrier_freq, False)
#         # if upper:
#         #     filter = HEAVISIDE(time, -carrier_freq, True) + HEAVISIDE(time, carrier_freq)
#         # else:
#         #     filter = HEAVISIDE(time, -carrier_freq) - HEAVISIDE(time, carrier_freq)
#         # mod_fourier = Fourier(modulated).calculate() * filter
#         # return InverseFourier(mod_fourier).calculate()
