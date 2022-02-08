import numpy as np
import matplotlib.pyplot as plt

from chirper.sgn.defaults import SIN
from chirper.transforms import f1, if1
from chirper.modulation import am_modulation

################################################################################################################
################################################################################################################
################################################################################################################


def main(show_fig=False):
    end_time = 2
    sf = 2000
    time = np.linspace(0, end_time, int(sf * end_time))

    triangle_built = SIN(time, 5, 10) + SIN(time, 10, 5) + SIN(time, 15, 2.5) + \
        SIN(time, 20, 1.25) + SIN(time, 25, 0.625) + SIN(time, 30, 0.3125)

    dsbfc_t = am_modulation(triangle_built, 200, 1, method="dsbfc")
    dsbsc_t = am_modulation(triangle_built, 200, 1, method="dsbsc")
    ssbu_t = am_modulation(triangle_built, 200, method="usb")
    ssbl_t = am_modulation(triangle_built, 200, method="lsb")

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)
    fig.suptitle("Original and different AM modulations")
    ax1.plot(*triangle_built.unpack(), label="Original")
    ax2.plot(*dsbfc_t.unpack(), label="DSBFC")
    ax3.plot(*dsbsc_t.unpack(), label="DSBSC")
    ax4.plot(*ssbu_t.unpack(), label="SSB Upper")
    ax5.plot(*ssbl_t.unpack(), label="SSB Lower")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax5.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax3.set_ylabel("Amplitude (-)")
    ax5.set_xlabel("Time (s)")

    orig_fourier = f1(triangle_built)
    dsbfc_fourier = f1(dsbfc_t)
    dsbsc_fourier = f1(dsbsc_t)
    ssbu_fourier = f1(ssbu_t)
    ssbl_fourier = f1(ssbl_t)

    orig_inv = if1(orig_fourier)
    dsbfc_inv = if1(dsbfc_fourier)
    dsbsc_inv = if1(dsbsc_fourier)
    ssbu_inv = if1(ssbu_fourier)
    ssbl_inv = if1(ssbl_fourier)

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)
    fig.suptitle("Fourier spectra of different AM modulations")
    ax1.plot(*abs(orig_fourier).unpack(), label="Original")
    ax2.plot(*abs(dsbfc_fourier).unpack(), label="DSBFC")
    ax3.plot(*abs(dsbsc_fourier).unpack(), label="DSBSC")
    ax4.plot(*abs(ssbu_fourier).unpack(), label="SSB Upper")
    ax5.plot(*abs(ssbl_fourier).unpack(), label="SSB Lower")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax5.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax3.set_ylabel("Amplitude (-)")
    ax5.set_xlabel("Frequency (Hz)")

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)
    fig.suptitle("Reconstructed modulations")
    ax1.plot(*orig_inv.real_part().unpack(), label="Original (Re)")
    ax1.plot(*orig_inv.imag_part().unpack(), label="Original (Im)")
    ax2.plot(*dsbfc_inv.real_part().unpack(), label="DSBFC (Re)")
    ax2.plot(*dsbfc_inv.imag_part().unpack(), label="DSBFC (Im)")
    ax3.plot(*dsbsc_inv.real_part().unpack(), label="DSBSC (Re)")
    ax3.plot(*dsbsc_inv.imag_part().unpack(), label="DSBSC (Im)")
    ax4.plot(*ssbu_inv.real_part().unpack(), label="SSB Upper (Re)")
    ax4.plot(*ssbu_inv.imag_part().unpack(), label="SSB Upper (Im)")
    ax5.plot(*ssbl_inv.real_part().unpack(), label="SSB Lower (Re)")
    ax5.plot(*ssbl_inv.imag_part().unpack(), label="SSB Lower (Im)")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax5.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax3.set_ylabel("Amplitude (-)")
    ax5.set_xlabel("Time (s)")

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
