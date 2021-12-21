class DimensionError(Exception):
    """Exception for innapropriate object dimensions."""
    pass


class InvalidModulation(Exception):
    """Exception for invalid calls to modulators."""
    pass


class InvalidFileExtension(Exception):
    """Exception for invalid file extensions."""

    def __init__(self, message="Invalid file extension", extension=None, exp_extension=None) -> None:
        self.extension = extension
        self.exp_extension = exp_extension
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message} (expected {self.exp_extension}, was given {self.extension})"
