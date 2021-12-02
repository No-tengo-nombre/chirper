from signpy.sgn.signal import Signal1

import abc


class Transform(Signal1, abc.ABC):
    """Abstract class for an integral transform (Fourier, Laplace, etc.)."""
    def __init__(self, target: Signal1):
        """Creates an instance of this integral transform.

        Parameters
        ----------
        target : sgn.Signal1
            Signal to apply the transform to. Must be a one-dimensional
            signal.
        """
        self.signal = target
        target_axis = target.axis
        super().__init__(target_axis, 0 * target_axis)

    @abc.abstractmethod
    def calculate(self) -> Signal1:
        """Applies the transform to the target signal.

        Returns
        -------
        Result of the transform.
        """
        pass
