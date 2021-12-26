import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn.defaults import SIN, COS
from signpy.transforms import cosine


def main(show_fig=False):
    end_time = 3
    sf = 441
    time = np.linspace(0, end_time, end_time * sf)

    triangle_built = (
        SIN(time, 5, 10)
        + SIN(time, 10, 5)
        + SIN(time, 15, 2.5)
        + SIN(time, 20, 1.25)
        + SIN(time, 25, 0.625)
        + SIN(time, 30, 0.3125)
        + SIN(time, 35, 0.15625)
    )

    fig, ax = plt.subplots()
    fig.suptitle("Original signal")
    ax.plot(*triangle_built.unpack(), label="Original")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    c1 = cosine.c1(triangle_built, 1)
    c1_inv = cosine.c1(c1, 1)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DCT-I transform")
    ax.plot(*c1.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DCT-I Reconstructed")
    ax.plot(*c1_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    c2 = cosine.c1(triangle_built, 2)
    c2_inv = cosine.c1(c2, 3)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DCT-II transform")
    ax.plot(*c2.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DCT-II Reconstructed")
    ax.plot(*c2_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    c3 = cosine.c1(triangle_built, 3)
    c3_inv = cosine.c1(c3, 2)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DCT-III transform")
    ax.plot(*c3.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DCT-III Reconstructed")
    ax.plot(*c3_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    c4 = cosine.c1(triangle_built, 4)
    c4_inv = cosine.c1(c4, 4)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DCT-IV transform")
    ax.plot(*c4.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DCT-IV Reconstructed")
    ax.plot(*c4_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
