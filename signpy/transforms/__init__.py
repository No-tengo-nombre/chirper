# from __future__ import annotations
# from typing import TYPE_CHECKING
# import abc

# from signpy.sgn import Signal1, Signal


# class Transform(Signal, abc.ABC):
#     """Abstract class for an integral transform (Fourier, Laplace, etc.)."""
#     @abc.abstractmethod
#     def calculate(self) -> Signal:
#         """Applies the transform to the target signal.

#         Returns
#         -------
#         Result of the transform.
#         """
#         pass


# class Transform1(Transform, Signal1):
#     def __init__(self, target: Signal1):
#         self.signal = target
#         super().__init__(*target.unpack())
