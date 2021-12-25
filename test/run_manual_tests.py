import matplotlib.pyplot as plt
from tqdm import tqdm

from . import (manual_am_modulation, manual_conv1, manual_conv2, manual_hilbert,
               manual_fourier1, manual_fourier2, manual_io1, manual_modulation)


SHOW_ALL_FIGS = False

tests = (
    (manual_am_modulation, False),
    (manual_conv1, False),
    (manual_conv2, False),
    (manual_io1, False, False),
    (manual_hilbert, False),
    (manual_fourier1, False),
    (manual_fourier2, False),
    (manual_modulation, False),
)

for test, *control in tqdm(tests, desc="Running manual tests"):
    test.main(*control)
if SHOW_ALL_FIGS:
    plt.show()
