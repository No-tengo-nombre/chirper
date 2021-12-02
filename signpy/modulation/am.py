from signpy.sgn.signal import COS, HEAVISIDE, Signal1
from signpy.modulation import Modulator
from signpy.config import AM_MODULATION, HERTZ, SSB_UPPER
from signpy.transforms.fourier import Fourier, InverseFourier


class Modulator_AM(Modulator):
    def __init__(self, carrier_freq, carrier_amp):
        super().__init__(carrier_freq, carrier_amp)
        self.methods = {
            "dsbfc": self.dsbfc_modulation,
            "dsbsc": self.dsbsc_modulation,
            "ssb": self.ssb_modulation,
        }

    def apply(self, signal : Signal1, method=AM_MODULATION, hertz=HERTZ):
        return self.methods[method](signal, self.carrier_freq, self.carrier_amp, hertz)

    def dsbfc_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz=HERTZ):
        time = signal.time
        carrier = COS(time, carrier_freq, 1, hertz)
        # return (carrier_amp + signal) * carrier
        return COS(time, carrier_freq, carrier_amp, hertz) + signal * carrier

    def dsbsc_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz=HERTZ):
        time = signal.time
        carrier = COS(time, carrier_freq, carrier_amp, hertz)
        return carrier * signal

    def ssb_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz=HERTZ, upper=SSB_UPPER):
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
