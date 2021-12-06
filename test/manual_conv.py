import matplotlib.pyplot as plt
import numpy as np
from signpy.sgn import Signal1

from signpy.sgn.defaults import NOISE, SIN
from signpy.transforms.fourier import Fourier1, InverseFourier1


################################################################################################################
################################################################################################################
################################################################################################################

time = np.linspace(0, 1000, 1000)

# signal1 = NOISE(time, 5)
signal1 = SIN(time, 5, 10)
for i in range(10, 200, 5):
    signal1 += SIN(time, i, 10)
# signal1 += NOISE(time, 10)
# signal1 *= NOISE(time, 2, False)


signal2 = Signal1.from_function(time, lambda t: 10 * np.sinc(2 * np.pi * 0.01 * t))
# signal2 += NOISE(time, 1)
# signal2 = Signal1(time, [np.sin(0.1 * t) / t if t != 0 else 1 for t in time])
# signal2 = Signal1(time, [np.log(t) if t != 0 else 1 for t in time])


fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original signals")
ax1.plot(*signal1.unpack(), label="Signal 1")
ax2.plot(*signal2.unpack(), label="Signal 2")
ax1.legend()
ax2.legend()

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original signals fourier spectra")
ax1.plot(*abs(Fourier1(signal1).freq_shift()).unpack(), label="Signal 1")
ax2.plot(*abs(Fourier1(signal2).freq_shift()).unpack(), label="Signal 2")
ax1.legend()
ax2.legend()

conv_signal = signal1.convolute(signal2)
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Convoluted signal")
ax1.plot(*conv_signal.unpack(), label="Convoluted signal")
ax2.plot(*abs(Fourier1(conv_signal).freq_shift()).unpack(), label="Convoluted signal spectrum")
ax1.legend()
ax2.legend()

################################################################################################################
################################################################################################################
################################################################################################################

time = np.linspace(0, 1000, 1000)

# signal1 = NOISE(time, 5)
signal1 = SIN(time, 5, 10)
# for i in range(10, 200, 5):
#     signal1 += SIN(time, i, 10)
signal1 += NOISE(time, 2)
# signal1 *= NOISE(time, 2, False)


signal2 = Signal1.from_function(time, lambda t: 10 * np.sinc(2 * np.pi * 0.01 * t))
signal2 += NOISE(time, 0.5)
# signal2 = Signal1(time, [np.sin(0.1 * t) / t if t != 0 else 1 for t in time])
# signal2 = Signal1(time, [np.log(t) if t != 0 else 1 for t in time])


fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Original signals")
ax1.plot(*signal1.unpack(), label="Signal 1")
ax2.plot(*signal2.unpack(), label="Signal 2")
ax1.legend()
ax2.legend()

sign1_ac = signal1.auto_correlate(method="fft")
sign2_ac = signal2.auto_correlate(method="fft")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Auto-correlated signals")
ax1.plot(*sign1_ac.unpack(), label="Signal 1")
ax2.plot(*sign2_ac.unpack(), label="Signal 2")
ax1.legend()
ax2.legend()

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
fig.suptitle("Fourier spectra")
ax1.plot(*abs(Fourier1(signal1).freq_shift()).unpack(), label="Signal 1")
ax2.plot(*abs(Fourier1(sign1_ac).freq_shift()).unpack(), label="Signal 1 auto")
ax3.plot(*abs(Fourier1(signal2).freq_shift()).unpack(), label="Signal 2")
ax4.plot(*abs(Fourier1(sign2_ac).freq_shift()).unpack(), label="Signal 2 auto")
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()

################################################################################################################
################################################################################################################
################################################################################################################

plt.show()
