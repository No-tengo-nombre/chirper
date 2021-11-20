from signpy.sgn.signal import COS, HEAVISIDE
from signpy.modulation import Modulator
from signpy.config import AM_MODULATION, HERTZ, SSB_UPPER
from signpy.transforms.fourier import Fourier

class Modulator_AM(Modulator):
    def __init__(self, carrier_freq, carrier_amp):
        super().__init__(carrier_freq, carrier_amp)
        self.methods = {
            "dsbfc": self.dsbfc_modulation,
            "dsbsc": self.dsbsc_modulation,
            "ssb": self.ssb_modulation,
        }

    def apply(self, signal, method=AM_MODULATION, hertz=HERTZ):
        return self._modulate(
            method,
            signal=signal,
            carrier_freq=self.carrier_freq,
            carrier_amp=self.carrier_amp,
            hertz=hertz,
        )

    def _modulate(self, method, *args, **kwargs):
        mod_method = self.methods[method]
        return mod_method(*args, **kwargs)

    def dsbfc_modulation(self, signal, carrier_freq, carrier_amp, hertz=HERTZ):
        time = signal.time
        carrier = COS(time, carrier_freq, 1, hertz)
        return (carrier_amp + signal) * carrier

    def dsbsc_modulation(self, signal, carrier_freq, carrier_amp, hertz=HERTZ):
        time = signal.time
        carrier = COS(time, carrier_freq, carrier_amp, hertz)
        return carrier * signal

    def ssb_modulation(self, signal, carrier_freq, carrier_amp, hertz=HERTZ, upper=SSB_UPPER):
        time = signal.time
        carrier = COS(time, carrier_freq, carrier_amp, hertz)
        modulated = carrier * signal
        filter = HEAVISIDE(time, -carrier_freq, upper) + ((-1) ** int(not upper)) * HEAVISIDE(time, carrier_freq, False)

        mod_fourier = Fourier(modulated).calculate()
        
