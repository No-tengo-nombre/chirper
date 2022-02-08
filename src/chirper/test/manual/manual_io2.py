import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from chirper.utils import kernel
from chirper.sgn import Signal2
from chirper.transforms import c2, s2, f2


def main(show_fig=False, export=True):
    filename = "chirper/test/manual/img/cat.png"
    signal = Signal2.from_file(filename)
    signal_r = Signal2.from_file(filename, "r")
    signal_g = Signal2.from_file(filename, "g")
    signal_b = Signal2.from_file(filename, "b")

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

    signal_fourier = f2(signal)
    # signal_cos = c2(signal)
    # signal_sine = s2(signal)

    fig, ax = plt.subplots()
    fig.suptitle("Fourier transform")
    im = ax.imshow(abs(signal_fourier).values, cmap="gray", norm=LogNorm(0.01, 1e6))
    fig.colorbar(im)

    # fig, ax = plt.subplots()
    # fig.suptitle("Cosine transform")
    # plt.imshow(signal_cos.values, cmap="gray")
    # plt.colorbar()

    # fig, ax = plt.subplots()
    # fig.suptitle("Sine transform")
    # plt.imshow(signal_sine.values, cmap="gray")
    # plt.colorbar()

    # signal = Signal2.from_freq(signal[150:250, 150:250])
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
    plt.imshow(abs(signal_edge[1:-1, 1:-1]), cmap="gray")
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
