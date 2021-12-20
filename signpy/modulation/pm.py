import numpy as np

from signpy.sgn import Signal1
from signpy.config import PM_MODULATION, HERTZ


def apply(signal : Signal1, carrier_freq, carrier_amp, method=PM_MODULATION, hertz=HERTZ):
    return PM_MODULATION_METHODS[method](signal, carrier_freq, carrier_amp, hertz)

def trad_modulation(signal : Signal1, carrier_freq, carrier_amp, hertz):
    time = signal.time
    freq = 2 * np.pi * carrier_freq if hertz else carrier_freq
    values = carrier_amp * np.sin(freq * time + signal.values)
    return Signal1(time, values)
        
PM_MODULATION_METHODS = {
    "trad": trad_modulation,
}

# class Modulator_PM(Modulator):
#     def __init__(self, carrier_freq, carrier_amp):
#         super().__init__(carrier_freq, carrier_amp)
#         self.methods = {
#             "traditional": self.trad_modulation,
#         }

#     def apply(self, signal : Signal1, method=PM_MODULATION, hertz=HERTZ):
#         return self.methods[method](signal, self.carrier_freq, self.carrier_amp, hertz)

#     def trad_modulation(self, signal : Signal1, carrier_freq, carrier_amp, hertz):
#         time = signal.time
#         freq = 2 * np.pi * carrier_freq if hertz else carrier_freq
#         values = carrier_amp * np.sin(freq * time + signal.values)
#         return Signal1(time, values)
