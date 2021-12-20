import matplotlib.pyplot as plt
from tqdm import tqdm

from . import (manual_am_modulation, manual_conv, manual_io,
               manual_hilbert, manual_fourier, manual_modulation)


SHOW_ALL_FIGS = False

tests = (
    (manual_am_modulation, False),
    (manual_conv, False),
    (manual_io, False),
    (manual_hilbert, False),
    (manual_fourier, False),
    (manual_modulation, False),
)

for test, show in tqdm(tests, desc="Running manual tests"):
    test.main(show)
if SHOW_ALL_FIGS:
    plt.show()
