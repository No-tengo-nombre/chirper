import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn.defaults import IMPULSE, SIN, SQUARE
from signpy.transforms.fourier import Fourier1, InverseFourier1


################################################################################################################
################################################################################################################
################################################################################################################

time = np.linspace(0, 3000, 3000)

triangle_built = (
    SIN(time, 5, 10)
    + SIN(time, 10, 5) 
    + SIN(time, 15, 2.5) 
    + SIN(time, 20, 1.25) 
    + SIN(time, 25, 0.625) 
    + SIN(time, 30, 0.3125)
    + SIN(time, 35, 0.15625)
)

orig_fourier = Fourier1(triangle_built)
triangle_inv = InverseFourier1(orig_fourier)

fig, ax = plt.subplots()
fig.suptitle("Triangular signal fourier spectrum")
ax.plot(*abs(orig_fourier.freq_shift()).unpack(), label="Spectrum")
ax.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original vs reconstructed signal")
ax1.plot(*triangle_built.unpack(), label="Original")
ax2.plot(*triangle_inv.unpack(), label="Reconstructed")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

time = np.linspace(0, 100, 1000)

pulse = (
    SQUARE(time, 0.2, 10)
)

pulse_fourier = Fourier1(pulse)
pulse_inv = InverseFourier1(pulse_fourier)

fig, ax = plt.subplots()
fig.suptitle("Pulse fourier spectrum")
ax.plot(*abs(pulse_fourier.freq_shift()).unpack(), label="Spectrum")
ax.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original vs reconstructed signal")
ax1.plot(*pulse.unpack(), label="Original")
ax2.plot(*pulse_inv.unpack(), label="Reconstructed")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

plt.show()
