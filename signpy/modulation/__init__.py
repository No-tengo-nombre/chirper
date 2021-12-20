# import abc

# from signpy.exceptions import InvalidModulation


# class Modulator(abc.ABC):
#     """Modulator object."""
#     def __init__(self, carrier_freq, carrier_amp):
#         """Create an empty modulator.

#         Parameters
#         ----------
#         carrier_freq : float
#             Frequency of the carrier signal.
#         carrier_amp : float
#             Amplitude of the carrier signal.
#         """
#         self.carrier_freq = carrier_freq
#         self.carrier_amp = carrier_amp

#     @abc.abstractmethod
#     def apply(self, signal, method=None):
#         """Applies the modulator to a given signal.

#         Parameters
#         ----------
#         signal : sgn.signal.Signal
#             Signal to modulate.
#         method : str, optional
#             Desired method for the modulation process, by default None.

#         Raises
#         ------
#         InvalidModulation
#             If the modulation could not be applied, or if trying to apply
#             an empty modulator.
#         """
#         # raise InvalidModulation("Can not apply empty modulator.")
#         pass
