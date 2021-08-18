import sgn.signal as signal
from sgn.signal import Signal
from transforms.fourier import Fourier, InverseFourier

import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    wave1 = {
        "freq": 2 * np.pi * 5,
        "amp": 10
    }
    wave2 = {
        "freq": 2 * np.pi * 250,
        "amp": 5
    }
    wave3 = {
        "freq": 2 * np.pi * 600,
        "amp": 2.5
    }

    time = np.linspace(-1500, 1500, 3000)

    signal1 = Signal.from_function(
        time,
        lambda t: wave1["amp"] * np.sin(wave1["freq"] * t)
    )
    signal2 = Signal.from_function(
        time,
        lambda t: wave2["amp"] * np.sin(wave2["freq"] * t)
    )
    signal3 = Signal.from_function(
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

    fig, ax = plt.subplots()

    # plt.plot(*signal1.unpack(), color="b")
    # plt.plot(*signal2.unpack(), color="b")
    # plt.plot(*signal3.unpack(), color="b")
    # plt.plot(*sum_signal.unpack(), color="b")
    # plt.plot(*(sq_signal + noise5).unpack(), color="b")

    fourier = Fourier(sq_signal).calculate()#.half()

    plt.plot(*abs(fourier).unpack(), color="r")
    plt.plot(*InverseFourier(fourier).calculate().unpack(), color="b")

    # plt.xlim(0)

    plt.show()
