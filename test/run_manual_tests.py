import matplotlib.pyplot as plt
from tqdm import tqdm

from . import (manual_am_modulation, manual_conv, manual_io, 
    manual_hilbert, manual_fourier, manual_modulation)


tests = (
    manual_am_modulation,
    manual_conv,
    manual_io,
    manual_hilbert,
    manual_fourier,
    manual_modulation,
)

for test in tqdm(tests, desc="Running manual tests"):
    test.main(False)
# plt.show()
