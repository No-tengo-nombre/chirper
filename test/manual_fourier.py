import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn.defaults import IMPULSE, SIN, SQUARE, COS
from signpy.transforms import fourier, ifourier

################################################################################################################
################################################################################################################
################################################################################################################


def main(show_fig=False):
    end_time = 3
    sf = 4410
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

    # print(1 / (triangle_built.axis[1] - triangle_built.axis[0]))
    orig_fourier = fourier.f1(triangle_built)
    triangle_inv = ifourier.if1(orig_fourier)

    fig, ax = plt.subplots()
    fig.suptitle("Triangular signal fourier spectrum")
    ax.plot(*abs(orig_fourier).unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Original vs reconstructed signal")
    ax1.plot(*triangle_built.unpack(), label="Original")
    ax2.plot(*triangle_inv.unpack(), label="Reconstructed")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    end_time = 3
    sf = 4410
    time = np.linspace(0, end_time, end_time * sf)

    pulse = (
        SQUARE(time, 2, 10)
    )

    pulse_fourier = fourier.f1(pulse)
    pulse_inv = ifourier.if1(pulse_fourier)

    fig, ax = plt.subplots()
    fig.suptitle("Pulse fourier spectrum")
    ax.plot(*abs(pulse_fourier).unpack(), label="Spectrum")
    ax.legend()
    ax.grid()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (-)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Original vs reconstructed signal")
    ax1.plot(*pulse.unpack(), label="Original")
    ax2.plot(*pulse_inv.unpack(), label="Reconstructed")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    # rate = 1000
    # amp = 10000
    # center = 0.3

    # time = np.linspace(0, 1, 4410)
    # t1 = np.linspace(0, center, int(4410 * center))
    # t2 = np.linspace(center, 1, int(4410  * (1 - center)))

    # test_signal = SIN(time, 900, 10)
    # test_fourier = Fourier1(test_signal)

    # fourier_test = Signal1.from_function(time, lambda t: t)
    # s1 = Signal1.from_function(t1, lambda t: amp * np.exp(rate * (t - center)))
    # s2 = Signal1.from_function(t2, lambda t: amp * np.exp(-rate * (t - center)))
    # new_vals = np.array([*s1.values, *s2.values])
    # fourier_test.values = new_vals + 0.9 * np.flip(new_vals) + 1.5j * new_vals - 1j * np.flip(new_vals)
    # fourier_test = fourier_test.shift(-0.5)

    # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
    # fig.suptitle("Made up signal")
    # ax1.plot(*fourier_test.real_part().unpack(), label="Made up spectrum (Re)")
    # ax1.plot(*fourier_test.imag_part().unpack(), label="Made up spectrum (Im)", linestyle=":")
    # ax2.plot(*InverseFourier1(fourier_test).unpack(), label="Reconstructed")
    # ax3.plot(*test_fourier.freq_shift().real_part().unpack(), label="Test signal spectrum (Re)")
    # ax3.plot(*test_fourier.freq_shift().imag_part().unpack(), label="Test signal spectrum (Im)", linestyle=":")
    # ax4.plot(*test_signal.unpack(), label="Test signal")
    # ax1.legend()
    # ax2.legend()
    # ax3.legend()
    # ax4.legend()

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
