import matplotlib.pyplot as plt
from tqdm import tqdm

from . import *

SHOW_ALL_FIGS = False

# All these tests are imported with the `from . import *` line
tests = (
    (manual_conv1, False),
    (manual_conv2, False),
    (manual_io1, False, False),
    (manual_io2, False, False),
    (manual_hilbert, False),
    (manual_fourier1, False),
    (manual_fourier2, False),
    (manual_modulation, False),
    (manual_am_modulation, False),
)

for test, *control in tqdm(tests, desc="Running manual tests"):
    test.main(*control)
if SHOW_ALL_FIGS:
    plt.show()
