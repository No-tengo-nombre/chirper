import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal2
from signpy.transforms import fourier, ifourier


def f(x, y):
    return np.cos(1 * x + 1 * y)


axis = np.arange(40)

Y = Signal2.from_function(axis, axis, f)
fig, ax = plt.subplots()
plt.imshow(Y.values, cmap="Greys", origin="lower")

y_fft = fourier.f2(Y, "fft")

fig, ax = plt.subplots()
fig.suptitle("FFT")
plt.imshow(np.imag(y_fft.values), cmap="Greys", origin="lower")


plt.show()
