import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal1
from signpy.sgn.defaults import COS, SIN
from signpy.transforms import fourier, hilbert


################################################################################################################
################################################################################################################
################################################################################################################

end_time = 10
sf = 2000
time = np.linspace(0.001, end_time, sf * end_time)

# signal1 = Signal1.from_function(time, lambda t: 1 / (t ** 2 + 1))
signal1 = COS(time, 10, 10)
hilbert_signal1 = hilbert.h1(signal1, "scipy")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original and hilbert transform (scipy)")
ax1.plot(*signal1.unpack(), label="Original")
ax2.plot(*hilbert_signal1.real_part().unpack(), label="Hilbert (Re)")
ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert (Im)")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Fourier spectra (scipy)")
ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Original")
ax2.plot(*abs(fourier.f1(hilbert_signal1.real_part())).unpack(), label="Hilbert (Re)")
ax2.plot(*abs(fourier.f1(hilbert_signal1.imag_part())).unpack(), label="Hilbert (Im)")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

end_time = 10
sf = 2000
time = np.linspace(0.001, end_time, sf * end_time)

signal1 = COS(time, 10, 10)
hilbert_signal1 = hilbert.h1(signal1, "prod")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original and hilbert transform (prod)")
ax1.plot(*signal1.unpack(), label="Original")
ax2.plot(*hilbert_signal1.real_part().unpack(), label="Hilbert (Re)")
ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert (Im)")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Fourier spectra (prod)")
ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Original")
ax2.plot(*abs(fourier.f1(hilbert_signal1.real_part())).unpack(), label="Hilbert (Re)")
ax2.plot(*abs(fourier.f1(hilbert_signal1.imag_part())).unpack(), label="Hilbert (Im)")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

end_time = 10
sf = 2000
time = np.linspace(0.001, end_time, sf * end_time)

signal1 = COS(time, 10, 10)
hilbert_signal1 = hilbert.h1(signal1, "fft")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original and hilbert transform (fft)")
ax1.plot(*signal1.unpack(), label="Original")
ax2.plot(*hilbert_signal1.real_part().unpack(), label="Hilbert (Re)")
ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert (Im)")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Fourier spectra (fft)")
ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Original")
ax2.plot(*abs(fourier.f1(hilbert_signal1.real_part())).unpack(), label="Hilbert (Re)")
ax2.plot(*abs(fourier.f1(hilbert_signal1.imag_part())).unpack(), label="Hilbert (Im)")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

plt.show()
