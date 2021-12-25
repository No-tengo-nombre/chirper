import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal2
from signpy.kernel import ker_mean


def f(x, y):
    return np.sin(x ** 2 + y ** 2)


axis = np.linspace(0, 20, 100)

Y = Signal2.from_function(axis, axis, f)

fig, ax = plt.subplots()
fig.suptitle("Original")
plt.imshow(Y.values, cmap="Greys", origin="lower")
# plt.contourf(*Y.unpack(), cmap="Greys")

kernel1 = ker_mean(3)
kernel2 = ker_mean(5)

Y_mean1 = Y.convolute(kernel1)
Y_mean2 = Y.convolute(kernel2)

fig, ax = plt.subplots()
fig.suptitle("Convoluted Mean 3x3")
plt.imshow(Y_mean1.values, cmap="Greys", origin="lower")
# plt.contourf(*Y_mean.unpack(), cmap="Greys")

fig, ax = plt.subplots()
fig.suptitle("Convoluted Mean 5x5")
plt.imshow(Y_mean2.values, cmap="Greys", origin="lower")
# plt.contourf(*Y_mean.unpack(), cmap="Greys")


plt.show()