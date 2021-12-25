import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal2
from signpy.transforms import fourier, ifourier


def f(x, y):
    return np.sin(x ** 2 + y ** 2)


def main(show_fig=False):
    axis = np.linspace(0, 20, 1000)

    Y = Signal2.from_function(axis, axis, f)

    fig, ax = plt.subplots()
    fig.suptitle("Original")
    # plt.imshow(Y.values, cmap="Greys", origin="lower")
    plt.contourf(*Y.unpack(), cmap="Greys")

    y_fft = fourier.f2(Y)
    y_inv = ifourier.if2(y_fft)
    y_inv_fft = fourier.f2(y_inv)

    fig, ax = plt.subplots()
    fig.suptitle("FFT")
    # plt.imshow(abs(y_fft).values, cmap="Greys", origin="lower")
    plt.contourf(*abs(y_fft).unpack(), cmap="Greys")

    fig, ax = plt.subplots()
    fig.suptitle("Reconstructed")
    # plt.imshow(y_inv.values, cmap="Greys", origin="lower")
    plt.contourf(*y_inv.unpack(), cmap="Greys")

    fig, ax = plt.subplots()
    fig.suptitle("Reconstructed Fourier")
    # plt.imshow(y_inv.values, cmap="Greys", origin="lower")
    plt.contourf(*abs(y_inv_fft).unpack(), cmap="Greys")

    # fig, ax = plt.subplots()
    # fig.suptitle("Error")
    # # plt.imshow(y_inv.values, cmap="Greys", origin="lower")
    # plt.contourf(*(y_inv - Y).unpack(), cmap="Greys")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)