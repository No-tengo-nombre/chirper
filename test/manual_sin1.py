import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn.defaults import SIN
from signpy.transforms import sine


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

    s1 = sine.s1(triangle_built, 1)
    s1_inv = sine.s1(s1, 1)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DST-I transform")
    ax.plot(*s1.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DST-I Reconstructed")
    ax.plot(*s1_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    s2 = sine.s1(triangle_built, 2)
    s2_inv = sine.s1(s2, 3)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DST-II transform")
    ax.plot(*s2.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DST-II Reconstructed")
    ax.plot(*s2_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    s3 = sine.s1(triangle_built, 3)
    s3_inv = sine.s1(s3, 2)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DST-III transform")
    ax.plot(*s3.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DST-III Reconstructed")
    ax.plot(*s3_inv.unpack(), label="Reconstructed")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (-)")

    s4 = sine.s1(triangle_built, 4)
    s4_inv = sine.s1(s4, 4)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal DST-IV transform")
    ax.plot(*s4.unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, ax = plt.subplots()
    fig.suptitle("DST-IV Reconstructed")
    ax.plot(*s4_inv.unpack(), label="Reconstructed")
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
