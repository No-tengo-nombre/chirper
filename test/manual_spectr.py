import matplotlib.pyplot as plt

from src.chirper.sgn import Signal1
from src.chirper.transforms import stft


def main(show_fig=False):
    audio = Signal1.from_file("test/audio/flute_a4.wav")
    spect = stft.stft1(audio, time_interval=(0, 1), samp_time=0.05,
                       window_method="gaussian").half()

    print(spect.imshow())
    fig, ax = plt.subplots()
    fig.suptitle("Imshow abs")
    # plt.imshow(spect.abs().values.T, aspect="auto", cmap="jet", origin="lower", extent=())
    plt.imshow(**spect.imshow(), aspect="auto", cmap="jet", origin="lower")

    fig, ax = plt.subplots()
    fig.suptitle("Imshow PSD")
    plt.imshow(spect.psd().values.T, aspect="auto", cmap="jet", origin="lower")

    fig, ax = plt.subplots()
    fig.suptitle("Contourf abs")
    plt.contourf(*spect.abs().contourf(), cmap="jet")
    ax.set_ylim(0, 2500)

    fig, ax = plt.subplots()
    fig.suptitle("Contourf PSD")
    plt.contourf(*spect.psd().contourf(), cmap="jet")
    ax.set_ylim(0, 2500)

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
