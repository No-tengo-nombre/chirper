import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal1
from signpy.sgn.defaults import COS, SIN
from signpy.transforms import fourier, hilbert

################################################################################################################
################################################################################################################
################################################################################################################


def main(show_fig=False):
    end_time = 10
    sf = 2000
    time = np.linspace(0.001, end_time, sf * end_time)

    signal1 = COS(time, 10, 10)
    hilbert_signal1 = hilbert.h1(signal1, "scipy")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Original and hilbert transform (scipy)")
    ax1.plot(*signal1.unpack(), label="Original")
    ax2.plot(*hilbert_signal1.real_part().unpack(), label="Hilbert (Re)")
    ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Fourier spectra (scipy)")
    ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Original")
    ax2.plot(*abs(fourier.f1(hilbert_signal1.real_part())
                  ).unpack(), label="Hilbert (Re)")
    ax2.plot(*abs(fourier.f1(hilbert_signal1.imag_part())
                  ).unpack(), label="Hilbert (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Frequency (Hz)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    end_time = 10
    sf = 2000
    time = np.linspace(0.001, end_time, sf * end_time)

    signal1 = COS(time, 10, 10)
    hilbert_signal1 = hilbert.h1(signal1, "prod")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Original and hilbert transform (prod)")
    ax1.plot(*signal1.unpack(), label="Original")
    ax2.plot(*hilbert_signal1.real_part().unpack(), label="Hilbert (Re)")
    ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Fourier spectra (prod)")
    ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Original")
    ax2.plot(*abs(fourier.f1(hilbert_signal1.real_part())
                  ).unpack(), label="Hilbert (Re)")
    ax2.plot(*abs(fourier.f1(hilbert_signal1.imag_part())
                  ).unpack(), label="Hilbert (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Frequency (Hz)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    end_time = 10
    sf = 2000
    time = np.linspace(0.001, end_time, sf * end_time)

    signal1 = COS(time, 10, 10)
    hilbert_signal1 = hilbert.h1(signal1, "fft")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Original and hilbert transform (fft)")
    ax1.plot(*signal1.unpack(), label="Original")
    ax2.plot(*hilbert_signal1.real_part().unpack(), label="Hilbert (Re)")
    ax2.plot(*hilbert_signal1.imag_part().unpack(), label="Hilbert (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Fourier spectra (fft)")
    ax1.plot(*abs(fourier.f1(signal1)).unpack(), label="Original")
    ax2.plot(*abs(fourier.f1(hilbert_signal1.real_part())
                  ).unpack(), label="Hilbert (Re)")
    ax2.plot(*abs(fourier.f1(hilbert_signal1.imag_part())
                  ).unpack(), label="Hilbert (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Frequency (Hz)")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
