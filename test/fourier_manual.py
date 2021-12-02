# from numpy.lib.twodim_base import tri
from signpy import sgn
from signpy.transforms import fourier

import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0, 3000, 3000)

triangle_built = (
    sgn.SIN(time, 5, 10)
    + sgn.SIN(time, 10, 5) 
    + sgn.SIN(time, 15, 2.5) 
    + sgn.SIN(time, 20, 1.25) 
    + sgn.SIN(time, 25, 0.625) 
    + sgn.SIN(time, 30, 0.3125)
    + sgn.SIN(time, 35, 0.15625)
)

orig_fourier = fourier.Fourier(triangle_built)
triangle_inv = fourier.InverseFourier(orig_fourier)
triangle_inv_calc = triangle_inv.calculate()

fig, ax = plt.subplots()
fig.suptitle("Triangular signal fourier spectrum")
ax.plot(*abs(orig_fourier.calculate_shift()).unpack(), label="Spectrum")
ax.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original vs reconstructed signal")
ax1.plot(*triangle_built.unpack(), label="Original")
# ax2.plot(*triangle_inv.calculate().real_part().unpack(), label="Reconstructed (real)")
# ax2.plot(*triangle_inv.calculate().imag_part().unpack(), label="Reconstructed (imag)")
ax2.plot(*triangle_inv_calc.unpack(), label="Reconstructed")
ax2.plot(*triangle_inv.calculate().unpack(), label="a")
ax1.legend()
ax2.legend()

plt.show()
