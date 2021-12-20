import numpy as np
import matplotlib.pyplot as plt

from signpy.sgn.defaults import SIN
from signpy.transforms import fourier, ifourier
from signpy.modulation import am, pm


time = np.linspace(0, 3000, 3000)

triangle_built = SIN(time, 5, 10) + SIN(time, 10, 5) + SIN(time, 15, 2.5) + SIN(time, 20, 1.25) + SIN(time, 25, 0.625) + SIN(time, 30, 0.3125)

t_am_mod = am.am_modulation(triangle_built, 200, 1)
t_pm_mod = pm.pm_modulation(triangle_built, 100, 10)

orig_fourier = fourier.f1(triangle_built)
am_fourier = fourier.f1(t_am_mod)
pm_fourier = fourier.f1(t_pm_mod)

orig_inv = ifourier.if1(orig_fourier)
am_inv = ifourier.if1(am_fourier)
pm_inv = ifourier.if1(pm_fourier)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

fig.suptitle("FFT")
ax1.plot(*abs(orig_fourier).unpack(), color="r", label="Fourier original")
ax2.plot(*abs(am_fourier).unpack(), color="b", label="Fourier AM modulated")
ax3.plot(*abs(pm_fourier).unpack(), color="g", label="Fourier PM modulated")
ax1.legend()
ax2.legend()
ax3.legend()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

fig.suptitle("Original vs modulated")
ax1.plot(*triangle_built.unpack(), color="r", label="Original")
ax2.plot(*t_am_mod.unpack(), color="b", label="AM Modulated")
ax3.plot(*t_pm_mod.unpack(), color="g", label="PM Modulated")
ax1.legend()
ax2.legend()
ax3.legend()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

fig.suptitle("Reconstructed signals")
ax1.plot(*orig_inv.unpack(), color="r", label="Original reconstructed")
ax2.plot(*am_inv.unpack(), color="b", label="AM Modulated reconstructed")
ax3.plot(*pm_inv.unpack(), color="g", label="PM Modulated reconstructed")
ax1.legend()
ax2.legend()
ax3.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle("Reconstructed vs originals")
ax1.plot(*triangle_built.unpack(), color="r", label="Original")
ax2.plot(*orig_inv.unpack(), color="b", label="Original reconstructed")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle("Reconstructed vs originals")
ax1.plot(*t_am_mod.unpack(), color="r", label="AM Modulated")
ax2.plot(*am_inv.unpack(), color="b", label="AM Modulated reconstructed")
ax1.legend()
ax2.legend()

plt.show()