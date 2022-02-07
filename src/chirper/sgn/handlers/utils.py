from multipledispatch import dispatch

from ...exceptions import InvalidFileExtension


@dispatch(str, str)
def validate_extension(filename: str, expected: str) -> None:
    """Validates the extension of the given filename.

    Parameters
    ----------
    filename : str
        Name of the file to check.
    expected : str
        Expected file extension.

    Raises
    ------
    InvalidFileExtension
        If the file extension is not valid.
    """
    extension = filename.split(".")[-1]
    if extension != expected:
        raise InvalidFileExtension(extension=extension, exp_extension=expected)


@dispatch(str, (list, tuple))
def validate_extension(filename: str, expected: list[str]) -> None:
    """Validates the extension of the given filename.

    Parameters
    ----------
    filename : str
        Name of the file to check.
    expected : list[str]
        List of expected file extensions.

    Raises
    ------
    InvalidFileExtension
        If the file extension is not valid.
    """
    extension = filename.split(".")[-1]
    if extension not in expected:
        raise InvalidFileExtension(extension=extension, exp_extension=expected)
