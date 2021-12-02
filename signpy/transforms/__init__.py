from signpy import sgn

import abc


class Transform(sgn.Signal, abc.ABC):
    """Abstract class for an integral transform (Fourier, Laplace, etc.)."""
    def __init__(self, target: sgn.Signal):
        """Creates an instance of this transform.

        Parameters
        ----------
        target : sgn.Signal
            Signal to apply the transform to.
        """
        self.signal = target
        target_axis = target.axis
        super().__init__(target_axis, 0 * target_axis)

    @abc.abstractmethod
    def calculate(self) -> sgn.Signal:
        """Applies the transform to the target signal.

        Returns
        -------
        Result of the transform.
        """
        pass

class Transform1(Transform, sgn.Signal1):
    pass
