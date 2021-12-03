from signpy import sgn
from signpy.sgn.defaults import SIN
from signpy.transforms import fourier

import matplotlib.pyplot as plt
import numpy as np

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

orig_fourier = fourier.Fourier(triangle_built)
triangle_inv = fourier.InverseFourier(orig_fourier)

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

plt.show()
