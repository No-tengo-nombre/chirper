import abc

import sgn.signal


class Transform(abc.ABC, sgn.signal.Signal):
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
    def calculate(self) -> sgn.signal.Signal:
        """Applies the transform to the target signal.

        Returns
        -------
        New sgn.signal.Signal representing the result of the transform.
        """
        pass
