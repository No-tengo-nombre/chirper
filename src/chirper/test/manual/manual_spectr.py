import matplotlib.pyplot as plt

from chirper.sgn import Signal1
from chirper.transforms import stft1


def main(show_fig=False):
    audio = Signal1.from_file("chirper/test/manual/audio/audio_4.wav")
    spect = stft1(audio, time_interval=(0, 3), samp_time=0.05,
                       window_method="gaussian").half()

    fig, ax = plt.subplots()
    fig.suptitle("Imshow abs")
    plt.imshow(**spect.abs().imshow(), aspect="auto", cmap="jet", origin="lower")

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
