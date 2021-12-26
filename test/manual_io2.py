import numpy as np
import matplotlib.pyplot as plt

from signpy import kernel
from signpy.sgn import Signal2


def main(show_fig=False, export=True):
    signal = Signal2.from_file("test/img/cat.png")
    signal_r = Signal2.from_file("test/img/cat.png", "r")
    signal_g = Signal2.from_file("test/img/cat.png", "g")
    signal_b = Signal2.from_file("test/img/cat.png", "b")

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Original")
    ax1.set_title("Mean channel")
    ax2.set_title("RGB channel")
    im1 = ax1.imshow(signal.values, cmap="gray")
    im2 = ax2.imshow(
        np.stack([signal_r.values, signal_g.values, signal_b.values], axis=2))
    plt.colorbar(im1, ax=ax1)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    fig.suptitle("Original")
    ax1.set_title("Mean channel")
    ax2.set_title("Red channel")
    ax3.set_title("Green channel")
    ax4.set_title("Blue channel")
    im1 = ax1.imshow(signal.values, cmap="gray")
    im2 = ax2.imshow(signal_r.values, cmap="Reds")
    im3 = ax3.imshow(signal_g.values, cmap="Greens")
    im4 = ax4.imshow(signal_b.values, cmap="Blues")

    plt.colorbar(im1, ax=ax1)
    plt.colorbar(im2, ax=ax2)
    plt.colorbar(im3, ax=ax3)
    plt.colorbar(im4, ax=ax4)

    signal = Signal2.from_freq(signal[100:200, 100:200])
    signal_mean = signal.apply_kernel(kernel.ker_mean(3))
    signal_edge = signal.apply_kernel(kernel.ker_edge())
    signal_sharpen = signal.apply_kernel(kernel.ker_sharpen())

    fig, ax = plt.subplots()
    fig.suptitle("Mean 3x3")
    plt.imshow(signal_mean.values, cmap="gray")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Edge")
    plt.imshow(signal_edge[1:-1, 1:-1], cmap="gray")
    plt.colorbar()

    fig, ax = plt.subplots()
    fig.suptitle("Sharpen")
    plt.imshow(signal_sharpen.values, cmap="gray")
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
