import numpy as np
import matplotlib.pyplot as plt

from signpy.sgn.defaults import SIN
from signpy.transforms import fourier, ifourier
from signpy.modulation import am, pm

################################################################################################################
################################################################################################################
################################################################################################################


def main(show_fig=False):
    end_time = 2
    sf = 2000
    time = np.linspace(0, end_time, end_time * sf)

    triangle_built = SIN(time, 5, 10) + SIN(time, 10, 5) + SIN(time, 15, 2.5) + \
        SIN(time, 20, 1.25) + SIN(time, 25, 0.625) + SIN(time, 30, 0.3125)

    t_am_mod = am.am_modulation(triangle_built, 200, 1)
    t_pm_mod = pm.pm_modulation(triangle_built, 100, 10)

    orig_fourier = fourier.f1(triangle_built)
    am_fourier = fourier.f1(t_am_mod)
    pm_fourier = fourier.f1(t_pm_mod)

    orig_inv = ifourier.if1(orig_fourier)
    am_inv = ifourier.if1(am_fourier)
    pm_inv = ifourier.if1(pm_fourier)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    fig.suptitle("FFT")
    ax1.plot(*abs(orig_fourier).unpack(), label="Fourier original")
    ax2.plot(*abs(am_fourier).unpack(), label="Fourier AM modulated")
    ax3.plot(*abs(pm_fourier).unpack(), label="Fourier PM modulated")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_xlabel("Frequency (Hz)")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    fig.suptitle("Original vs modulated")
    ax1.plot(*triangle_built.unpack(), label="Original")
    ax2.plot(*t_am_mod.unpack(), label="AM Modulated")
    ax3.plot(*t_pm_mod.unpack(), label="PM Modulated")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_xlabel("Time (s)")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    fig.suptitle("Reconstructed signals")
    ax1.plot(*orig_inv.real_part().unpack(),
             label="Original reconstructed (Re)")
    ax1.plot(*orig_inv.imag_part().unpack(),
             label="Original reconstructed (Im)")
    ax2.plot(*am_inv.real_part().unpack(),
             label="AM Modulated reconstructed (Re)")
    ax2.plot(*am_inv.imag_part().unpack(),
             label="AM Modulated reconstructed (Im)")
    ax3.plot(*pm_inv.real_part().unpack(),
             label="PM Modulated reconstructed (Re)")
    ax3.plot(*pm_inv.imag_part().unpack(),
             label="PM Modulated reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    fig.suptitle("Reconstructed vs originals")
    ax1.plot(*triangle_built.unpack(), label="Original")
    ax2.plot(*orig_inv.real_part().unpack(),
             label="Original reconstructed (Re)")
    ax2.plot(*orig_inv.imag_part().unpack(),
             label="Original reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    fig.suptitle("Reconstructed vs originals")
    ax1.plot(*t_am_mod.unpack(), label="AM Modulated")
    ax2.plot(*am_inv.real_part().unpack(),
             label="AM Modulated reconstructed (Re)")
    ax2.plot(*am_inv.imag_part().unpack(),
             label="AM Modulated reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    if show_fig:
        plt.show()
