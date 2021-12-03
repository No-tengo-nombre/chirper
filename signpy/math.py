# from signpy.sgn import Signal1

import numpy as np


def convolute(s1_x, s1_y):
    copy = s1_x.clone()
    return copy.apply_function(_conv_helper, s1_y)

def _conv_helper(self, a, signal1):
    sum = 0
    for k in signal1.time:
        sum += a * signal1[k]
    return sum

def cross_correlation(s1_x, s1_y):
    copy = s1_x.clone()
