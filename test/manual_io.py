import numpy as np
import matplotlib.pyplot as plt
import struct

from numpy.lib.twodim_base import mask_indices

from signpy.sgn import Signal1
from signpy.sgn.defaults import SIN, SQUARE
from signpy.transforms.fourier import Fourier1, InverseFourier1

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
signal1 = (
    SIN(time, 440, 20)
    + SIN(time, 880, 4)
    + SIN(time, 1320, 7.5)
    + SIN(time, 1760, 5)
    + SIN(time, 2200, 4)
    + SIN(time, 2640, 3)
    + SIN(time, 3080, 2)
    + SIN(time, 3520, 1)
)
signal2 = SQUARE(time, 440, 10)

manipulated = Fourier1(signal1).freq_shift().rect_smooth(35)
# manipulated.values = np.array([10 * np.exp(-(t ** 2) / 0.01) for t in manipulated.axis])

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle("Original signals")
ax1.plot(*signal1.unpack(), label="Signal 1")
ax2.plot(*signal2.unpack(), label="Signal 2")
ax3.plot(*InverseFourier1(manipulated).real_part().unpack(), label="Manipulated (Re)")
ax3.plot(*InverseFourier1(manipulated).imag_part().unpack(), label="Manipulated (Im)")
ax1.legend()
ax2.legend()
ax3.legend()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle("Fourier spectra")
ax1.plot(*abs(Fourier1(signal1).freq_shift()).unpack(), label="Signal 1")
ax2.plot(*abs(Fourier1(signal2).freq_shift()).unpack(), label="Signal 2")
ax3.plot(*abs(manipulated).unpack(), label="Manipulated")
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
InverseFourier1(manipulated).__abs__().export_to_file("test/outputs/manual_io_sgn3.wav")
