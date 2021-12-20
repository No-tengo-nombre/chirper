import numpy as np
import matplotlib.pyplot as plt

from signpy.sgn.defaults import NOISE, SIN, SQUARE
# from signpy.transforms.fourier import Fourier1, InverseFourier1
from signpy.transforms import fourier, ifourier

################################################################################################################
################################################################################################################
################################################################################################################

end_time = 3
sf = 4410 * 2
time = np.linspace(0, end_time, end_time * sf)

# signal1 = SIN(time, 440, 10)
# signal1 = (
#     SIN(time, 1, 7.5)
#     + SIN(time, 440, 15)
#     + SIN(time, 880, 2)
#     + SIN(time, 1320, 5)
#     + SIN(time, 1760, 1.5)
# )
# signal1 = (
#     SIN(time, 440, 20)
#     + SIN(time, 880, 10)
#     + SIN(time, 1320, 7)
#     + SIN(time, 1760, 1)
#     + SIN(time, 2200, 0.5)
#     + SIN(time, 2640, 0.25)
#     + SIN(time, 3080, 0.125)
#     + SIN(time, 3520, 0.1)
#     # + NOISE(time, 0.1)
# )

main_amp = 10
f = 880
i = 1

signal1 = SIN(time, 440, main_amp)
while f < sf / 2:
    signal1 += SIN(time, f, main_amp / (2 ** i))
    i += 1
    f += 440

mod = SIN(time, 10, 0.1) + SIN(time, 15, 0.075) + SIN(time, 25, 0.05) + 1
signal1 *= mod

signal2 = SQUARE(time, 440, 20)

manipulated = fourier.f1(signal1).rect_smooth(5)
# manipulated.values = np.array([10 * np.exp(-(t ** 2) / 0.01) for t in manipulated.axis])

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle("Original signals")
ax1.plot(*signal1.unpack(), label="Signal 1")
ax2.plot(*signal2.unpack(), label="Signal 2")
ax3.plot(*ifourier.if1(manipulated).real_part().unpack(), label="Manipulated (Re)")
ax3.plot(*ifourier.if1(manipulated).imag_part().unpack(), label="Manipulated (Im)")
ax1.legend()
ax2.legend()
ax3.legend()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle("Fourier spectra")
ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Signal 1")
ax2.plot(*abs(fourier.f1(signal2)).unpack(), label="Signal 2")
# ax3.plot(*abs(manipulated).unpack(), label="Manipulated")
ax3.plot(*abs(fourier.f1(fourier.f1(signal1))).unpack(), label="Fourierception")
ax1.legend()
ax2.legend()
ax3.legend()

################################################################################################################
################################################################################################################
################################################################################################################

plt.show()

print("Exporting")

# signal1.export_to_file("outputs/manual_io_sgn1.wav", nchannels=1, sampwidth=10)
# signal2.export_to_file("outputs/manual_io_sgn2.wav", nchannels=1, sampwidth=10)
signal1.export_to_file("test/outputs/manual_io_sgn1.wav")
signal2.export_to_file("test/outputs/manual_io_sgn2.wav")
ifourier.if1(manipulated).__abs__().export_to_file("test/outputs/manual_io_sgn3.wav")
