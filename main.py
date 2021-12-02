from signpy.sgn import signal
from signpy.sgn.signal import HEAVISIDE, SIN, Signal1, IMPULSE
from signpy.transforms.hilbert import Hilbert
from signpy.transforms.fourier import Fourier, InverseFourier
from signpy.modulation import am, pm

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    wave1 = {
        "freq": 2 * np.pi * 50,
        "amp": 10
    }
    wave2 = {
        "freq": 2 * np.pi * 50,
        "amp": 10
    }
    wave3 = {
        "freq": 2 * np.pi * 600,
        "amp": 5
    }

    time = np.linspace(0, 3000, 3000)

    signal1 = Signal1.from_function(
        time,
        lambda t: wave1["amp"] * np.sin(wave1["freq"] * t)
    )
    signal2 = Signal1.from_function(
        time,
        lambda t: wave2["amp"] * np.sin(wave2["freq"] * t)
    )
    signal3 = Signal1.from_function(
        time,
        lambda t: wave3["amp"] * np.sin(wave3["freq"] * t)
    )

    sq_signal = signal.SQUARE(time, 100e-4, 10)

    noise0 = signal.NOISE(time, 0.1)
    noise1 = signal.NOISE(time, 1)
    noise2 = signal.NOISE(time, 2)
    noise3 = signal.NOISE(time, 3)
    noise4 = signal.NOISE(time, 4)
    noise5 = signal.NOISE(time, 5)

    noise_m_0 = signal.NOISE(time, 0.1, add=False)
    noise_m_1 = signal.NOISE(time, 1, add=False)
    noise_m_2 = signal.NOISE(time, 2, add=False)
    noise_m_3 = signal.NOISE(time, 3, add=False)
    noise_m_4 = signal.NOISE(time, 4, add=False)
    noise_m_5 = signal.NOISE(time, 5, add=False)

    heaviside1 = signal.HEAVISIDE(time, 1000)

    # fourier = Fourier(signal1).calculate()
    # sum_signal = signal1 + signal2 + signal3

    # mixed_signal = (signal1 + signal2 + signal3 + noise5)

    # fig, ax = plt.subplots()

    # plt.scatter(*signal1.unpack())
    # plt.scatter(*signal2.unpack())

    # fourier = Fourier(mixed_signal)
    # filtered = fourier.calculate()
    # filtered.apply_function(lambda t: t if abs(t) > 1 else 0)
    # filtered = filtered * signal.HEAVISIDE(time, 1000, True) * signal.HEAVISIDE(time, -1000)

    # fig1, ax1 = plt.subplots(2, 1)

    # ax1[0].plot(*signal1.unpack(), color="b")
    # plt.plot(*signal2.unpack(), color="b")
    # plt.plot(*signal3.unpack(), color="b")
    # plt.plot(*sum_signal.unpack(), color="b")
    # plt.plot(*(sq_signal + noise5).unpack(), color="b")
    # ax1[0].plot(*mixed_signal.unpack(), color="b")
    # ax1[1].plot(*InverseFourier(filtered).calculate().unpack(), color="g")
    # ax1[0].set_xlim(0)
    # ax1[1].set_xlim(0)

    # labels = ["Original signal", "Filtered signal"]
    # plt.legend(labels)
    #
    # fig2, ax2 = plt.subplots(2, 1)
    #
    # ax2[0].plot(*abs(fourier.calculate()).unpack(), color="b")
    # ax2[1].plot(*filtered.unpack(), color="g")
    # # ax2[0].set_xlim(0)
    # # ax2[1].set_xlim(0)
    #
    # labels = ["Original fourier", "Filtered fourier"]
    # plt.legend(labels)

    triangle_built = SIN(time, 5, 10) + SIN(time, 10, 5) + SIN(time, 15, 2.5) + SIN(time, 20, 1.25) + SIN(time, 25, 0.625) + SIN(time, 30, 0.3125)

    am_mod = am.Modulator_AM(200, 1)
    pm_mod = pm.Modulator_PM(100, 10)
    triangle_mod = am_mod.apply(triangle_built)
    triangle_pm_mod = pm_mod.apply(triangle_built)

    orig_fourier = Fourier(triangle_built)
    mod_fourier = Fourier(triangle_mod)
    pm_fourier = Fourier(triangle_pm_mod)

    # orig_fourier_dft = orig_fourier.calculate("dft")
    # mod_fourier_dft = mod_fourier.calculate("dft")

    orig_fourier_fft = orig_fourier.calculate_shift()
    mod_fourier_fft = mod_fourier.calculate_shift()
    pm_fourier_fft = pm_fourier.calculate_shift()

    # plt.suptitle("DFT")
    # plt.plot(*abs(orig_fourier_dft).unpack(), color="r")
    # plt.plot(*abs(mod_fourier_dft).unpack(), color="b")
    # # plt.xlim(0, 400)

    fig, ax = plt.subplots()

    fig.suptitle("FFT")
    ax.plot(*abs(orig_fourier_fft).unpack(), color="r", label="Fourier original")
    ax.plot(*abs(mod_fourier_fft).unpack(), color="b", label="Fourier AM modulated")
    ax.plot(*abs(pm_fourier_fft).unpack(), color="g", label="Fourier PM modulated")
    ax.legend()

    fig, ax = plt.subplots()

    fig.suptitle("Original vs modulated")
    # ax.plot(*triangle_built.unpack(), color="r", label="Original")
    # ax.plot(*triangle_mod.unpack(), color="b", label="AM Modulated")
    ax.plot(*triangle_pm_mod.unpack(), color="g", label="PM Modulated")
    ax.legend()

    orig_inv = InverseFourier(orig_fourier_fft).calculate_shift()
    mod_inv = InverseFourier(mod_fourier_fft).calculate_shift()
    pm_inv = InverseFourier(pm_fourier_fft).calculate_shift()

    fig, ax = plt.subplots()

    fig.suptitle("Reconstructed signals")
    ax.plot(*orig_inv.unpack(), color="r", label="Original reconstructed")
    ax.plot(*mod_inv.unpack(), color="b", label="AM Modulated reconstructed")
    ax.plot(*pm_inv.unpack(), color="g", label="PM Modulated reconstructed")
    ax.legend()

    fig, ax = plt.subplots()

    fig.suptitle("Reconstructed vs originals")
    ax.plot(*triangle_built.unpack(), color="r", label="Original")
    ax.plot(*orig_inv.unpack(), color="b", label="Original reconstructed")
    ax.legend()

    fig, ax = plt.subplots()

    fig.suptitle("Reconstructed vs originals")
    ax.plot(*triangle_mod.unpack(), color="r", label="AM Modulated")
    ax.plot(*mod_inv.unpack(), color="b", label="AM Modulated reconstructed")
    ax.legend()

    # fig, ax = plt.subplots()

    # sin_signal = SIN(time, 10, 10)
    # hilbert = Hilbert(sin_signal).calculate()

    # ax.plot(*sin_signal.unpack(), color="r", label="Original", linestyle=":")
    # ax.plot(*hilbert.real_part().unpack(), color="b", label="Hilbert real")
    # ax.plot(*hilbert.imag_part().unpack(), color="g", label="Hilbert imag")
    # ax.legend()

    # plt.xlim(0, 400)

    # plt.plot(*InverseFourier(orig_fourier_vals).calculate().unpack(), color="r")
    # plt.plot(*InverseFourier(mod_fourier_vals).calculate().unpack(), color="b")

    # plt.plot(*triangle_built.unpack(), color="r", alpha=1)
    # plt.plot(*triangle_mod.unpack(), color="b", alpha=1)

    # s1 = SIN(time[1:], 5, 100).apply_function_tuple(lambda t, x: x / t)
    # s2 = HEAVISIDE(time[1:], 100) * HEAVISIDE(time, 500, True)
    # s1_fourier = Fourier(s1)
    # s2_fourier = Fourier(s2)

    # fig, ax = plt.subplots()
    # ax.plot(*s1.unpack(), label="s1", color="b", alpha=0.4)
    # ax.plot(*s2.unpack(), label="s2", color="r", alpha=0.4)

    # ax.plot(*abs(s1_fourier.calculate()).unpack(), label="s1", color="r")
    # ax.plot(*abs(s2_fourier.calculate()).unpack(), label="s2", color="b")

    # ax.set_xlim(-300, 300)

    # ax.plot(*(s1.convolute(s2)).unpack(), label="convolution", color="g", linestyle=":")

    # ax.legend()

    plt.show()