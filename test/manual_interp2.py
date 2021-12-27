import matplotlib.pyplot as plt
import numpy as np
from signpy.config import INTERP1_METHOD

from signpy.sgn import Signal2


# ax0 = np.array([0, 1, 2, 3], dtype=float)
# ax1 = np.array([0, 1, 2, 3], dtype=float)
# values = np.array(
#     [
#         [0, 1, 2, 3],
#         [1, 2, 3, 4],
#         [2, 3, 4, 5],
#         [3, 4, 5, 6],
#     ], dtype=float)

# signal = Signal2(ax0, ax1, values)
signal = Signal2.from_file("test/img/cat.png")
interpolated = signal(150.5, 150.5)

fig, ax = plt.subplots()
plt.imshow(signal.values, cmap="gray")

fig, ax = plt.subplots()
plt.imshow(interpolated[0].values, cmap="gray")

# fig, ax = plt.subplots()
# plt.contourf(*signal.contourf(), cmap="gray")

# fig, ax = plt.subplots()
# plt.contourf(*interpolated[0].contourf(), cmap="gray")

plt.show()