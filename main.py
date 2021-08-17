from sgn.signal import Signal

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    wave1 = {
        "freq": 0.5,
        "amp": 10
    }
    wave2 = {
        "freq": 25,
        "amp": 5
    }
    wave3 = {
        "freq": 125,
        "amp": 2.5
    }

    time = np.linspace(0, 100, 100000)

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

    fig, ax = plt.subplots()
    # plt.plot(*signal1.unpack(), color="r")
    # plt.plot(*signal2.unpack(), color="b")
    # plt.plot(*signal3.unpack(), color="g")
    # plt.plot(*(signal1 + signal3).rect_smooth(1501).unpack(), color="r")

    plt.show()
