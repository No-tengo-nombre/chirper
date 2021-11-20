import signpy.sgn.signal as signal
from signpy.sgn.signal import Signal
from signpy.transforms.fourier import Fourier, InverseFourier

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft

# def modulate(carrier, modulator):


if __name__ == "__main__":
    Vp = 1.8 / 2
    fp = 200
    Vm = 0.4 / 2
    fm = 10

    m = Vm / Vp

    carrier_params = {
        "freq": fp,
        "amp": Vp
    }
    mod_params = {
        "freq": fm,
        "amp": Vm
    }

    sr = (5e-1) / 10000

    time = np.linspace(0, 5e-1, 10000)
    carrier = signal.SIN(time, **carrier_params)
    mod = signal.SIN(time, **mod_params)
    modulated = Signal.from_function(time, lambda t: Vp * np.sin(2 * np.pi * fp * t) + 0.5 * m * Vp * np.cos(2 * np.pi * (fp - fm) * t) - 0.5 * m * Vp * np.cos(2 * np.pi * (fp + fm) * t))
    # fourier = abs(Fourier(modulated).calculate())
    
    new_t, mod_vals = carrier.unpack()
    mod_fft = fft(mod_vals)
    N = len(mod_fft)

    fig, ax = plt.subplots()

    # ax.plot(*carrier.unpack(), label="Portadora")
    # ax.plot(*mod.unpack(), label="Moduladora")
    # ax.plot(*modulated.unpack(), label="Modulada xd")
    # ax.plot(*fourier.unpack(), label="Fourier")
    ax.plot(, abs(mod_fft), label="fourier")
    # ax.plot(*(carrier * mod / Vp + carrier).unpack(),  label="Modulada")

    ax.legend()

    plt.show()
