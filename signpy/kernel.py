import numpy as np


def ker_mean(size):
    return np.array(
        [[1 / size ** 2 for _ in range(size)] for _ in range(size)]
    )
