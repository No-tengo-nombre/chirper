import numpy as np
import matplotlib.pyplot as plt

from chirper.sgn.defaults import NOISE, SIN, SQUARE, COS
from chirper.transforms import f1, if1

################################################################################################################
################################################################################################################
################################################################################################################


def main(show_fig=False, export=True):
    end_time = 3
    sf = 4410 * 2
    time = np.linspace(0, end_time, end_time * sf)

    # signal1 = (
    #     SIN(time, 440, 20)
    #     + SIN(time, 880, 10)
    #     + SIN(time, 1320, 7)
    #     + SIN(time, 1760, 1)
    #     + SIN(time, 2200, 0.5)
    #     + SIN(time, 2640, 0.25)
    #     + SIN(time, 3080, 0.125)
    #     + SIN(time, 3520, 0.1)
    #     # + NOISE(time, 0.1)
    # )

    main_amp = 10
    f = 880
    i = 1

    signal1 = SIN(time, 440, main_amp)
    while f < sf / 2:
        signal1 += SIN(time, f, main_amp / (2 ** i))
        i += 1
        f += 440

    manipulated = f1(signal1).rect_smooth(3)

    mod = SIN(time, 10, 0.1) + SIN(time, 15, 0.075) + SIN(time, 25, 0.05) + 1
    signal1 *= mod

    gauss = manipulated
    for (i, w) in enumerate(gauss.axis):
        gauss.values[i] = np.exp(-w ** 2) if -3 < w < 3 else 0

    signal2 = SQUARE(time, 440, 20)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    fig.suptitle("Original signals")
    ax1.plot(*signal1.unpack(), label="Signal 1")
    ax2.plot(*if1(manipulated).real_part().unpack(),
             label="Manipulated (Re)")
    ax2.plot(*if1(manipulated).imag_part().unpack(),
             label="Manipulated (Im)")
    ax3.plot(*signal2.unpack(), label="Signal 2")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_xlabel("Time (s)")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    fig.suptitle("Fourier spectra")
    ax1.plot(*abs(f1(signal1)).unpack(), label="Signal 1")
    ax2.plot(*abs(manipulated).unpack(), label="Manipulated")
    ax3.plot(*abs(f1(signal2)).unpack(), label="Signal 2")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.grid()
    ax2.grid()
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_xlabel("Frequency (Hz)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")

    if export:
        print("Exporting")
        signal1.export_to_file("chirper/test/manual/outputs/manual_io_sgn1.wav")
        signal2.export_to_file("chirper/test/manual/outputs/manual_io_sgn2.wav")
        if1(manipulated).__abs__().export_to_file(
            "chirper/test/manual/outputs/manual_io_sgn3.wav")


if __name__ == "__main__":
    main(True)
