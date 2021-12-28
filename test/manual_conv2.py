import matplotlib.pyplot as plt
import numpy as np

from src.chirper.sgn import Signal2
from src.chirper import kernel


def f(x, y):
    return np.sin(x ** 2 + y ** 2)


def main(show_fig=False):
    axis = np.linspace(0, 20, 100)

    Y = Signal2.from_function(axis, axis, f)

    fig, ax = plt.subplots()
    fig.suptitle("Original")
    plt.imshow(Y.values, cmap="Greys", origin="lower")
    # plt.contourf(*Y.unpack(), cmap="Greys")
    plt.colorbar()

    kernel1 = kernel.ker_mean(3)
    kernel2 = kernel.ker_mean(5)
    kernel3 = kernel.ker_edge()
    kernel4 = kernel.ker_sharpen()

    Y_mean1 = Y.apply_kernel(kernel1)
    Y_mean2 = Y.apply_kernel(kernel2)
    Y_edge1 = Y.apply_kernel(kernel3)
    Y_sharpen = Y.apply_kernel(kernel4)

    fig, ax = plt.subplots()
    fig.suptitle("Convoluted Mean 3x3")
    plt.imshow(Y_mean1.values, cmap="Greys", origin="lower")
    # plt.contourf(*Y_mean.unpack(), cmap="Greys")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Convoluted Mean 5x5")
    plt.imshow(Y_mean2.values, cmap="Greys", origin="lower")
    # plt.contourf(*Y_mean.unpack(), cmap="Greys")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Edge")
    plt.imshow(Y_edge1.values, cmap="Greys", origin="lower")
    # plt.contourf(*Y_mean.unpack(), cmap="Greys")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Sharpen")
    plt.imshow(Y_sharpen.values, cmap="Greys", origin="lower")
    # plt.contourf(*Y_mean.unpack(), cmap="Greys")
    plt.colorbar()

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
