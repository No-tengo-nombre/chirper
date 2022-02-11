"""
Module that defines utilities for generating kernels, used for image
processing
"""
import numpy as np


def ker_mean(size):
    """Creates a kernel that, when convoluted with a two dimensional
    signal, takes the mean over a given size. The `size` parameter
    determines how far the kernel will reach for the values.

    Parameters
    ----------
    size : int, odd
        Size of the kernel.

    Returns
    -------
    np.ndarray
        Kernel matrix.

    Raises
    ------
    ValueError
        If a `size` is given that isn't an odd integer.
    """
    if size % 2 != 1:
        raise ValueError("Size must be an odd integer.")
    return np.ones((size, size)) / (size ** 2)


def ker_edge(level=2):
    """Creates an edge detecting kernel.

    Parameters
    ----------
    level : int, optional
        Sensibility of the edge detection, by default 2.

    Returns
    -------
    np.ndarray
        Kernel matrix.
    """
    if level == 0:
        return np.array([
            [1, 0, -1],
            [0, 0, 0],
            [-1, 0, 1]
        ])
    elif level == 1:
        return np.array([
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ])
    elif level == 2:
        return np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ])


def ker_sharpen():
    """Creates a kernel that sharpens a two dimensional signal.

    Returns
    -------
    np.ndarray
        Kernel matrix.
    """
    return np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ])
