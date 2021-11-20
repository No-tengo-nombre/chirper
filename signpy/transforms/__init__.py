import abc

import signpy.sgn.signal


class Transform(abc.ABC, signpy.sgn.signal.Signal):
    """Abstract class for an integral transform (Fourier, Laplace, etc.)."""
    def __init__(self, target):
        """Creates an instance of this integral transform.

        Parameters
        ----------
        target : sgn.Signal
            Signal to apply the transform to.
        """
        self.signal = target
        target_time = target.time
        super().__init__(target_time, 0 * target_time)

    @abc.abstractmethod
    def calculate(self):
        """Applies the transform to the target signal.

        Returns
        -------
        Result of the transform.
        """
        pass
