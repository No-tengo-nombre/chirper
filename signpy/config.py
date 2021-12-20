"""
Default parameters for this package.
"""

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||# SIGNALS #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################

INTERPOLATION_METHOD = "linear"
NOISE_TYPE = "gaussian"
HERTZ = True
CONVOLUTION_METHOD = "fft"
CROSS_CORRELATION_METHOD = "fft"

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||# TRANSFORMS #||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################

F1_METHOD = "fft"
H1_METHOD = "scipy"
Z_METHOD = "dzt"

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||# MODULATION #||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################

AM_MODULATION = "dsbsc"
PM_MODULATION = "trad"
SSB_UPPER = True
