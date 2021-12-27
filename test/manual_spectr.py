import matplotlib.pyplot as plt
import numpy as np

from signpy.sgn import Signal1
from signpy.transforms import stft, fourier


audio = Signal1.from_file("test/audio/audio_1.wav")
spect = stft.stft1(audio, time_interval=(0, 4), samp_time=0.05, window_method="gaussian").psd()
spect.values = spect.values.T

fig, ax = plt.subplots()
fig.suptitle("Imshow")
plt.imshow(spect.values, aspect="auto", cmap="jet")

fig, ax = plt.subplots()
fig.suptitle("Contourf")
plt.contourf(*spect.unpack(), cmap="jet")

# audio.export_to_file("test/outputs/test.wav")

plt.show()
