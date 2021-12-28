from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from src.chirper.sgn.defaults import SIN


def main(show_fig=False):
    axis = np.linspace(0, 5, 50)
    values = np.linspace(0, 5, 20)

    sgn = SIN(axis, 1, 10)

    t0 = datetime.now()
    sgn_line, _, _ = sgn.interpolate(2.3, "linear")
    sgn_line_values = sgn.interpolate_list(values, "linear")
    tf = datetime.now()
    print(f" Line : {tf - t0}")

    t0 = datetime.now()
    sgn_sinc, _, _ = sgn.interpolate(2.3, "sinc")
    sgn_sinc_values = sgn.interpolate_list(values, "sinc")
    tf = datetime.now()
    print(f" Sinc : {tf - t0}")

    fig, ax = plt.subplots()
    fig.suptitle("Line interpolated")
    plt.plot(*sgn_line.unpack())

    fig, ax = plt.subplots()
    fig.suptitle("Sinc interpolated")
    plt.plot(*sgn_sinc.unpack())

    fig, ax = plt.subplots()
    fig.suptitle("Line interpolated values")
    plt.plot(*sgn_line_values.unpack())

    fig, ax = plt.subplots()
    fig.suptitle("Sinc interpolated values")
    plt.plot(*sgn_sinc_values.unpack())

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
