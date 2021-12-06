import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal1
from signpy.sgn.defaults import SIN
from signpy.transforms.fourier import Fourier1
from signpy.transforms.hilbert import Hilbert


################################################################################################################
################################################################################################################
################################################################################################################

time = np.linspace(0, 10, 99)

signal1 = Signal1.from_function(time, lambda t: 1 / (t ** 2 + 1))
hilbert_signal1 = Hilbert(signal1, "scipy")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original and hilbert transform")
ax1.plot(*signal1.unpack(), label="Original")
ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Fourier spectra")
ax1.plot(*abs(Fourier1(signal1).freq_shift()).unpack(), label="Original")
ax2.plot(*abs(Fourier1(hilbert_signal1).freq_shift()).unpack(), label="Hilbert")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

time = np.linspace(0.001, 100, 100)

signal1 = SIN(time, 10, 10)
hilbert_signal1 = Hilbert(signal1, "prod")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original and hilbert transform")
ax1.plot(*signal1.unpack(), label="Original")
ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Fourier spectra")
ax1.plot(*abs(Fourier1(signal1).freq_shift()).unpack(), label="Original")
ax2.plot(*abs(Fourier1(hilbert_signal1).freq_shift()).unpack(), label="Hilbert")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

plt.show()
