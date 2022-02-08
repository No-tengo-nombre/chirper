import matplotlib.pyplot as plt
import numpy as np

from chirper.sgn import Signal2
from chirper.transforms import f2, if2


def f(x, y):
    return np.sin(x ** 2 + y ** 2)


def main(show_fig=False):
    axis = np.linspace(0, 20, 1000)

    Y = Signal2.from_function(axis, axis, f)

    fig, ax = plt.subplots()
    fig.suptitle("Original")
    plt.imshow(Y.values, cmap="gray", origin="lower")
    # plt.contourf(*Y.unpack(), cmap="gray")
    plt.colorbar()

    y_fft = f2(Y)
    y_inv = if2(y_fft)
    y_inv_fft = f2(y_inv)

    fig, ax = plt.subplots()
    fig.suptitle("FFT")
    plt.imshow(y_fft.psd().values, cmap="gray", origin="lower")
    # plt.contourf(*y_fft.psd().unpack(), cmap="gray")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Reconstructed")
    plt.imshow(y_inv.real_part().values, cmap="gray", origin="lower")
    # plt.contourf(*y_inv.real_part().unpack(), cmap="gray")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Reconstructed Fourier")
    plt.imshow(y_inv_fft.psd().values, cmap="gray", origin="lower")
    # plt.contourf(*y_inv_fft.psd().unpack(), cmap="gray")
    plt.colorbar()

    # fig, ax = plt.subplots()
    # fig.suptitle("Error")
    # # plt.imshow((y_inv - Y).values, cmap="gray", origin="lower")
    # plt.contourf(*(y_inv - Y).unpack(), cmap="gray")
    # plt.colorbar()
    # print("A")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)