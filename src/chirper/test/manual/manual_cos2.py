import matplotlib.pyplot as plt
import numpy as np

from chirper.sgn import Signal2
from chirper.transforms import c2


def f(x, y):
    return np.sin(x ** 2 + y ** 2)
    # return np.sin(1.1 * x + 0.6 * y)

def main(show_fig=False):
    axis = np.linspace(0, 20, 50)

    Y = Signal2.from_function(axis, axis, f)

    fig, ax = plt.subplots()
    fig.suptitle("Original")
    plt.imshow(Y.values, cmap="gray", origin="lower")
    # plt.contourf(*Y.unpack(), cmap="Greys")

    y_c2 = c2(Y, 2)
    y_c4 = c2(Y, 4)

    fig, ax = plt.subplots()
    fig.suptitle("Cosine 2")
    plt.imshow(y_c2.values, cmap="gray", origin="lower")
    # plt.contourf(*y_c2.unpack(), cmap="gray")

    fig, ax = plt.subplots()
    fig.suptitle("Cosine 4")
    plt.imshow(y_c4.values, cmap="gray", origin="lower")
    # plt.contourf(*y_c4.unpack(), cmap="gray")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)